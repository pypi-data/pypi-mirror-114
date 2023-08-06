import datetime
import os
import random
import time

import cv2
import matplotlib
import numpy as np
import torch
from torch.backends import cudnn

from ftools.f_general import get_img_file
from ftools.fits.f_fit_tools import FitExecutor
from ftools.fits.f_predictfun import f_prod_pic, f_prod_vodeo
from ftools.fsys.fcamera import init_video


class DispatchTask:
    def __init__(self, fun_task_cfg=None) -> None:
        super().__init__()
        self.init_sys(None)
        self.fun_task_cfg = fun_task_cfg

    def init_sys(self, cfg):
        # -----------通用系统配置----------------
        # format short g, %precision=5
        torch.set_printoptions(linewidth=320, sci_mode=False, precision=5, profile='long')
        np.set_printoptions(linewidth=320, suppress=True, formatter={'float_kind': '{:11.5g}'.format})
        # 修改配置文件
        matplotlib.rcParams['font.sans-serif'] = ['SimHei']  # 设置matplotlib可以显示汉语
        matplotlib.rcParams['axes.unicode_minus'] = False
        matplotlib.rcParams['font.size'] = 11
        # matplotlib.rc('font', **{'size': 11})

        # --- pytorch 系统加速 ---
        torch.multiprocessing.set_sharing_strategy('file_system')  # 多GPU必须开 实测加速
        cv2.setNumThreads(0)  # 防止OpenCV进入多线程(使用PyTorch DataLoader)
        seed = 0
        # 随机种子
        np.random.seed(seed)
        random.seed(seed)
        # from yolo5 Speed-reproducibility tradeoff https://pytorch.org/docs/stable/notes/randomness.html
        torch.manual_seed(seed)
        if torch.cuda.is_available():
            torch.cuda.manual_seed(seed)
            torch.cuda.manual_seed_all(seed)
            cudnn.deterministic = True
            if seed == 0:  # slower, more reproducible
                cudnn.benchmark, cudnn.deterministic = False, True
            else:  # faster, less reproducible
                cudnn.benchmark, cudnn.deterministic = True, False

    def show_args(self, cfg):
        '''
        重要参数显示
        本方法 参数在 cfg 中具备较强依赖  不适合通用

        :param cfg:
        :return:
        '''
        if cfg.is_writer:
            if cfg.keep_writer is not None:
                tb_writer_info = cfg.keep_writer
            else:
                tb_writer_info = '开,随机目录'
        else:
            tb_writer_info = False

        if cfg.IS_WARMUP:
            warmup_info = cfg.NUM_WARMUP
        else:
            warmup_info = False

        if cfg.IS_MULTI_SCALE:
            size = '多尺度: ' + str(cfg.MULTI_SCALE_VAL)
        else:
            size = cfg.size_wh_input

        _text_dict = {
            'dataset_name': cfg.dataset_name,
            'tb_writer_info': tb_writer_info,
            'device': cfg.device,
            'num_vis_z': cfg.NUM_VIS_Z,
            'num_workers': cfg.num_workers,
            'path_save_weight': cfg.PATH_SAVE_WEIGHT,
            'warmup_info': warmup_info,
            'is_visual': cfg.IS_VISUAL,
            'size': size,
            'batch_train': cfg.batch_train,
            'mode_train': cfg.data_info.mode_train,
            'ema': cfg.IS_EMA,
            'maps_def_max': cfg.MAPS_DEF_MAX,
        }

        separator = '  \n'
        for k, v in _text_dict.items():
            _text_dict[k] = str(v) + separator

        # 遍历转str + 分隔

        # _text = '--- 训练类 ---\n'.format(**_text_dict)

        _text1 = '----------------- 系统类 ---------------\n' \
                 '\t 当前数据集: {dataset_name}' \
                 '\t 当前设备: {device}' \
                 '\t 权重路径: {path_save_weight}' \
                 '\t tb_writer: {tb_writer_info}' \
                 '\t num_workers: {num_workers}' \
                 '\t WARMUP: {warmup_info}' \
                 '\t IS_VISUAL: {is_visual}' \
                 '\t size: {size}' \
                 '\t 上限AP: {maps_def_max}'

        _text2 = '----------------- 训练类 -----------------\n' \
                 '\t batch:{batch_train}' \
                 '\t mode_train:{mode_train}' \
                 '\t ema:{ema}'

        _text3 = '----------------- 测试类 -----------------\n' \
                 '\t NUM_VIS_Z:{num_vis_z}'

        show_text = (_text1 + _text2 + _text3).format(**_text_dict)
        print(show_text)

    def run_train(self):
        t00 = time.time()
        cfg, start_epoch, end_epoch, model, fun_loss, \
        optimizer, lr_val_base, lr_scheduler, \
        dataloader_train, dataloader_test, \
        is_writer, save_weight_name, keep_writer = self.fun_task_cfg()

        self.show_args(cfg)

        ''' --------------- 启动 --------------------- '''
        executor = FitExecutor(cfg, model=model, fun_loss=fun_loss,
                               save_weight_name=save_weight_name,
                               path_save_weight=cfg.PATH_SAVE_WEIGHT,
                               optimizer=optimizer, dataloader_train=dataloader_train, lr_scheduler=lr_scheduler,
                               end_epoch=end_epoch, is_mixture_fit=cfg.IS_MIXTURE_FIT, lr_val_base=lr_val_base,
                               is_writer=is_writer, keep_writer=keep_writer,
                               print_freq=cfg.PRINT_FREQ,
                               dataloader_test=dataloader_test, maps_def_max=cfg.MAPS_DEF_MAX,
                               num_vis_z=cfg.NUM_VIS_Z, mode_vis=cfg.MODE_VIS,
                               )
        executor.frun(start_epoch=start_epoch)

        time_text = str(datetime.timedelta(seconds=int(time.time() - t00)))
        return time_text


class DetectTask:

    def __init__(self, mode_detect, model, data_transform, device, ids_classes,
                 path_pic=None, ) -> None:
        super().__init__()
        self.mode_detect = mode_detect
        self.model = model
        self.data_transform = data_transform
        self.device = device
        self.ids_classes = ids_classes
        self.path_pic = path_pic

    def detect(self):
        if self.mode_detect == 'pic':
            if self.path_pic is not None and os.path.exists(self.path_pic):
                if os.path.isdir(self.path_pic):
                    files_pic = get_img_file(self.path_pic)
                elif os.path.isfile(self.path_pic):
                    files_pic = [self.path_pic]
                else:
                    raise Exception('path_pic 有问题 %s' % self.path_pic)
            else:
                raise Exception('path_pic 不存在 %s' % self.path_pic)

            if len(files_pic) == 0:
                raise Exception('path_pic 路径没有图片 %s' % self.path_pic)

            for file in files_pic:
                f_prod_pic(file=file, data_transform=self.data_transform,
                           model=self.model, ids_classes=self.ids_classes, device=self.device)
                pass
        elif self.mode_detect == 'video':
            cap = init_video(det=0)
            f_prod_vodeo(cap=cap,
                         data_transform=self.data_transform,
                         model=self.model,
                         ids_classes=self.ids_classes,
                         device=self.device)
