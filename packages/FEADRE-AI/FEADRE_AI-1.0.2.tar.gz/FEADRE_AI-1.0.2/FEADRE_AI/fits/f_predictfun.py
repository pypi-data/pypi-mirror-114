import sys
import time
from abc import abstractmethod

import numpy as np
import cv2
import torch
from PIL import ImageFont
from torch import nn

from ftools.GLOBAL_LOG import flog
from ftools.picture.f_show import f_show_od_ts4plt_v3, f_show_od_np4plt_v3, draw_text_chinese4cv


def nms(boxes, scores, iou_threshold):
    ''' IOU大于0.5的抑制掉
         boxes (Tensor[N, 4])) – bounding boxes坐标. 格式：(ltrb
         scores (Tensor[N]) – bounding boxes得分
         iou_threshold (float) – IoU过滤阈值
     返回:NMS过滤后的bouding boxes索引（降序排列）
     '''
    return torch.ops.torchvision.nms(boxes, scores, iou_threshold)


def batched_nms(boxes_ltrb, scores, idxs, threshold_iou):
    '''
    多 labels nms
    :param boxes_ltrb: 拉平所有类别的box重复的 n*20类,4
    :param scores: torch.Size([16766])
    :param idxs:  真实类别index 通过手动创建匹配的 用于表示当前 nms的类别 用于统一偏移 技巧
    :param threshold_iou:float 0.5
    :return:
    '''
    if boxes_ltrb.numel() == 0:  # 维度全乘
        return torch.empty((0,), dtype=torch.int64, device=boxes_ltrb.device)

    # torchvision.ops.boxes.batched_nms(boxes, scores, lvl, nms_thresh)
    # 根据最大的一个值确定每一类的偏移
    max_coordinate = boxes_ltrb.max()  # 选出每个框的 坐标最大的一个值
    # idxs 的设备和 boxes 一致 , 真实类别index * (1+最大值) 则确保同类框向 左右平移 实现隔离
    offsets = idxs.to(boxes_ltrb) * (max_coordinate + 1)
    # boxes 加上对应层的偏移量后，保证不同类别之间boxes不会有重合的现象
    boxes_for_nms = boxes_ltrb + offsets[:, None]
    keep = nms(boxes_for_nms, scores, threshold_iou)
    return keep


def batch_nms_v1(ids_batch1, p_ltrb1, p_labels1, p_scores1, threshold_nms):
    '''
    这个是以 迭代每一个类, 每次出一个类的所有batch的结果,
    难以以每个批次选100进行加速 , 如果用nms的全部结果,则没有问题
    :param ids_batch1: [nn]
    :param p_ltrb1: [nn,4] float32
    :param p_labels1: [nn]
    :param p_scores1: [nn]
    :return:
    '''
    device = p_ltrb1.device
    p_labels_unique = p_labels1.unique()  # nn -> n
    ids_batch2, p_scores2, p_labels2, p_ltrb2 = [], [], [], []

    for lu in p_labels_unique:  # 迭代每个类别
        # 过滤类别
        _mask = p_labels1 == lu
        _ids_batch = ids_batch1[_mask]
        _p_scores = p_scores1[_mask]
        _p_ltrb = p_ltrb1[_mask]
        # 这里用batch去区分
        keep = batched_nms(_p_ltrb, _p_scores, _ids_batch, threshold_nms)
        _p_labels = p_labels1[_mask]

        # 每批100个
        ids_batch2.append(_ids_batch[keep])
        p_scores2.append(_p_scores[keep])
        p_labels2.append(_p_labels[keep])
        p_ltrb2.append(_p_ltrb[keep])

    ids_batch2 = torch.cat(ids_batch2, 0)
    p_scores2 = torch.cat(p_scores2, 0)
    p_labels2 = torch.cat(p_labels2, 0)
    p_ltrb2 = torch.cat(p_ltrb2, 0)

    # print('12')
    return ids_batch2, p_ltrb2, p_labels2, p_scores2


def batch_nms_v2(ids_batch1, p_ltrb1, p_labels1, p_scores1, threshold_nms, num_max=100):
    '''
    以每个batch进行迭代 可以每个batch选100个最好的结果 进行评分加速 和筛选
    :param ids_batch1: [nn]
    :param p_ltrb1: [nn,4] float32
    :param p_labels1: [nn]
    :param p_scores1: [nn]
    :param num_max: 通常一张图选 100个高分加速
    :return:
    '''
    device = p_ltrb1.device
    ids_batch_unique = ids_batch1.unique()  # nn -> n
    ids_batch2, p_scores2, p_labels2, p_ltrb2 = [], [], [], []

    for lu in ids_batch_unique:  # 迭代每个批次
        # 过滤类别
        _mask = ids_batch1 == lu
        _p_scores = p_scores1[_mask]
        _p_labels = p_labels1[_mask]
        _p_ltrb = p_ltrb1[_mask]
        keep = batched_nms(_p_ltrb, _p_scores, _p_labels, threshold_nms)
        _ids_batch = ids_batch1[_mask]
        # 每批100个
        keep = keep[:num_max]

        ids_batch2.append(_ids_batch[keep])
        p_scores2.append(_p_scores[keep])
        p_labels2.append(_p_labels[keep])
        p_ltrb2.append(_p_ltrb[keep])

    ids_batch2 = torch.cat(ids_batch2, 0)
    p_scores2 = torch.cat(p_scores2, 0)
    p_labels2 = torch.cat(p_labels2, 0)
    p_ltrb2 = torch.cat(p_ltrb2, 0)

    # print('12')
    return ids_batch2, p_ltrb2, p_labels2, p_scores2


class Predicting_Base(nn.Module):
    '''
    由 f_fit_eval_base 运行至net模型主Center 再由模型主Center调用
    返回到 f_fit_eval_base
    '''

    def __init__(self, cfg) -> None:
        '''

        :param mode_vis:  这里是nms的 模式 bbox keypoints
        cfg.PRED_CONF_THR  # 阀值
        cfg.PRED_NMS_THR  # 阀值
        cfg.PRED_SELECT_TOPK  # 初选个数
        cfg.MODE_VIS
        '''
        super(Predicting_Base, self).__init__()
        self.cfg = cfg

    @abstractmethod
    def p_init(self, model_outs, targets):
        '''
        p_init 处理数据
        :param model_outs:
        :param targets: 这个需要处理  例如 to.显卡
        :return:
        '''

    @abstractmethod
    def get_pscores(self, outs, targets):
        '''

        :param outs: p_init 处理后
        :param targets: 这个需要处理  例如 to.显卡
        :return:
            pscores : 这个用于判断 生成 mask_pos
            plabels : 这个用于二阶段
            pconf : 用于显示conf的统计值
        '''

    @abstractmethod
    def get_stage_res(self, outs, mask_pos, pscores, plabels, imgs_ts_4d, targets, off_ltrb_ts):
        '''

        :param imgs_ts_4d: 这个需要处理
        :param targets:
        :param off_ltrb_ts: 实际归一化尺寸 这个需要处理
        :return:
            ids_batch1 : 返回第二阶段
            pboxes_ltrb1 :
            plabels1 :
            pscores1 :
        '''

    def forward(self, model_outs, imgs_ts_4d=None, targets=None, off_ltrb_ts=None):
        '''
        由 FModelBase 已处理  toones_wh_ts_input
        :param model_outs: 这个输出就已经带了 device
        :return:
        '''
        ''' 进行数据的处理 传递到 get_pscores get_stage_res 中'''
        outs = self.p_init(model_outs, targets)

        ''' 返回分数 和 plabels    pconf可返回任意值 用于没有目标时分析值域 '''
        pscores, plabels, pconf = self.get_pscores(outs, targets)
        # batch, dim = pscores.shape
        mask_pos = pscores > self.cfg.PRED_CONF_THR
        if not torch.any(mask_pos):  # 如果没有一个对象
            print('该批次没有找到目标 max:{0:.2f} min:{0:.2f} mean:{0:.2f}'.format(pconf.max().item(),
                                                                          pconf.min().item(),
                                                                          pconf.mean().item(),
                                                                          ))
            return [None] * 5

        # dim中 取500个
        if pscores.shape[-1] > self.cfg.PRED_SELECT_TOPK:  # 并行取top100 与mask_pos 进行and操作
            # 最大1000个
            ids_topk = pscores.topk(self.cfg.PRED_SELECT_TOPK, dim=-1)[1]  # torch.Size([32, 1000])
            mask_topk = torch.zeros_like(mask_pos)
            mask_topk[torch.arange(ids_topk.shape[0])[:, None], ids_topk] = True
            mask_pos = torch.logical_and(mask_pos, mask_topk)

        # ids_batch1, pboxes_ltrb1, plabels1, pscores1,pkp_keypoint
        reses = self.get_stage_res(outs, mask_pos, pscores, plabels, imgs_ts_4d, targets, off_ltrb_ts)

        if self.cfg.MODE_VIS == 'bbox':  # 单人脸
            assert len(reses) == 4, 'res = self.get_stage_res(outs, mask_pos, pscores, plabels) 数据错误'
            ids_batch2, p_boxes_ltrb2, p_labels2, p_scores2 = batch_nms_v2(reses[0],
                                                                           reses[1],
                                                                           reses[2],
                                                                           reses[3],
                                                                           self.cfg.PRED_NMS_THR,
                                                                           num_max=100,
                                                                           )

            return ids_batch2, p_boxes_ltrb2, None, p_labels2, p_scores2,
        elif self.cfg.MODE_VIS == 'keypoints':
            # assert len(reses) == 5, 'res = self.get_stage_res(outs, mask_pos, pscores, plabels) 数据错误'
            # ids_batch2, p_boxes_ltrb2, p_keypoints2, p_labels2, p_scores2 = batch_nms4kp(
            #     ids_batch1=reses[0],
            #     p_boxes_ltrb1=reses[1],
            #     p_labels1=reses[2],
            #     p_scores1=reses[3],
            #     p_keypoints1=reses[4],
            #     threshold_nms=self.cfg.PRED_NMS_THR)
            # return ids_batch2, p_boxes_ltrb2, p_keypoints2, p_labels2, p_scores2
            raise Exception('不支持 keypoints')
        else:
            raise Exception('self.mode_vis = %s 错误' % self.cfg.mode_vis)


def f_prod_vodeo(cap, data_transform, model, ids_classes, device):
    fps = 0.0
    count = 0
    num_out = 0
    while True:
        start_time = time.time()
        '''---------------数据加载及处理--------------'''
        ref, img_np_file = cap.read()  # 读取某一帧 ref是否成功
        if not ref:
            if num_out >= 3:
                raise Exception('cap 读取出错~~~num_out=%s' % num_out)
            num_out += 1
            flog.error('cap 读取出错，再试')
            continue

        size_wh_file = np.array(img_np_file.shape[:2][::-1])
        img_ts_3d, target = data_transform(img_np_file)
        img_ts_4d = img_ts_3d.unsqueeze(0).to(device)

        p_boxes_ltrb_f, title_text, p_texts = fprod(model=model,
                                                    img_ts_4d=img_ts_4d,
                                                    size_wh_file=size_wh_file,
                                                    ids_classes=ids_classes,
                                                    target=target,
                                                    )
        # cv转码 乱码
        if isinstance(p_boxes_ltrb_f, torch.Tensor):
            # ts -> np
            p_boxes_ltrb_f = p_boxes_ltrb_f.numpy()

        img_np = img_np_file
        for box, text in zip(p_boxes_ltrb_f, p_texts):
            box = box.astype(np.int)
            cv2.rectangle(img_np, (box[0], box[1]), (box[2], box[3]), (0, 0, 255), 2)  # (l,t),(r,b),颜色.宽度
            cx = box[0]
            cy = box[1] + 12
            cv2.putText(img_np, text, (cx, cy), cv2.FONT_HERSHEY_DUPLEX, 0.5, (255, 255, 255), )

        img_np = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)

        # print("fps= %.2f" % (fps))
        count += 1
        text_ = "%s fps= %.2f count=%s " % (title_text, fps, count)
        # 图片，添加的文字，左上角坐标，字体，字体大小，颜色，字体粗细
        img_np = cv2.putText(img_np, text_, (0, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                             (0, 255, 0), 1)
        # img_np=draw_text_chinese4cv(img_np, text_, 0, 40, )
        # 极小数
        fps = (fps + (1. / max(sys.float_info.min, time.time() - start_time))) / 2

        # cv2.imshow(title_text, img_np)
        # cv2.imshow('无效'.encode("gbk").decode(errors="ignore"), img_np) # 无效
        cv2.imshow(u'abc', img_np)

        c = cv2.waitKey(1) & 0xff  # 输入esc退出
        if c == 27:
            cap.release()
            cv2.destroyAllWindows()
            break


def f_prod_pic(file, data_transform, model, ids_classes, device):
    img_np_file = cv2.imread(file)  # h,w,c bgr
    size_wh_file = np.array(img_np_file.shape[:2][::-1])

    # 这个必须返回一个target
    img_ts_3d, target = data_transform(img_np_file)
    img_ts_4d = img_ts_3d.unsqueeze(0).to(device)

    p_boxes_ltrb_f, title_text, p_texts = fprod(model=model,
                                                img_ts_4d=img_ts_4d,
                                                size_wh_file=size_wh_file,
                                                ids_classes=ids_classes,
                                                target=target,
                                                )
    f_show_od_np4plt_v3(img_np_file, p_ltrb=p_boxes_ltrb_f, title=title_text, p_texts=p_texts,
                        is_recover_size=False)
    pass


def fprod(model, img_ts_4d, size_wh_file, ids_classes, target):
    with torch.no_grad():
        # 这里要传数组 要全4d的
        reses, imgs_ts_4d, targets, off_ltrb = model((img_ts_4d, [target]))
        ids_batch, p_ltrbs, p_kps, p_labels, p_scores = reses
        if p_labels is None or len(p_labels) == 0:
            flog.debug('没有目标 %s', )
            # sys.exit(-1)
        else:
            p_texts = []
            for i, p_label in enumerate(p_labels):
                s = ids_classes[str(p_label.long().item())] + ':' + str(round(p_scores[i].cpu().item(), 2))
                p_texts.append(str(s))

            # --------------- input可视 ----------------
            # title_text = '%s x %s (num_pos = %s) max=%s' % (str(size_wh_input[0]),
            #                                                 str(size_wh_input[1]),
            #                                                 str(len(p_ltrbs)),
            #                                                 str(round(p_scores.max().cpu().item(), 2))
            #                                                 )
            # # torch.tensor(size_wh_input)+torch.tensor(off_ltrb)
            # f_show_od_ts4plt_v3(img_ts_3d, p_ltrb=p_ltrbs,
            #                     title=title_text,
            #                     is_recover_size=True, is_normal=True)

            # --------------- file可视 -----------------
            title_text = '%s x %s (num_pos = %s) max=%s' % (str(size_wh_file[0]),  # w
                                                            str(size_wh_file[1]),  # h
                                                            str(len(p_ltrbs)),
                                                            str(round(p_scores.max().cpu().item(), 2))
                                                            )
            size_wh_file_x2 = np.tile(size_wh_file, 2)
            p_boxes_ltrb_f = p_ltrbs * size_wh_file_x2
    return p_boxes_ltrb_f, title_text, p_texts
