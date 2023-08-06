import copy
import datetime
import json
import math
import os
import sys
import tempfile
import time
from collections import deque

import cv2
import numpy as np
import torch
import torch.nn as nn
from torch.cuda.amp import GradScaler, autocast

from ftools.GLOBAL_LOG import flog
from ftools.boxes.f_boxes import ltrb2ltwh
from ftools.fits.fcocoeval import FCOCOeval
from ftools.fits.fweight import save_weight
from ftools.fmodels.tools.ema import ModelEMA
from ftools.picture.f_show import f_show_od_np4plt_v3

from ftools.f_general import get_path_root


class FModelBase(nn.Module):
    def __init__(self, net, losser, preder, is_val=None, is_test=None):
        super(FModelBase, self).__init__()
        self.net = net
        self.losser = losser
        self.preder = preder
        self.is_val = is_val
        self.is_test = is_test

    def forward(self, datas_batch):
        if isinstance(datas_batch, (tuple, list)):
            imgs_ts_4d, targets = datas_batch
        else:
            imgs_ts_4d = datas_batch
            targets = None

        # ''' 尺寸偏移 '''
        # device = imgs_ts_4d.device  # 在这里还没有进行to显卡操作
        device = self.fdevice  # 在这里还没有进行to显卡操作
        batch, c, h, w = imgs_ts_4d.shape
        off_ltrb_ts = []  # (batch,4)
        if targets is not None and 'off_ltrb' in targets[0]:  # 多尺度归一
            for target in targets:
                off_ltrb_ts.append(torch.tensor(target['off_ltrb'], dtype=torch.float, device=device))
            off_ltrb_ts = torch.stack(off_ltrb_ts, 0)
        else:
            off_ltrb_ts = torch.zeros(batch, 4, device=device, dtype=torch.float)

        if self.training:
            if targets is None:
                raise ValueError("In training mode, targets should be passed")
            # model.fdevice 这里模型自动转显卡 单显卡
            outs = self.net(imgs_ts_4d.to(self.fdevice))
            loss_total, log_dict = self.losser(outs, targets, imgs_ts_4d, off_ltrb_ts)
            return loss_total, log_dict
        else:
            reses, loss_total, log_dict = [None] * 3
            with torch.no_grad():  # 这个没用
                if (self.is_val is not None and self.is_val) or (self.is_test is not None and self.is_test):
                    outs = self.net(imgs_ts_4d.to(self.fdevice))
                    if self.is_val:
                        loss_total, log_dict = self.losser(outs, targets, imgs_ts_4d, off_ltrb_ts)

                    if self.is_test:
                        # outs模型输出  返回 ids_batch, p_boxes_ltrb, p_keypoints, p_labels, p_scores
                        reses = self.preder(outs, imgs_ts_4d, targets, off_ltrb_ts)

            return reses, imgs_ts_4d, targets, off_ltrb_ts, loss_total, log_dict


class FitExecutor:
    def __init__(self, cfg, model, fun_loss, save_weight_name, path_save_weight,
                 optimizer=None, dataloader_train=None, lr_scheduler=None,
                 end_epoch=None, is_mixture_fit=True, lr_val_base=1e-3,
                 is_writer=False, keep_writer=None,
                 print_freq=10,
                 dataloader_test=None, maps_def_max=None,
                 num_vis_z=None, mode_vis=None,
                 ) -> None:
        '''
        参数在 cfg 中具备较强依赖, 将参数分离出来 可用于独立使用
        大写为必须 小写为特殊方法使用

        :param fun_loss: 回调 loss 处理
        '''
        super().__init__()
        self.dataloader_train = dataloader_train
        self.model = model
        self.optimizer = optimizer
        self.lr_scheduler = lr_scheduler
        self.end_epoch = end_epoch
        self.is_mixture_fit = is_mixture_fit
        self.lr_val_base = lr_val_base

        self.fun_loss = fun_loss
        self.cfg = cfg

        # 测试属性
        self.dataloader_test = dataloader_test
        self.num_vis_z = num_vis_z  # 预测时显示的图片数
        self.mode_vis = mode_vis  # 'keypoints','bbox'
        self.maps_def_max = maps_def_max

        assert os.path.exists(path_save_weight), 'path_save_weight 不存在 %s' % path_save_weight
        self.save_weight_name = save_weight_name
        self.path_save_weight = path_save_weight
        self.print_freq = print_freq

        if is_writer:
            from torch.utils.tensorboard import SummaryWriter
            if keep_writer:
                _dir = keep_writer
            else:
                _dir = time.strftime('%Y-%m-%d_%H_%M_%S', time.localtime(time.time()))

            _path = os.path.join(get_path_root(), 'logs', _dir)
            os.makedirs(_path, exist_ok=True)
            flog.debug('---- use tensorboard ---\ntensorboard --host=192.168.0.199 --logdir=\\\n%s\n', _path)
            self.tb_writer = SummaryWriter(_path)
        else:
            self.tb_writer = None

        self.ema_model = None  # 在训练中赋值

    def frun(self, start_epoch):

        if self.cfg.IS_EMA and self.model is not None and self.dataloader_train is not None:
            self.ema_model = ModelEMA(self.model, 0.9998)
            # 开始 * max_iter数
            self.ema_model.updates = int(start_epoch * len(self.dataloader_train) / self.cfg.FORWARD_COUNT)

        restart = True  # 重新运行的判断
        for epoch in range(start_epoch, self.end_epoch + 1, 1):  # 从1开始
            save_val = None
            ''' ------------------- 训练代码  --------------------- '''
            if self.dataloader_train is not None and self.cfg.IS_TRAIN:
                if self.model is not None:
                    self.model.train()
                    if self.cfg.NUMS_LOCK_WEIGHT_DICT is not None:

                        if restart:
                            n_time = len(self.cfg.NUMS_LOCK_WEIGHT_DICT[::-1])
                            for s in self.cfg.NUMS_LOCK_WEIGHT_DICT[::-1]:
                                if epoch >= s:
                                    self.cfg.FUN_LOCK(self.model, n_time)
                                else:
                                    n_time -= 1
                            restart = False  # 执行完成关闭
                        else:
                            _mask = self.cfg.NUMS_LOCK_WEIGHT_DICT == epoch  # 这里只用结果的第一个
                            if _mask.any():
                                self.cfg.FUN_LOCK(self.model, np.where(_mask)[0][0] + 1)

                t0_test = time.time()
                loss_val_obj = self.ftrain(dataloader_train=self.dataloader_train,
                                           optimizer=self.optimizer, lr_scheduler=self.lr_scheduler,
                                           epoch=epoch, end_epoch=self.end_epoch,
                                           fun_loss=self.fun_loss, model=self.model,
                                           lr_val_base=self.lr_val_base, tb_writer=self.tb_writer,
                                           is_mixture_fit=self.is_mixture_fit, print_freq=self.print_freq,
                                           forward_count=self.cfg.FORWARD_COUNT,
                                           is_warmup=self.cfg.IS_WARMUP, num_warmup=self.cfg.NUM_WARMUP,
                                           ema_model=self.ema_model,
                                           )
                save_val = loss_val_obj.avg

                if self.cfg.IS_EMA:
                    self.ema_model.update_attr(model=self.model)

                print(' ----- 训练用时 %s ----- \n\n' % str(datetime.timedelta(seconds=int(time.time() - t0_test))))

            if self.dataloader_train is not None \
                    and self.is_open(epoch, self.cfg.NUM_WEIGHT_SAVE_DICT):
                print('训练完成正在保存模型...')
                save_weight(
                    path_save=self.path_save_weight,
                    model=self.model,
                    name=self.save_weight_name,
                    loss=save_val,  # 这个正常是一样的有的
                    optimizer=self.optimizer,
                    lr_scheduler=self.lr_scheduler,
                    epoch=epoch,
                    ema_model=self.ema_model,
                )

            ''' ------------------- 验证代码  --------------------- '''
            # if self.dataloader_val is not None and self.cfg.IS_VAL and self.is_open(epoch, self.cfg.NUMS_VAL_DICT):
            #     t0_test = time.time()
            #     loss_val_obj = self.fval(dataloader_val=self.dataloader_val,
            #                              epoch=epoch, end_epoch=self.end_epoch,
            #                              fun_loss=self.fun_loss, model=self.model,
            #                              tb_writer=self.tb_writer, print_freq=self.print_freq
            #                              )
            #     print(' ----- 验证用时 %s ----- \n\n' % str(datetime.timedelta(seconds=int(time.time() - t0_test))))

            ''' ------------------- 测试代码  --------------------- '''
            if self.dataloader_test is not None and self.is_open(epoch, self.cfg.NUMS_TEST_DICT):

                if self.cfg.IS_TEST is None and self.cfg.IS_VAL is None:
                    flog.warning('cfg.IS_TEST,cfg.IS_VAL 均为空')
                    return

                t0_test = time.time()
                maps_val = self.ftest(model=self.model,
                                      dataloader_test=self.dataloader_test,
                                      epoch=epoch, is_vis_all=self.cfg.IS_VISUAL, mode_vis=self.mode_vis,
                                      num_vis_z=self.num_vis_z, tb_writer=self.tb_writer, is_test=self.cfg.IS_TEST,
                                      is_val=self.cfg.IS_VAL, end_epoch=self.end_epoch, print_freq=self.print_freq,
                                      )

                torch.cuda.empty_cache()

                if maps_val is not None and self.maps_def_max is not None:
                    # 更新 self.maps_def_max 值
                    if maps_val[0] > self.maps_def_max[0]:
                        self.maps_def_max[0] = maps_val[0]
                        self.maps_def_max[1] = max(self.maps_def_max[1], maps_val[1])
                    elif maps_val[1] > self.maps_def_max[1]:
                        self.maps_def_max[0] = max(self.maps_def_max[0], maps_val[0])
                        self.maps_def_max[1] = maps_val[1]
                    else:
                        print(' ----- 测试总用时 %s ----- \n\n'
                              % str(datetime.timedelta(seconds=int(time.time() - t0_test))))
                        continue
                    save_weight(
                        path_save=self.path_save_weight,
                        model=self.model,
                        name=self.save_weight_name,
                        loss=save_val,  # 这个正常是一样的有的
                        optimizer=self.optimizer,
                        lr_scheduler=self.lr_scheduler,
                        epoch=epoch,
                        maps_val=maps_val,
                    )
                print(' ----- 测试总用时 %s ----- \n\n' % str(datetime.timedelta(seconds=int(time.time() - t0_test))))

    def fval(self, dataloader_val, epoch, end_epoch,
             model=None, fun_loss=None,
             print_freq=1, tb_writer=None,
             ):
        # 这个在 epoch 中
        loss_val_obj = SmoothedValue()
        print('\n-------------------- 验证 fval 开始 %s -------------------------' % epoch)
        epoch_size = len(dataloader_val)
        batch = dataloader_val.batch_size
        titel_tb_writer = 'loss_iter_val:(batch = %d，epoch_size = %d)' % (batch, epoch_size)

        t0 = time.time()
        for i, datas_batch in enumerate(dataloader_val):
            t1 = time.time()

            with torch.no_grad():
                if fun_loss is not None:
                    # 这里是回调
                    loss_total, log_dict = fun_loss(datas_batch)
                else:
                    loss_total, log_dict = model(datas_batch)

            loss_val_obj.update(loss_total.item())

            if i % print_freq == 0:
                self.print_log(end_epoch=end_epoch, epoch=epoch,
                               epoch_size=epoch_size, iter_i=i, log_dict=log_dict,
                               l_val=loss_val_obj.value, l_avg=loss_val_obj.avg,
                               t0=t0, t1=t1, title='val',
                               device=model.fdevice,
                               )

            if tb_writer is not None:
                self.tb_writing4tv(tb_writer=tb_writer, log_dict=log_dict,
                                   iter_i=epoch_size * (epoch - 1) + i + 1,
                                   title=titel_tb_writer, lr=None)

            # 更新时间用于获取 data 时间
            t0 = time.time()

        return loss_val_obj

    def ftrain(self, dataloader_train, optimizer, epoch, end_epoch, lr_scheduler=None,
               fun_loss=None, model=None, fun_datas_l2=None,
               lr_val_base=1e-3, tb_writer=None,
               is_mixture_fit=False, print_freq=1, forward_count=1,
               is_warmup=True, num_warmup=2, ema_model=None):
        # 这个在 epoch 中
        loss_val_obj = SmoothedValue()
        print('-------------------- 训练 ftrain 开始 %s -------------------------' % epoch)
        epoch_size = len(dataloader_train)
        batch = dataloader_train.batch_size
        title_tb_writer = 'loss_iter_train:(batch = %d，epoch_size = %d)' % (batch, epoch_size)

        scaler = GradScaler(enabled=is_mixture_fit)

        t0 = time.time()
        for i, datas_batch in enumerate(dataloader_train):
            # 这里输出的是CPU 数据 dataloader 之前是多进程使用CPU兼容性好 这里需要转换
            if epoch < num_warmup and is_warmup:
                now_lr = lr_val_base * pow((i + epoch * epoch_size) * 1. / (num_warmup * epoch_size), 4)
                self.update_lr(optimizer, now_lr)
            elif epoch == num_warmup:
                self.update_lr(optimizer, lr_val_base)

            with autocast(enabled=is_mixture_fit):
                if fun_loss is not None:
                    # 这里是回调 多返回一个 数据时间
                    loss_total, log_dict, t1 = fun_loss(datas_batch)
                else:
                    # datas_batch = fun_datas_l2(datas_batch, model.fdevice)
                    t1 = time.time()  # 前置任务完成, 数据及初始化
                    loss_total, log_dict = model(datas_batch)

                if not math.isfinite(loss_total):  # 当计算的损失为无穷大时停止训练
                    flog.critical("Loss is {}, stopping training".format(loss_total))
                    flog.critical(log_dict)
                    sys.exit(1)
                loss_total *= 1. / forward_count

            loss_val_obj.update(loss_total.item())

            scaler.scale(loss_total).backward()

            if ((i + 1) % forward_count) == 0:
                scaler.step(optimizer)
                scaler.update()
                if ema_model is not None:
                    ema_model.update(model)
                optimizer.zero_grad()

            if i % print_freq == 0:
                self.print_log(end_epoch=end_epoch, epoch=epoch,
                               epoch_size=epoch_size, iter_i=i, log_dict=log_dict,
                               l_val=loss_val_obj.value, l_avg=loss_val_obj.avg,
                               lr=optimizer.param_groups[0]['lr'],
                               t0=t0, t1=t1, title='train',
                               device=model.fdevice, )
                pass

            if tb_writer is not None:
                self.tb_writing4tv(tb_writer=tb_writer, log_dict=log_dict,
                                   iter_i=epoch_size * (epoch - 1) + i + 1,
                                   title=title_tb_writer,
                                   lr=optimizer.param_groups[0]['lr'])
                pass

            # 更新时间用于获取 data 时间
            t0 = time.time()

        if lr_scheduler is not None:  # 这个必须与梯度代码在一个地方
            lr_scheduler.step()  # 更新学习
        return loss_val_obj

    def ftest(self, model, dataloader_test, epoch, is_vis_all,
              mode_vis, num_vis_z, tb_writer=None, is_test=None,
              is_val=None, end_epoch=None, print_freq=None, fun_datas_l2=None, ):
        '''
        ['segm', 'bbox', 'keypoints']
        :param epoch:
        :return:
        '''
        print('-------------------- 测试 ftest 开始 %s -------------------------' % epoch)
        model.eval()
        loss_val_obj = SmoothedValue()
        batch = dataloader_test.batch_size
        epoch_size = len(dataloader_test)
        title_tb_writer = 'loss_iter_val:(batch = %d，epoch_size = %d)' % (batch, epoch_size)

        num_no_pos_z = 0  # 没发现目标的计数器
        num_pos_z_mean = []  # 正例计数
        res_z = {}  # 保存 全部的coco结果
        num_vis_now = 0  # 已可视化的临时值
        ids_data_all = []  # dataloader_test 的所有图片ID

        # with torch.no_grad() 这个由模型处理
        # pbar = tqdm(dataloader_test, desc='%s' % epoch, postfix=dict, mininterval=0.1)
        # for datas_batch in pbar:
        t0 = time.time()
        for i, datas_batch in enumerate(dataloader_test):
            t1 = time.time()
            # 由模型 FModelBase 处理数据后输出 返回的已进行完整归一化
            reses, imgs_ts_4d, targets, off_ltrb_ts, loss_total, log_dict = model(datas_batch)

            if is_val is not None and is_val:
                # 只要 is_val loss_val_obj 才有效
                loss_val_obj.update(loss_total.item())
                if tb_writer is not None:
                    self.tb_writing4tv(tb_writer=tb_writer, log_dict=log_dict,
                                       iter_i=epoch_size * (epoch - 1) + i + 1,
                                       title=title_tb_writer, lr=None)

            if is_test is None or not is_test:
                # 如果没有test则 就在这里完结
                if i % print_freq == 0:
                    self.print_log(end_epoch=end_epoch, epoch=epoch,
                                   epoch_size=epoch_size, iter_i=i, log_dict=log_dict,
                                   l_val=loss_val_obj.value, l_avg=loss_val_obj.avg,
                                   t0=t0, t1=t1, title='val',
                                   device=model.fdevice, )
                t0 = time.time()
                continue

            # 这里输出的都是归一化尺寸
            ids_batch, p_ltrbs, p_kps, p_labels, p_scores = reses
            ''' 整批没有目标 提示和处理 '''
            if p_labels is None or len(p_labels) == 0:
                num_no_pos_z += batch
                # flog.info('本批没有目标 当前共有: %s 张图片未检出', num_no_pos_z)
                # if num_no_pos > 3:  # 如果3个批都没有目标则放弃
                #     return
                # else:  # 没有目标就下一个
                #     num_no_pos += 1
                # pbar.set_description("未检出数: %s" % num_no_pos_z)
                continue

            ''' 有目标进行如下操作 提取该批真实ID及尺寸 '''
            size_wh_f_ts_batch = []  # 用于修复box
            ids_img_batch = []
            device = off_ltrb_ts.device

            for target in targets:  # 通过target 提取ID 和 size
                ids_data_all.append(target['image_id'])
                ids_img_batch.append(target['image_id'])
                size_wh_f_ts_batch.append(target['size'].clone().detach())  # tnesor
            size_wh_input_ts = torch.tensor(imgs_ts_4d.shape[-2:][::-1], device=device)

            _res_batch = {}  # 每一批的coco 结果 临时值

            _num_pos_mean = []
            scores = []
            # 每一张图的 id 与批次顺序保持一致 选出匹配
            for j, (size_wh_f_ts, image_id) in enumerate(zip(size_wh_f_ts_batch, ids_img_batch)):
                # 图片与 输出的对应
                mask = ids_batch == j  # 构建 batch 次的mask
                ''' 单张图没有目标 计数提示 '''
                if not torch.any(mask):
                    # flog.warning('没有预测出框 %s', files_txt)
                    num_no_pos_z += 1
                    scores.append(0)
                    _num_pos_mean.append(0)
                    # pbar.set_description("未检出数: %s" % num_no_pos_z)
                else:
                    ''' 已检出 是否可视化逻辑 '''
                    if is_vis_all or num_vis_now < num_vis_z:
                        num_vis_now += 1

                        self.show_pic(dataloader_test=dataloader_test,
                                      size_wh_input_ts=size_wh_input_ts.cpu(),
                                      off_ltrb_ts_f=off_ltrb_ts[j].cpu(),
                                      gltrb_f=targets[j]['boxes'].cpu(),
                                      image_id=image_id, mode_vis=mode_vis,
                                      p_labels_pos=p_labels[mask].cpu(),
                                      p_ltrbs_pos=p_ltrbs[mask].cpu(),
                                      p_scores_pos=p_scores[mask].cpu())

                    # 归一化->file尺寸  coco需要 ltwh
                    boxes_ltwh = ltrb2ltwh(p_ltrbs[mask] * size_wh_f_ts.repeat(2)[None])
                    _res_batch[image_id] = {
                        'boxes': boxes_ltwh.cpu(),  # coco loadRes 会对ltwh 转换成 ltrb
                        'labels': p_labels[mask].cpu(),
                        'scores': p_scores[mask].cpu(),
                    }
                    _num_pos_mean.append(len(boxes_ltwh))
                    scores.append(p_scores[mask].mean().item())

            # 正例判断遍历完成
            _mean = np.array(_num_pos_mean).mean()
            num_pos_z_mean.append(_mean)
            if log_dict is None:
                log_dict = {}
            log_dict['num_no_pos'] = num_no_pos_z
            log_dict['num_pos_mean'] = _mean  # 正例平均
            log_dict['scores_max'] = max(scores)  # 这个是迭代一次的
            log_dict['scores_mean'] = np.array(scores).mean()

            if len(_res_batch) > 0:  # 有检测出的目标
                res_z.update(_res_batch)  # 字典叠加

            if i % print_freq == 0:
                self.print_log(end_epoch=end_epoch, epoch=epoch,
                               epoch_size=epoch_size, iter_i=i, log_dict=log_dict,
                               l_val=loss_val_obj.value, l_avg=loss_val_obj.avg,
                               t0=t0, t1=t1, title='test&val',
                               device=model.fdevice, )
            t0 = time.time()

        if is_test is None or not is_test:
            return None

        res_coco_standard = []  # 最终的 coco 标准格式 一个ID可能 有多个目标
        # res_z 每一个ID可能有多个目标 每个目标形成一条 id对应数据
        for i, (image_id, g_target) in enumerate(res_z.items()):
            labels = g_target['labels'].type(torch.int).tolist()
            boxes_ltwh = g_target['boxes'].tolist()
            score = g_target['scores'].tolist()
            for i in range(len(labels)):
                # catid转换
                category_id = dataloader_test.dataset.classes_train2coco[labels[i]]
                res_coco_standard.append(
                    {"image_id": image_id, "category_id": category_id, "bbox": boxes_ltwh[i], "score": score[i]})

        if len(res_coco_standard) > 0:  # 有 coco 结果
            # 这个保存 AP50的结果
            maps_val, coco_eval_obj = self.run_cocoeval(dataloader_test=dataloader_test,
                                                        ids_data_all=ids_data_all,
                                                        res_coco_standard=res_coco_standard,
                                                        )
            coco_stats = coco_eval_obj.stats
        else:
            # 没有 coco 结果
            maps_val = [0, 0]
            coco_stats = None

        if tb_writer is not None:
            d = {
                'num_no_pos_z': num_no_pos_z,
                'num_pos_z_mean': np.array(num_pos_z_mean).mean() if len(num_pos_z_mean) > 0 else 0,
            }

            self.tr_writing4test(epoch=epoch, log_dict=d,
                                 tb_writer=tb_writer, coco_stats=coco_stats)

        return maps_val

    def print_log(self, end_epoch, epoch,
                  epoch_size, iter_i, log_dict, l_val, l_avg,
                  t0, t1, lr=math.nan, title='title',
                  device=torch.device('cpu')):
        '''

        :param end_epoch:
        :param epoch:
        :param epoch_size: 一个 epoch 需迭代的次数
        :param iter_i:  当前迭代次数
        :param log_dict:
        :param l_val:
        :param l_avg:
        :param lr: 当前学习率
        :param t0: 最开始的时间 这个是秒
        :param t1:  数据加载完成时间
        :param title:  标题
        :return:
        '''
        s = '[{title} {epoch}/{end_epoch}] ' \
            '[Iter {iter_i}/{iter_epoch}/{iter_z}] ' \
            '[lr: {lr:.6f}] (Loss:({val:.2f} /{avg:.2f} )|| {loss_str}) ' \
            '[time: d{data_time:.2f}/i{iter_time:.2f}/{residue_time}] {memory:.0f}'
        MB = 1024.0 * 1024.0

        show_loss_str = []
        for k, v, in log_dict.items():
            show_loss_str.append(
                "{}: {:.4f} ||".format(k, v)
            )

        iter_time = time.time() - t0
        residue_time = iter_time * (epoch_size - iter_i + 1)  # 剩余时间

        d = {
            'title': title,
            'epoch': epoch,
            'end_epoch': end_epoch,
            'iter_i': iter_i + 1,
            'iter_epoch': epoch_size,
            'iter_z': (epoch - 1) * epoch_size + iter_i + 1,
            'lr': lr,
            'val': l_val,
            'avg': l_avg,
            'loss_str': str(show_loss_str),
            'data_time': t1 - t0,  # 数据
            'iter_time': iter_time,  # 迭代时间
            'residue_time': str(datetime.timedelta(seconds=int(residue_time))),  # 剩余时间
            'memory': torch.cuda.max_memory_allocated() / MB if device.type == 'cuda' else math.nan,  # 只能取第一个显卡
        }

        print(s.format(**d))

    def update_lr(self, optimizer, now_lr):
        for param_group in optimizer.param_groups:
            param_group['lr'] = now_lr

    def is_open(self, epoch, nums_dict):
        '''
        是否开启 验证或测试
        :param epoch:
        :param nums_dict: NUMS_TEST_DICT = {2: 1, 35: 1, 50: 1}
        :return:
        '''

        #  {2: 1, 35: 1, 50: 1}  -> 2,35,50 ->  50,35,2
        s_keys = sorted(list(nums_dict), reverse=True)
        for s_key in s_keys:
            if epoch < s_key:
                continue
            else:
                eval_interval = nums_dict[s_key]
                if epoch % eval_interval != 0:
                    # 满足epoch 无需验证退出
                    break
                return True

    def run_cocoeval(self, dataloader_test, ids_data_all, res_coco_standard):
        maps_val = []
        coco_gt = dataloader_test.dataset.coco_obj
        # 第一个元素指示操作该临时文件的安全级别，第二个元素指示该临时文件的路径
        _, tmp = tempfile.mkstemp()  # 创建临时文件
        json.dump(res_coco_standard, open(tmp, 'w'))
        coco_dt = coco_gt.loadRes(tmp)
        '''
                    _summarizeDets()->_summarize() 
                        _summarizeDets 函数中调用了12次 _summarize
                        结果在 self.eval['precision'] , self.eval['recall']中 
                    '''
        coco_eval_obj = FCOCOeval(copy.deepcopy(coco_gt), copy.deepcopy(coco_dt), 'bbox')  # 这个添加了每个类别的map分
        # coco_eval_obj = COCOeval(coco_gt, coco_dt, ann_type)
        coco_eval_obj.params.imgIds = ids_data_all  # 多显卡id合并更新
        coco_eval_obj.evaluate()
        coco_eval_obj.accumulate()
        coco_stats, print_coco = coco_eval_obj.summarize()
        coco_eval_obj.stats = coco_stats
        print(print_coco)
        clses_name = list(dataloader_test.dataset.classes_ids)
        coco_eval_obj.print_clses(clses_name)
        maps_val.append(coco_eval_obj.stats[1])  # 添加ap50
        maps_val.append(coco_eval_obj.stats[7])
        return maps_val, coco_eval_obj

    def tr_writing4test(self, epoch, log_dict, tb_writer, coco_stats):
        # 一个图只有一个值
        title = 'mAP/'
        # 这个顺序关系
        for k, v, in log_dict.items():
            tb_writer.add_scalar('%s/%s' % (title, k), v, epoch)

        if coco_stats is not None:
            _d = {
                'IoU=0.50:0.95': coco_stats[0],
                'IoU=0.50': coco_stats[1],
                'IoU=0.75': coco_stats[2],
            }
            tb_writer.add_scalars(title + 'Precision_iou', _d, epoch)
            # Recall_iou
            _d = {
                'maxDets=  1': coco_stats[6],
                'maxDets= 10': coco_stats[7],
                'maxDets=100': coco_stats[8],
            }
            tb_writer.add_scalars(title + 'Recall_iou', _d, epoch)
            # 小中大
            _d = {
                'p_large': coco_stats[5],
                'r_large': coco_stats[11],
            }
            tb_writer.add_scalars(title + 'large', _d, epoch)
            _d = {
                'p_medium': coco_stats[4],
                'r_medium': coco_stats[10],
            }
            tb_writer.add_scalars(title + 'medium', _d, epoch)
            _d = {
                'p_small': coco_stats[3],
                'r_small': coco_stats[9],
            }
            tb_writer.add_scalars(title + 'small', _d, epoch)

    def tb_writing4tv(self, tb_writer, log_dict, iter_i, title, lr=None):
        # 主进程写入   不验证时写
        for k, v, in log_dict.items():
            tb_writer.add_scalar('%s/%s' % (title, k), v, iter_i)
        if lr is not None:
            tb_writer.add_scalar('%s/lr' % title, lr, iter_i)

    def show_pic(self, dataloader_test, size_wh_input_ts,
                 off_ltrb_ts_f, gltrb_f,
                 image_id, mode_vis,
                 p_labels_pos, p_ltrbs_pos, p_scores_pos):
        '''

        :param dataloader_test:
        :param size_wh_input_ts:
        :param off_ltrb_ts_f:  这个是1D [4]
        :param gltrb_f:
        :param image_id:
        :param mode_vis: 可视化模式  bbox keypoints
        :return:
        '''

        coco = dataloader_test.dataset.coco_obj
        img_info = coco.loadImgs([image_id])
        file_img = os.path.join(dataloader_test.dataset.path_img, img_info[0]['file_name'])
        img_np_file = cv2.imread(file_img)
        img_np_file = cv2.cvtColor(img_np_file, cv2.COLOR_BGR2RGB)
        # import skimage.io as io
        # h,w,c
        # img_np = io.imread(file_img)

        # p归一化
        size_wh_f_ts = torch.tensor(img_np_file.shape[:2][::-1])
        size_wh_f_ts_x2 = size_wh_f_ts.repeat(2)  # 图片真实尺寸
        p_boxes_ltrb_f = p_ltrbs_pos * size_wh_f_ts_x2

        # g归一化
        size_wh_toone_ts = size_wh_input_ts - off_ltrb_ts_f[:2] - off_ltrb_ts_f[2:]
        # 平移 [nn,4]  [4] -> [1,4]
        gltrb_ = gltrb_f - off_ltrb_ts_f.view(1, -1)
        gltrb_ = gltrb_ / size_wh_toone_ts.repeat(2).squeeze(0) * size_wh_f_ts.repeat(2).squeeze(0)

        p_texts = []
        for i, p_label in enumerate(p_labels_pos):
            name_cat = dataloader_test.dataset.ids_classes[(p_label.long()).item()]
            s = name_cat + ':' + str(round(p_scores_pos[i].item(), 2))
            p_texts.append(s)

        title_text = '%s x %s (num_pos = %s) max=%s' % (str(img_np_file.shape[1]),  # w
                                                        str(img_np_file.shape[0]),  # h
                                                        str(len(p_boxes_ltrb_f)),
                                                        str(round(p_scores_pos.max().item(), 2))
                                                        )

        if mode_vis == 'bbox':
            f_show_od_np4plt_v3(
                img_np_file, p_ltrb=p_boxes_ltrb_f,
                title=title_text,
                g_ltrb=gltrb_,
                p_texts=p_texts,
                is_recover_size=False,
            )
        elif mode_vis == 'keypoints':
            # size_wh_file_x5 = np.tile(size_wh_file, self.cfg.NUM_KEYPOINTS)  # 图片真实尺寸
            raise Exception('待完善 keypoints')
            # p_keypoints_f = p_kps_pos.cpu() * size_wh_file_x5
            # f_show_kp_np4plt(img_np_file, p_boxes_ltrb_f,
            #                  kps_xy_input=p_keypoints_f,
            #                  mask_kps=torch.ones_like(p_keypoints_f, dtype=torch.bool),
            #                  # 测试集 GT默认不归一化,是input模型尺寸
            #                  g_ltrb=target['boxes'].cpu() / size_wh_toone_ts_x2 * size_wh_file_x2,
            #                  plabels_text=p_labels_pos,
            #                  p_scores_float=p_scores_pos.tolist(),
            #                  is_recover_size=False)
        else:
            raise Exception('self.cfg.MODE_VIS = %s 错误' % self.cfg.MODE_VIS)


class SmoothedValue(object):
    """
    记录一系列统计量
    Track a series of values and provide access to smoothed values over a
    window or the global series average.
    """

    def __init__(self, window_size=20, fmt=None):
        if fmt is None:
            fmt = "{median:.4f} ({global_avg:.4f})"
        self.deque = deque(maxlen=window_size)  # deque简单理解成加强版list
        self.total = 0.0
        self.count = 0
        self.fmt = fmt

    def update(self, value, n=1):
        self.deque.append(value)
        self.count += n
        self.total += value * n

    # def synchronize_between_processes(self):
    #     """
    #     Warning: does not synchronize the deque!
    #     """
    #     if not fis_mgpu():
    #         return
    #     t = torch.tensor([self.count, self.total], dtype=torch.float64, device="cuda")
    #     dist.barrier()
    #     dist.all_reduce(t)
    #     t = t.tolist()
    #     self.count = int(t[0])
    #     self.total = t[1]

    @property
    def median(self):  # @property 是装饰器，这里可简单理解为增加median属性(只读)
        d = torch.tensor(list(self.deque))
        return d.median().item()

    @property
    def avg(self):
        if len(self.deque) == 0:
            return math.nan
        d = torch.tensor(list(self.deque), dtype=torch.float32)
        return d.mean().item()

    @property
    def global_avg(self):
        return self.total / self.count

    @property
    def max(self):
        if len(self.deque) == 0:
            return math.nan
        return max(self.deque)

    @property
    def value(self):
        if len(self.deque) == 0:
            return math.nan
        return self.deque[-1]

    def __str__(self):
        return self.fmt.format(
            median=self.median,
            avg=self.avg,
            global_avg=self.global_avg,
            max=self.max,
            value=self.value)
