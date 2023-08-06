import torch

from ftools.GLOBAL_LOG import flog
from ftools.boxes.f_boxes import bbox_iou_v3, ltrb2xywh, xywh2ltrb
from ftools.calc.f_calc_adv import f_cre_grid_cells

from ftools.picture.f_show import f_show_od_ts4plt_v3


def match4atss(gltrb_i_b, anc_ltrb_i, nums_dim_t_list, num_atss_topk=9, glabels_b=None,
               img_ts=None, is_visual=False):
    '''
    这里默认都是 input 尺寸 且是batch
    核心作用:
        1. 使正例框数量都保持一致 保障小目标也能匹配到多个anc
        2. 用最大一个iou的均值和标准差,计算阀值,用IOU阀值初选正样本
        3. 确保anc中心点在gt框中

    :param gltrb_i_b:
    :param anc_ltrb_i:
    :param anc_ltrb_i:
    :param nums_dim_t_list:
        [1600, 400, 100] 这个是每个特图对应的维度数 用于索引 如果只有一层可以优化掉
    :param num_atss_topk: # 这个 topk = 初选个数 要 * 该层的anc数
    :param glabels_b: 暂时没用 可视化
    :param img_ts: 可视化
    :param is_visual:  可视化
    :return:
        mask_pos : [2100] 正例mask
        anc_max_iou: [2100] anc 对应的最大IOU值
        g_pos_index: [2100] anc 对应GT的索引
    '''

    def _force_set(device, ious_ag, mask_pos4all, mask_pos4distances, num_atss_topk):
        # 强制以IOU匹配 num_atss_topk 个   [2100, ngt] -> [2100] -> [nnn] ^^ -> tuple([n_nogt])
        indexes = torch.where(mask_pos4all.sum(0) == 0)[0]
        _mask = torch.zeros_like(ious_ag, dtype=torch.bool, device=device)

        for ii in indexes:
            # [2100, ngt] -> [2100,1] -> [2100]
            _mask_dis = mask_pos4distances[:, ii].squeeze(-1)
            # [2100,ngt] -> [nnnn]
            _iou_s = ious_ag[_mask_dis, ii]
            max_index = _iou_s.topk(num_atss_topk)[1]
            _m = torch.zeros_like(_iou_s, dtype=torch.bool)
            _m[max_index] = True
            _mask[_mask_dis, ii] = _m

        return _mask

    device = gltrb_i_b.device

    # 计算 iou
    anc_xywh_i = ltrb2xywh(anc_ltrb_i)
    # num_anc = anc_xywh_i.shape[0]
    # (anc 个,boxes 个) torch.Size([3, 10647])
    ious_ag = bbox_iou_v3(anc_ltrb_i, gltrb_i_b)
    num_gt = gltrb_i_b.shape[0]  # 正样本个数

    # 全部ANC的距离
    gxywh_i_b = ltrb2xywh(gltrb_i_b)
    # 中间点绝对距离 多维广播 (anc 个,boxes 个)  torch.Size([32526, 7])
    distances = (anc_xywh_i[:, None, :2] - gxywh_i_b[None, :, :2]).pow(2).sum(-1).sqrt()

    # 每层 anc 数是一致的
    # num_atss_topk = 9  # 这个 topk = 初选个数 要 * 该层的anc数

    idxs_candidate = []  # 这个用来保存最一层所匹配的最小距离anc的索引  每层9个
    index_start = 0  # 这是每层的anc偏移值
    for i, num_dim_feature in enumerate(nums_dim_t_list):  # [24336, 6084, 1521, 441, 144]
        '''每一层的每一个GT选 topk * anc数'''
        index_end = index_start + num_dim_feature
        # 取出某层的所有anc距离  中间点绝对距离 (anc 个,boxes 个)  torch.Size([32526, 7]) -> [nn, 7]
        distances_per_level = distances[index_start:index_end, :]
        # 确认该层的TOPK 不能超过该层总 anc 数 这里是一个数
        topk = min(num_atss_topk, num_dim_feature)
        # 选 topk个最小的 每个gt对应对的anc的index torch.Size([24336, box_n])---(anc,gt) -> torch.Size([topk, 1])
        _, topk_idxs_per_level = distances_per_level.topk(topk, dim=0, largest=False)  # 只能在某一维top
        idxs_candidate.append(topk_idxs_per_level + index_start)
        index_start = index_end

    # 用于计算iou均值和方差 候选人，候补者；应试者 torch.Size([405, 1])
    idxs_candidate = torch.cat(idxs_candidate, dim=0)
    '''--- 选出每层每个anc对应的距离中心最近topk iou值 ---'''
    # ***************这个是ids选择 这个是多维筛选 ious---[anc,ngt]    [405, ngt] [0,1...ngt]-> [405,ngt]
    ious_candidate = ious_ag[idxs_candidate, torch.arange(num_gt)]  # 这里是index 蒙板取数的方法
    mask_pos4distances = torch.zeros_like(distances, device=device, dtype=torch.bool)
    # [2000,ngt]
    mask_pos4distances[idxs_candidate, torch.arange(idxs_candidate.shape[1])] = True

    '''--- 用最大一个iou的均值和标准差,计算阀值 ---'''
    # 统计每一个 GT的均值 std [ntopk,ngt] -> [ngt] 个
    _iou_mean_per_gt = ious_candidate.mean(dim=0)  # 除维
    _iou_std_per_gt = ious_candidate.std(dim=0)
    _iou_thresh_per_gt = _iou_mean_per_gt + _iou_std_per_gt
    '''--- 用IOU阀值初选正样本 ---'''
    # torch.Size([32526, 1]) ^^ ([ngt] -> [1,ngt]) -> [32526,ngt]
    mask_pos4iou = ious_ag >= _iou_thresh_per_gt.unsqueeze(0)  # 核心是这个选

    '''--- 中心点需落在GT中间 需要选出 anc的中心点-gt的lt为正, gr的rb-anc的中心点为正  ---'''
    # torch.Size([32526, 1, 2])
    dlt = anc_xywh_i[:, None, :2] - gltrb_i_b[None, :, :2]
    drb = gltrb_i_b[None, :, 2:] - anc_xywh_i[:, None, :2]
    # [32526, 1, 2] -> [32526, 1, 4] -> [32526, 1]
    mask_pos4in_gt = torch.all(torch.cat([dlt, drb], dim=-1) > 0.01, dim=-1)
    mask_pos4all = torch.logical_and(torch.logical_and(mask_pos4distances, mask_pos4iou), mask_pos4in_gt)

    '''--- 生成最终正例mask [32526, ngt] -> [32526] ---'''
    # 多个GT可能对应 不同的index 需要合并
    msak_pos_1d = mask_pos4all.any(1)

    '''--- 确定anc匹配 一个锚框被多个真实框所选择，则其归于iou较高的真实框  ---'''
    # (anc 个,boxes 个) torch.Size([3, 10647])
    anc_max_iou, g_index = ious_ag.max(dim=1)  # 存的是 bboxs的index

    ''' 这里是强制代码 '''
    if msak_pos_1d.sum() == 0 or (mask_pos4iou.sum(0) == 0).any() or (mask_pos4all.sum(0) == 0).any():
        '''
        msak_pos_1d 该图所有GT都没有匹配GT,概率较低
        mask_pos4iou 该图存在的通过IOU高斯值 没有匹配到的GT
        mask_pos4all 最终IOU+框内条件 存在有没有匹配到的GT
        '''
        # mask_pos4all mask_pos4iou mask_pos4distances
        # flog.debug('有问题 mask_pos4iou= %s, mask_pos4iou= %s, mask_pos4all= %s '
        #            % (mask_pos4distances.sum(0), mask_pos4iou.sum(0), mask_pos4all.sum(0)))
        # 强制修正 1阶段 选5个IOU最大的 再进行框内逻辑
        _mask = _force_set(device, ious_ag, mask_pos4all, mask_pos4distances, 5)
        # 更新 两个mask
        mask_pos4all[_mask] = True
        mask_pos4all = torch.logical_and(mask_pos4all, mask_pos4in_gt)  # 优先框内
        # 1阶段未修复的 2阶段直接取两个IOU最大的匹配
        if (mask_pos4all.sum(0) == 0).any():
            # 二次修正 单修就很难再进来
            # flog.error('二次修正,强制选一个 mask_pos4all= %s' % (mask_pos4all.sum(0)))
            _mask = _force_set(device, ious_ag, mask_pos4all, mask_pos4distances, 2)
            mask_pos4all[_mask] = True
        msak_pos_1d = mask_pos4all.any(1)
        # 修正强制IOU 对应关系  解决iou小 最终被强制修订  这里不能再用 anc_max_iou值
        ious_ag[mask_pos4all] = 999
        anc_max_iou, g_index = ious_ag.max(dim=1)  # 存的是 bboxs的index
        # flog.debug('修正后匹配的GT mask_pos4all= %s ' % (mask_pos4all.sum(0)))
        # is_visual = True

    if is_visual or msak_pos_1d.sum() == 0 or (mask_pos4all.sum(0) == 0).any():
        # 修正后还不行的进来 这里
        flog.error('双重修正后不可能没有 mask_pos4iou= %s, mask_pos4all= %s ' % (mask_pos4iou.sum(0), mask_pos4all.sum(0)))
        from ftools.picture.f_show import f_show_od_ts4plt_v3
        # ***********  debug 可视  每层选9个匹配27(3*9)个正例可视化  *****************
        # 多个gt 对应一个anc 进行转换显示
        dim, ngt = mask_pos4distances.shape
        # [2100,4] -> [ngt,2100,4]
        anc_ltrb_i_pos = anc_ltrb_i.view(1, dim, 4).repeat(ngt, 1, 1)[mask_pos4distances.t()]
        f_show_od_ts4plt_v3(img_ts, g_ltrb=gltrb_i_b.cpu(),
                            # p_ltrb=anc_ltrb_i[mask_pos_distances],
                            p_ltrb=anc_ltrb_i_pos.cpu(),
                            is_normal=True,
                            )

        # ***********  可视化IOU  *****************
        # mask_pos 已经进行max iou 筛选对应的GT
        anc_ltrb_i_pos = anc_ltrb_i.view(1, dim, 4).repeat(ngt, 1, 1)[mask_pos4iou.t()]
        f_show_od_ts4plt_v3(img_ts, g_ltrb=gltrb_i_b.cpu(),
                            p_ltrb=anc_ltrb_i_pos.cpu(),
                            is_normal=True,
                            )

        # ***********  可视化  多重过滤(IOU正态阀值,框内,已对应最大GT)后个正例可视化  *****************
        # mask_pos 已经进行max iou 筛选对应的GT
        f_show_od_ts4plt_v3(img_ts, g_ltrb=gltrb_i_b.cpu(),
                            p_ltrb=anc_ltrb_i[msak_pos_1d].cpu(),
                            is_normal=True,
                            )

    return msak_pos_1d, anc_max_iou, g_index


def decode4nanodet(anc_xy_t, p_tltrb_t, max_size_hw=None):
    '''
    p -> g
    :param anc_xy_t: torch.Size([2100, 2])
    :param p_tltrb_t: torch.Size([3, 2100, 4])
    :param max_size_hw: 预测时使用 这个在归一化后使用 clamp是一样的
    :return:
    '''
    assert anc_xy_t.shape[-1] == 2, 'anc_xy_t 输入应为xy shape = %s' % anc_xy_t.shape
    # torch.Size([3, 2100])
    x1 = anc_xy_t[..., 0] - p_tltrb_t[..., 0]
    y1 = anc_xy_t[..., 1] - p_tltrb_t[..., 1]
    x2 = anc_xy_t[..., 0] + p_tltrb_t[..., 2]
    y2 = anc_xy_t[..., 1] + p_tltrb_t[..., 3]
    if max_size_hw is not None:
        x1 = x1.clamp(min=0, max=max_size_hw[1])
        y1 = y1.clamp(min=0, max=max_size_hw[0])
        x2 = x2.clamp(min=0, max=max_size_hw[1])
        y2 = y2.clamp(min=0, max=max_size_hw[0])
    # torch.Size([3, 2100]) x4 torch.Size([3, 2100,4])
    return torch.stack([x1, y1, x2, y2], -1)


def encode4nanodet(anc_xy_t, g_ltrb_t, max_val, eps=0.1, is_debug=False):
    '''
    编码针对特图
    :param anc_xy_t:  torch.Size([2100, 2])
    :param g_ltrb_t:  torch.Size([3, 2100, 4])
    :param max_val: 限制匹配的正例 最大距离 在0~7 之内
    :param is_debug:  用于查看 GT 与 匹配的点 的ltrb距离是否会超过7
    :param eps:
    :return:
    '''
    left = anc_xy_t[:, 0] - g_ltrb_t[..., 0]
    top = anc_xy_t[:, 1] - g_ltrb_t[..., 1]
    right = g_ltrb_t[..., 2] - anc_xy_t[:, 0]
    bottom = g_ltrb_t[..., 3] - anc_xy_t[:, 1]
    g_tltrb_t = torch.stack([left, top, right, bottom], -1)
    if is_debug:
        # flog.debug('注意是正例 最大值应该在7以内 min=%f  max=%f' % (g_tltrb_t.min(), g_tltrb_t.max()))
        pass
    if max_val is not None:
        g_tltrb_t = g_tltrb_t.clamp(min=0, max=max_val - eps)
    return g_tltrb_t


def match_yolo1_od(g_ltrb_input_b, g_labels_b, size_wh_t_ts, device, cfg, img_ts_input):
    '''
    匹配 gyolo 如果需要计算IOU 需在这里生成
    :param g_ltrb_input_b: ltrb
    :return:
    '''
    num_gt = g_ltrb_input_b.shape[0]
    g_txywh_t, weights, indexs_colrow_t = encode_yolo1_od(g_ltrb_input_b, size_wh_t_ts, cfg)

    g_cls_b_ = torch.zeros((size_wh_t_ts[1], size_wh_t_ts[0], cfg.NUM_CLASSES), device=device)
    g_weight_b_ = torch.zeros((size_wh_t_ts[1], size_wh_t_ts[0], 1), device=device)
    g_txywh_t_b_ = torch.zeros((size_wh_t_ts[1], size_wh_t_ts[0], 4), device=device)

    labels_index = (g_labels_b - 1).long()
    indexs_colrow_t = indexs_colrow_t.long()  # index需要long类型

    for i in range(num_gt):
        g_cls_b_[indexs_colrow_t[i, 1], indexs_colrow_t[i, 0], labels_index[i]] = 1  # 构建 onehot
        g_weight_b_[indexs_colrow_t[i, 1], indexs_colrow_t[i, 0]] = weights[i]
        g_txywh_t_b_[indexs_colrow_t[i, 1], indexs_colrow_t[i, 0]] = g_txywh_t[i]

    g_cls_b_ = g_cls_b_.reshape(-1, cfg.NUM_CLASSES)
    g_weight_b_ = g_weight_b_.reshape(-1, 1)
    g_txywh_t_b_ = g_txywh_t_b_.reshape(-1, 4)

    '''可视化验证'''
    if cfg.IS_VISUAL:
        mask_pos_1d = (g_weight_b_ > 0).any(-1)  # [169]

        # [2] -> [1,2] -> [ngt,2]
        sizes_wh_t_ts = size_wh_t_ts.unsqueeze(0).repeat(num_gt, 1)

        flog.debug('size_wh_t_ts = %s', size_wh_t_ts)
        flog.debug('g_txywh_t = %s', g_txywh_t)
        flog.debug('indexs_colrow_t = %s', indexs_colrow_t)
        flog.debug('对应index = %s', indexs_colrow_t[0, 1] * size_wh_t_ts[0] + indexs_colrow_t[0, 0])
        flog.debug('对应index = %s', torch.where(g_weight_b_ > 0))

        flog.debug('g_ltrb_input_b = %s', g_ltrb_input_b)

        grid_wh = [size_wh_t_ts[0].item(), size_wh_t_ts[1].item()]
        # 预测时需要sigmoid  这里的 g_txywh_t_b_ 已 sigmoid
        p_ltrb_t = decode_yolo1_od(p_txywh_t_sigmoidxy=g_txywh_t_b_, grid_wh=grid_wh)
        p_ltrb_t_pos = p_ltrb_t[mask_pos_1d]

        # 特图 -> input
        # img_wh_ts_x2 = torch.tensor(img_np.shape[:2][::-1], device=device).repeat(2)
        p_ltrb_input_pos = p_ltrb_t_pos * cfg.STRIDE

        flog.debug('p_ltrb_input_pos = %s', p_ltrb_input_pos)
        flog.debug(' ----------------------------------------- ')
        f_show_od_ts4plt_v3(img_ts=img_ts_input,
                            g_ltrb=g_ltrb_input_b.cpu(),
                            p_ltrb=p_ltrb_input_pos.cpu(),
                            is_recover_size=False,
                            is_normal=True,  # 图形归一化恢复
                            grid_wh_np=size_wh_t_ts.cpu().numpy()
                            )

    return g_cls_b_, g_weight_b_, g_txywh_t_b_


def encode_yolo1_od(g_ltrb_input_b, size_wh_t_ts, cfg):
    # ltrb -> xywh 原图归一化   编码xy与yolo2一样的
    g_xywh_input = ltrb2xywh(g_ltrb_input_b)
    g_xywh_t = g_xywh_input / cfg.STRIDE
    cxys_t = g_xywh_t[:, :2]
    whs_t = g_xywh_t[:, 2:]
    whs_one = whs_t / size_wh_t_ts

    # 转换到特图的格子中
    indexs_colrow_t = cxys_t.floor()
    g_txy_t = cxys_t - indexs_colrow_t
    g_twh_t = whs_t.log()
    g_txywh_t = torch.cat([g_txy_t, g_twh_t], dim=-1)

    # 值在 1~2 之间 放大小的
    weights = 2.0 - torch.prod(whs_one, dim=-1)

    return g_txywh_t, weights, indexs_colrow_t


def decode_yolo1_od(p_txywh_t_sigmoidxy, grid_wh):
    '''
    解码出来是特图
    :param p_txywh_t_sigmoidxy:  必须 c 是最后一维
    :return: 输出原图归一化
    '''
    device = p_txywh_t_sigmoidxy.device
    # 单一格子偏移 + 特图格子偏移
    p_xy_t = p_txywh_t_sigmoidxy[..., :2] \
             + f_cre_grid_cells((grid_wh[1], grid_wh[0]), is_swap=True, num_repeat=1).to(device)
    p_wh_t = p_txywh_t_sigmoidxy[..., 2:].exp()
    p_xywh_t = torch.cat([p_xy_t, p_wh_t], -1)
    p_ltrb_t = xywh2ltrb(p_xywh_t)
    return p_ltrb_t
