import os
import time

import cv2
import torch
from pycocotools.coco import COCO
from torch.utils.data import Dataset
import numpy as np

from ftools.GLOBAL_LOG import flog

from ftools.f_general import fshow_time
from ftools.picture.f_show import f_show_od_ts4plt_v3


class CustomCocoDataset(Dataset):
    '''
    v 20210718
    v 20210726 更新为所选类型 s_ids_cats
    '''

    def __init__(self, file_json, path_img, mode, transform=None, is_debug=False,
                 s_ids_cats=None, nums_cat=None, is_ts_all=True,
                 image_size=None, mode_balance_data=None, name='fname'):
        '''

        :param cfg:
        :param mode:  bbox segm keypoints caption
        :param s_ids_cats:  指定类别 或数据集的类别ID
        :param nums_cat:  限制类别的最大数量
        :param is_ts_all:  默认全部转TS
        :param image_size:
        :param mode_balance_data: 这个优先冲突于 s_ids_cats  数据类别平衡方法
            'max': 4舍五入倍数整体复制  确保类别尽量一致
            'min': 取最少的类型数,多的随机选
            None: 不处理
            int 指定数据数量
        :param name: dataset 标注
        '''
        # assert cfg is not None, 'CustomCocoDataset  cfg 不能为空'
        self.image_size = image_size

        self.file_json = file_json
        self.transform = transform
        self.mode = mode
        self.coco_obj = COCO(file_json)
        # self.device = device  # 不能扩 use CUDA with multiprocessing

        self.name = name
        self.is_ts_all = is_ts_all

        # f_look_coco_type(self.coco_obj, ids_cats_ustom=None)
        print('创建dataset-----', name)

        self.s_ids_cats = []  # 初始化一下
        if mode_balance_data is not None:
            cats = self.coco_obj.getCatIds()
            num_class = len(cats)
            _t_ids = []
            _t_len = np.zeros(num_class)
            for i, cat in enumerate(cats):
                ids = self.coco_obj.getImgIds(catIds=cat)
                _t_ids.append(ids)
                _t_len[i] = len(ids)

            self.ids_img = []

            if mode_balance_data == 'max':
                num_repeats = np.around((_t_len.max() / _t_len)).astype(np.int)
                for i in range(num_class):
                    self.ids_img.extend(np.tile(np.array(_t_ids[i]), num_repeats[i]).tolist())
            elif mode_balance_data == 'min':
                len_min = _t_len.min().astype(np.int)
                # flog.debug('_t_len = %s', _t_len)
                for i in range(num_class):
                    self.ids_img.extend(np.random.choice(_t_ids[i], len_min).tolist())
            elif isinstance(mode_balance_data, int):
                for cat_id in cats:
                    # 每一类的ID
                    ids_ = self.coco_obj.getImgIds(catIds=[cat_id])
                    if len(ids_) > 0:
                        self.s_ids_cats.append(cat_id)
                    self.ids_img.extend(np.random.choice(ids_, mode_balance_data).tolist())

        else:
            # 与 mode_balance_data 冲突
            if s_ids_cats is not None:
                flog.warning('指定coco类型 %s', self.coco_obj.loadCats(s_ids_cats))
                self.s_ids_cats = s_ids_cats
                ids_img = []

                # 限制每类的最大个数
                if nums_cat is None:
                    for idc in zip(s_ids_cats):
                        # 类型对应哪些文件 可能是一张图片多个类型
                        ids_ = self.coco_obj.getImgIds(catIds=idc)
                        ids_img += ids_
                else:
                    # 限制每类的最大个数
                    for idc, num_cat in zip(s_ids_cats, nums_cat):
                        # 类型对应哪些文件 可能是一张图片多个类型
                        ids_ = self.coco_obj.getImgIds(catIds=idc)[:num_cat]
                        # ids_ = self.coco.getImgIds(catIds=idc)[:1000]
                        ids_img += ids_
                        # print(ids_)  # 这个只支持单个元素

                self.ids_img = list(set(ids_img))  # 去重
            else:
                # 所有类别所有图片
                self.s_ids_cats = self.coco_obj.getCatIds()
                self.ids_img = self.coco_obj.getImgIds()  # 所有图片的id 画图数量

        #  创建 coco 类别映射
        self._init_load_classes(self.s_ids_cats)  # 除了coco数据集,其它不管

        self.is_debug = is_debug
        self.path_img = path_img
        if not os.path.exists(path_img):
            raise Exception('coco path_img 路径不存在', path_img)

    def __len__(self):
        return len(self.ids_img)

    def open_img_tar(self, id_img):
        img = self.load_image(id_img)

        # bboxs, labels,keypoints
        tars_ = self.load_anns(id_img, img_wh=img.shape[:2][::-1])
        if tars_ is None:  # 没有标注返回空
            return None

        # 动态构造target
        target = {}
        l_ = ['boxes', 'labels', 'keypoints', 'kps_mask']
        target['image_id'] = id_img
        target['size'] = np.array(img.shape[:2][::-1])  # (w,h)

        # 根据标注模式 及字段自动添加 target['boxes', 'labels', 'keypoints']
        for i, tar in enumerate(tars_):
            target[l_[i]] = tar
        return img, target

    def __getitem__(self, index):
        '''

        :param index:
        :return: tensor or np.array 根据 out: 默认ts or other is np
            img: h,w,c
            target:
            coco原装是 ltwh
            dict{
                image_id: int,
                bboxs: ts n4 原图 ltwh -> ltrb
                labels: ts n,
                keypoints: ts n,10
                size: wh
            }
        '''
        # 这里生成的是原图尺寸的 target 和img_np_uint8 (375, 500, 3)
        id_img = self.ids_img[index]
        res = self.open_img_tar(id_img)

        if res is None:
            # print('这个图片没有标注信息 id为 %s ,继续下一个', id_img)
            # 这里预测可以控制下逻辑
            return self.__getitem__(index + 1)

        img, target = res

        _text_base = '!!! 数据有问题 %s  %s %s %s '
        assert len(target['boxes']) == len(target['labels']), \
            _text_base % ('transform前', target, len(target['boxes']), len(target['labels']))

        if target['boxes'].shape[0] == 0:
            flog.warning('数据有问题 重新加载 %s', id_img)
            return self.__getitem__(index + 1)

        # 以上img 确定是np格式(transform后出来一般是ts); target 全部是np 除imgid
        if self.transform is not None:
            img, target = self.transform(img, target)

            # debug
            # f_show_od_ts4plt_v3(
            #     img,
            #     target['boxes'],
            #     is_normal=True,
            # )

        # 这里img输出 ts_3d
        if self.is_ts_all:
            target['boxes'] = torch.tensor(target['boxes'], dtype=torch.float)
            target['labels'] = torch.tensor(target['labels'], dtype=torch.int64)
            target['size'] = torch.tensor(target['size'], dtype=torch.float)  # file尺寸

        assert len(target['boxes']) == len(target['labels']), \
            _text_base % ('transform后', target, len(target['boxes']), len(target['labels']))
        # 每个图片对应的target数量是不一致的 所以需要用target封装
        return img, target

    def load_image(self, id_img):
        '''

        :param id_img:
        :return:
        '''
        image_info = self.coco_obj.loadImgs(id_img)[0]
        file_img = os. \
            path.join(self.path_img, image_info['file_name'])
        if not os.path.exists(file_img):
            raise Exception('file_img 加载图片路径错误', file_img)

        img = cv2.imread(file_img)
        return img

    def load_anns(self, id_img, img_wh):
        '''
        ltwh --> ltrb
        :param id_img:
        :return:
            bboxs: np(num_anns, 4)
            labels: np(num_anns)
        '''
        # annotation_ids = self.coco.getAnnIds(self.image_ids[index], iscrowd=False)
        annotation_ids = self.coco_obj.getAnnIds(id_img)  # ann的id
        # anns is num_anns x 4, (x1, x2, y1, y2)
        bboxs_np = np.zeros((0, 4), dtype=np.float32)  # np创建 空数组 高级
        labels = []
        if len(annotation_ids) == 0:
            return None

        coco_anns = self.coco_obj.loadAnns(annotation_ids)
        for ann in coco_anns:
            x, y, box_w, box_h = ann['bbox']  # ltwh
            # 修正超范围的框  得 ltrb
            x1 = max(0, x)  # 修正lt最小为0 左上必须在图中
            y1 = max(0, y)
            x2 = min(img_wh[0] - 1, x1 + max(0, box_w - 1))  # 右下必须在图中
            y2 = min(img_wh[1] - 1, y1 + max(0, box_h - 1))
            ''' bbox校验 '''
            if ann['area'] > 0 and x2 > x1 and y2 >= y1:
                bbox = np.array([[x1, y1, x2, y2]], dtype=np.float32)
                # bbox[0, :4] = ann['bbox']
                # ann['bbox'] = [x1, y1, x2, y2]  # 这样写回有BUG 共享内存会修改
            else:
                flog.error('标记框有问题 %s 跳过', ann)
                continue

            # 全部通过后添加
            bboxs_np = np.append(bboxs_np, bbox, axis=0)
            labels.append(self.classes_coco2train[ann['category_id']])

        # 转NP
        labels = np.array(labels, dtype=np.float32)

        # bboxs = ltwh2ltrb(bboxs) # 前面 已转
        if bboxs_np.shape[0] == 0:
            flog.error('这图标注 不存在 %s', coco_anns)
            return None
            # raise Exception('这图标注 不存在 %s', coco_anns)

        # 这里转tensor
        if self.mode == 'bbox':
            return [bboxs_np, labels]
        elif self.mode == 'keypoints':
            pass

    def _init_load_classes(self, ids_cat):
        '''
        self.classes_ids :  {'Parade': 1}
        self.ids_classes :  {1: 'Parade'}
        self.ids_new_old {1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 6, 7: 7, 8: 8, 9: 9, 10: 10, 11: 11, 12: 12, 13: 13, 14: 14, 15: 15, 16: 16, 17: 17, 18: 18, 19: 19, 20: 20}
        self.ids_old_new {1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 6, 7: 7, 8: 8, 9: 9, 10: 10, 11: 11, 12: 12, 13: 13, 14: 14, 15: 15, 16: 16, 17: 17, 18: 18, 19: 19, 20: 20}
        :return:
        '''
        # [{'id': 1, 'name': 'aeroplane'}, {'id': 2, 'name': 'bicycle'}, {'id': 3, 'name': 'bird'}, {'id': 4, 'name': 'boat'}, {'id': 5, 'name': 'bottle'}, {'id': 6, 'name': 'bus'}, {'id': 7, 'name': 'car'}, {'id': 8, 'name': 'cat'}, {'id': 9, 'name': 'chair'}, {'id': 10, 'name': 'cow'}, {'id': 11, 'name': 'diningtable'}, {'id': 12, 'name': 'dog'}, {'id': 13, 'name': 'horse'}, {'id': 14, 'name': 'motorbike'}, {'id': 15, 'name': 'person'}, {'id': 16, 'name': 'pottedplant'}, {'id': 17, 'name': 'sheep'}, {'id': 18, 'name': 'sofa'}, {'id': 19, 'name': 'train'}, {'id': 20, 'name': 'tvmonitor'}]
        categories = self.coco_obj.loadCats(ids_cat)
        categories.sort(key=lambda x: x['id'])  # 按id升序 [{'id': 1, 'name': 'Parade'},]

        # coco ids is not from 1, and not continue ,make a new index from 0 to 79, continuely
        # 重建index 从1-80
        # classes_ids:   {names:      new_index}
        # coco_ids:  {new_index:  coco_index}
        # coco_ids_inverse: {coco_index: new_index}

        self.classes_ids, self.classes_train2coco, self.classes_coco2train = {}, {}, {}
        self.ids_classes = {}
        # 解决中间有断格的情况
        for i, c in enumerate(categories, start=1):  # 修正从1开始
            self.classes_train2coco[i] = c['id']  # 验证时用这个
            self.classes_coco2train[c['id']] = i
            self.classes_ids[c['name']] = i  # 这个是 train 索引 {'Parade': 0,}
            self.ids_classes[i] = c['name']  # 这个是 train 索引 {0:'Parade',}
        pass


if __name__ == '__main__':
    from ftools.datas.dta_heighten.f_data_pretreatment4np import ftransform_more_train, ftransform_nanodet_train
    from ftools.datas.data_factory import CLS4collate_fn


    def t001(dataset):
        for d in dataset:
            pass


    class cfg:
        pass


    path_host = ''
    # path_root = os.path.join(path_host, '/AI/datas/VOC2012')
    # path_img = os.path.join(path_root, 'train/JPEGImages')
    # file_json = os.path.join(path_root, 'coco/annotations/instances_train_17125.json')

    path_root = os.path.join(path_host, '/AI/datas/VOC2007')
    # path_img = os.path.join(path_root, 'train/JPEGImages')
    # file_json = os.path.join(path_root, 'coco/annotations/instances_type3_train_1066.json')
    path_img = os.path.join(path_root, 'val/JPEGImages')
    file_json = os.path.join(path_root, 'coco/annotations/instances_type3_val_413.json')

    mode = 'bbox'  # bbox segm keypoints caption
    # transform = None
    transform = ftransform_nanodet_train((320, 320))

    dataset = CustomCocoDataset(
        file_json=file_json,
        path_img=path_img,
        mode=mode,
        transform=transform,
        mode_balance_data=None,
    )
    fshow_time(t001, dataset)

    dataloader = torch.utils.data.DataLoader(
        dataset,
        batch_size=32,
        num_workers=0,
        shuffle=True,
        pin_memory=True,  # 不使用虚拟内存 GPU要报错
        # drop_last=True,  # 除于batch_size余下的数据
        # collate_fn=lambda x: fun_dataloader(x, cfg),
        collate_fn=CLS4collate_fn(False),
    )
    fshow_time(t001, dataloader)

    # print(dataset[0])
    print('len(dataset)', len(dataset))
