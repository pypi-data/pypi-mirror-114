import os

from ftools.datas.coco.coco_api import f_look_coco_type
from ftools.datas.data_factory import fcre_dataload


class DataInfo:

    def __init__(self, dataset_name, path_root,
                 mode_train, batch_train, path_img_train, file_json_train,
                 mode_test, batch_test, path_img_test, file_json_test) -> None:
        '''

        '''
        super().__init__()
        self.dataset_name = dataset_name  # 数据集的通用名称不能区分是train 还是test
        self.path_root = path_root

        self.mode_train = mode_train
        self.batch_train = batch_train
        self.path_img_train = path_img_train
        self.file_json_train = file_json_train

        self.mode_test = mode_train if mode_test is None else mode_test
        self.batch_test = batch_train if batch_test is None else batch_test
        self.path_img_test = path_img_test
        self.file_json_test = file_json_test


def get_dataloader(cfg, data_info, transform_train, transform_test, ):
    dataloader_train, dataloader_test = None, None
    if cfg.IS_TRAIN and data_info.file_json_train is not None:
        dataloader_train = fcre_dataload(is_multi_scale=cfg.IS_MULTI_SCALE,
                                         num_workers=cfg.num_workers,
                                         mode=data_info.mode_train,
                                         batch=data_info.batch_train,
                                         file_json=data_info.file_json_train,
                                         path_img=data_info.path_img_train,
                                         transform=transform_train,
                                         name=data_info.dataset_name + '_train', )
        f_look_coco_type(dataloader_train.dataset.coco_obj,
                         ids_cats_ustom=None,
                         name=dataloader_train.dataset.name)

    if (cfg.IS_VAL or cfg.IS_TEST) and data_info.file_json_test is not None:
        dataloader_test = fcre_dataload(is_multi_scale=cfg.IS_MULTI_SCALE,
                                        num_workers=cfg.num_workers,
                                        mode=data_info.mode_test,
                                        batch=data_info.batch_test,
                                        file_json=data_info.file_json_test,
                                        path_img=data_info.path_img_test,
                                        transform=transform_test,
                                        name=data_info.dataset_name + '_test', )
        f_look_coco_type(dataloader_test.dataset.coco_obj,
                         ids_cats_ustom=None,
                         name=dataloader_test.dataset.name)
    return dataloader_train, dataloader_test


def get_data_cocomin(cfg, path_host,
                     mode_train, batch_train, transform_train,
                     mode_test=None, batch_test=None, transform_test=None
                     ):
    cfg.NUMS_VAL_DICT = {55: 3, 66: 1, 77: 1}  # 验证起始和频率
    cfg.NUMS_TEST_DICT = {1: 1, 100: 1, 200: 1}  # 测试的起始和频率
    cfg.NUM_WEIGHT_SAVE_DICT = {1: 1, 35: 1, 50: 1}
    cfg.PRINT_FREQ = 30
    cfg.VAL_FREQ = 20
    cfg.NUM_CLASSES = 80  # 这个根据数据集要改

    dataset_name = 'cocomin'
    path_root = os.path.join(path_host, '/AI/datas/coco2017')
    path_img_train = os.path.join(path_root, 'imgs/train2017_118287')
    file_json_train = os.path.join(path_root, 'annotations/instances_coco_min_train_16000.json')
    path_img_test = os.path.join(path_root, 'imgs/val2017_5000')
    file_json_test = os.path.join(path_root, 'annotations/instances_coco_min_val_3200.json')

    data_info = DataInfo(dataset_name, path_root,
                         mode_train, batch_train, path_img_train, file_json_train,
                         mode_test, batch_test, path_img_test, file_json_test)

    dataloader_train, dataloader_test = get_dataloader(
        cfg, data_info,
        transform_train, transform_test,
    )

    return data_info, dataloader_train, dataloader_test


def get_data_type3(cfg, path_host,
                   mode_train, batch_train, transform_train,
                   mode_test=None, batch_test=None, transform_test=None
                   ):
    cfg.NUMS_VAL_DICT = {55: 3, 66: 1, 77: 1}  # 验证起始和频率
    cfg.NUMS_TEST_DICT = {1: 1, 100: 1, 200: 1}  # 测试的起始和频率
    cfg.NUM_WEIGHT_SAVE_DICT = {1: 1, 35: 1, 50: 1}
    cfg.PRINT_FREQ = 8
    cfg.VAL_FREQ = 20
    cfg.NUM_CLASSES = 3

    dataset_name = 'type3'
    path_root = os.path.join(path_host, '/AI/datas/VOC2007')
    path_img_train = os.path.join(path_root, 'train/JPEGImages')
    file_json_train = os.path.join(path_root, 'coco/annotations/instances_type3_train_1066.json')
    path_img_test = os.path.join(path_root, 'val/JPEGImages')
    # instances_type3_val_413.json
    file_json_test = os.path.join(path_root, 'coco/annotations/instances_type3_test_637.json')

    data_info = DataInfo(dataset_name, path_root,
                         mode_train, batch_train, path_img_train, file_json_train,
                         mode_test, batch_test, path_img_test, file_json_test)

    dataloader_train, dataloader_test = get_dataloader(
        cfg, data_info,
        transform_train, transform_test,
    )

    return data_info, dataloader_train, dataloader_test


def get_data_type3(cfg, path_host,
                   mode_train, batch_train, transform_train,
                   mode_test=None, batch_test=None, transform_test=None
                   ):
    cfg.NUMS_VAL_DICT = {55: 3, 66: 1, 77: 1}  # 验证起始和频率
    cfg.NUMS_TEST_DICT = {20: 1, 100: 1, 200: 1}  # 测试的起始和频率
    cfg.NUM_WEIGHT_SAVE_DICT = {15: 10, 35: 1, 50: 1}  # 25轮记录
    cfg.PRINT_FREQ = 8
    cfg.NUM_CLASSES = 3  # ** 这里要改

    dataset_name = 'type3'  # ** 这里要改
    path_root = os.path.join(path_host, '/AI/datas/VOC2007')
    path_img_train = os.path.join(path_root, 'train/JPEGImages')
    file_json_train = os.path.join(path_root, 'coco/annotations/instances_type3_train_1066.json')
    path_img_test = os.path.join(path_root, 'val/JPEGImages')
    # instances_type3_val_413.json
    file_json_test = os.path.join(path_root, 'coco/annotations/instances_type3_test_637.json')

    # 这里不变
    data_info = DataInfo(dataset_name, path_root,
                         mode_train, batch_train, path_img_train, file_json_train,
                         mode_test, batch_test, path_img_test, file_json_test)

    dataloader_train, dataloader_test = get_dataloader(
        cfg, data_info,
        transform_train, transform_test,
    )

    return data_info, dataloader_train, dataloader_test


def get_data_type4(cfg, path_host,
                   mode_train, batch_train, transform_train,
                   mode_test=None, batch_test=None, transform_test=None
                   ):
    cfg.NUMS_VAL_DICT = {55: 3, 66: 1, 77: 1}  # 验证起始和频率
    cfg.NUMS_TEST_DICT = {20: 1, 100: 1, 200: 1}  # 测试的起始和频率
    cfg.NUM_WEIGHT_SAVE_DICT = {15: 10, 35: 1, 50: 1}  # 25轮记录
    cfg.PRINT_FREQ = 8
    cfg.NUM_CLASSES = 4  # ** 这里要改

    dataset_name = 'type4'  # ** 这里要改
    path_root = os.path.join(path_host, '/AI/datas/VOC2007')
    path_img_train = os.path.join(path_root, 'train/JPEGImages')
    file_json_train = os.path.join(path_root, 'coco/annotations/instances_type4_train_994.json')
    path_img_test = os.path.join(path_root, 'val/JPEGImages')
    # instances_type4_test_550.json
    file_json_test = os.path.join(path_root, 'coco/annotations/instances_type4_test_550.json')

    # 这里不变
    data_info = DataInfo(dataset_name, path_root,
                         mode_train, batch_train, path_img_train, file_json_train,
                         mode_test, batch_test, path_img_test, file_json_test)

    dataloader_train, dataloader_test = get_dataloader(
        cfg, data_info,
        transform_train, transform_test,
    )

    return data_info, dataloader_train, dataloader_test

# # class DataInfo:
# #
# #     def __init__(self, dataset_name, path_root,
# #                  mode_train, batch_train, path_img_train, file_json_train,
# #                  mode_test, batch_test, path_img_test, file_json_test) -> None:
# #         '''
# #
# #         :param dataset_name:
# #         :param path_root:
# #         :param mode_train:
# #         :param batch_train:
# #         :param path_img_train:
# #         :param file_json_train:
# #         :param mode_test:
# #         :param batch_test:
# #         :param path_img_test:
# #         :param file_json_test:
# #         '''
# #         super().__init__()
# #         self.dataset_name = dataset_name
# #         self.path_root = path_root
# #
# #         self.mode_train = mode_train
# #         self.batch_train = batch_train
# #         self.path_img_train = path_img_train
# #         self.file_json_train = file_json_train
# #
# #         self.mode_test = mode_test
# #         self.batch_test = batch_test
# #         self.path_img_test = path_img_test
# #         self.file_json_test = file_json_test
#
#
# def get_coco2017_args(cfg, path_host, num_workers,
#                       batch_train, batch_test=None,
#                       mode_train=None, mode_test=None,
#                       transform_train=None, transform_test=None,
#                       ):
#     cfg.NUMS_VAL_DICT = {55: 3, 66: 1, 77: 1}  # 验证起始和频率
#     cfg.NUMS_TEST_DICT = {1: 1, 100: 1, 200: 1}  # 测试的起始和频率
#     cfg.NUM_WEIGHT_SAVE_DICT = {1: 1, 35: 1, 50: 1}
#     cfg.PRINT_FREQ = 50
#     cfg.VAL_FREQ = 20
#     cfg.NUM_CLASSES = 80
#
#     dataset_name = 'coco2017'
#     path_root = os.path.join(path_host, '/AI/datas/coco2017')
#     assert mode_train is not None, 'mode_train必须传'
#     path_img_train = os.path.join(path_root, 'imgs/train2017_118287')
#     file_json_train = os.path.join(path_root, 'annotations/instances_train2017_117266.json')
#
#     if mode_test is None:
#         mode_test = mode_train  # bbox segm keypoints caption
#     if batch_test is None:
#         batch_test = batch_train
#     path_img_test = os.path.join(path_root, 'imgs/val2017_5000')
#     file_json_test = os.path.join(path_root, 'annotations/instances_val2017_4952.json')
#
#     reses = cre_dataloader(path_img_train=path_img_train, file_json_train=file_json_train,
#                            transform_train=transform_train, mode_train=mode_train, batch_train=batch_train,
#                            path_img_test=path_img_test, file_json_test=file_json_test,
#                            transform_test=transform_test, mode_test=mode_test, batch_test=batch_test,
#                            # ---
#                            is_train=cfg.IS_TRAIN, is_test=cfg.IS_TEST,
#                            is_multi_scale=cfg.IS_MULTI_SCALE, num_workers=num_workers)
#     return reses, dataset_name
#
#
#
#
#
# def cre_dataloader(cfg, path_host,
#                    batch_train, batch_test=None,
#                    mode_train=None, mode_test=None,
#                    transform_train=None, transform_test=None,
#                    ):
#     cfg.NUMS_VAL_DICT = {55: 3, 66: 1, 77: 1}  # 验证起始和频率
#     cfg.NUMS_TEST_DICT = {1: 1, 100: 1, 200: 1}  # 测试的起始和频率
#     cfg.NUM_WEIGHT_SAVE_DICT = {1: 1, 35: 1, 50: 1}
#     cfg.PRINT_FREQ = 8
#     cfg.VAL_FREQ = 20
#     cfg.NUM_CLASSES = 3
#
#     dataset_name = 'type3'
#     path_root = os.path.join(path_host, '/AI/datas/VOC2007')
#     path_img_train = os.path.join(path_root, 'train/JPEGImages')
#     file_json_train = os.path.join(path_root, 'coco/annotations/instances_type3_train_1066.json')
#
#     if mode_test is None:
#         mode_test = mode_train  # bbox segm keypoints caption
#     if batch_test is None:
#         batch_test = batch_train
#     path_img_test = os.path.join(path_root, 'val/JPEGImages')
#     # instances_type3_val_413.json
#     file_json_test = os.path.join(path_root, 'coco/annotations/instances_type3_test_637.json')
#
#     return reses, dataset_name
#
#
# def get_type4_args(cfg, path_host, num_workers,
#                    batch_train, batch_test=None,
#                    mode_train=None, mode_test=None,
#                    transform_train=None, transform_test=None,
#                    ):
#     cfg.NUMS_VAL_DICT = {55: 3, 66: 1, 77: 1}  # 验证起始和频率
#     cfg.NUMS_TEST_DICT = {1: 1, 100: 1, 200: 1}  # 测试的起始和频率
#     cfg.NUM_WEIGHT_SAVE_DICT = {1: 1, 35: 1, 50: 1}
#     cfg.PRINT_FREQ = 8
#     cfg.VAL_FREQ = 20
#     cfg.NUM_CLASSES = 4
#
#     dataset_name = 'type4'
#     path_root = os.path.join(path_host, '/AI/datas/VOC2007')
#     assert mode_train is not None, 'mode_train必须传'
#     path_img_train = os.path.join(path_root, 'train/JPEGImages')
#     file_json_train = os.path.join(path_root, 'coco/annotations/instances_type4_train_994.json')
#
#     if mode_test is None:
#         mode_test = mode_train  # bbox segm keypoints caption
#     if batch_test is None:
#         batch_test = batch_train
#     path_img_test = os.path.join(path_root, 'val/JPEGImages')
#     # instances_type4_test_550.json
#     file_json_test = os.path.join(path_root, 'coco/annotations/instances_type4_test_550.json')
#
#     reses = cre_dataloader(path_img_train=path_img_train, file_json_train=file_json_train,
#                            transform_train=transform_train, mode_train=mode_train, batch_train=batch_train,
#                            path_img_test=path_img_test, file_json_test=file_json_test,
#                            transform_test=transform_test, mode_test=mode_test, batch_test=batch_test,
#                            # ---
#                            is_train=cfg.IS_TRAIN, is_test=cfg.IS_TEST,
#                            is_multi_scale=cfg.IS_MULTI_SCALE, num_workers=num_workers)
#     return reses, dataset_name
#
#
# def get_face5_args(cfg, path_host, num_workers,
#                    batch_train, batch_test=None,
#                    mode_train=None, mode_test=None,
#                    transform_train=None, transform_test=None,
#                    ):
#     cfg.NUMS_VAL_DICT = {55: 3, 66: 1, 77: 1}  # 验证起始和频率
#     cfg.NUMS_TEST_DICT = {1: 1, 100: 1, 200: 1}  # 测试的起始和频率
#     cfg.NUM_WEIGHT_SAVE_DICT = {1: 1, 35: 1, 50: 1}
#     cfg.PRINT_FREQ = 30
#     cfg.VAL_FREQ = 20
#     cfg.NUM_CLASSES = 1
#
#     dataset_name = 'face5'
#     path_root = os.path.join(path_host, '/AI/datas/face_5')
#     assert mode_train is not None, 'mode_train必须传'
#     path_img_train = os.path.join(path_root, 'images_13466')
#     file_json_train = os.path.join(path_root, 'annotations/keypoints_train_10000_10000.json')
#
#     if mode_test is None:
#         mode_test = mode_train  # bbox segm keypoints caption
#     if batch_test is None:
#         batch_test = batch_train
#     path_img_test = path_img_train
#     file_json_test = os.path.join(path_root, 'annotations/keypoints_test_3466_3466.json')
#
#     reses = cre_dataloader(path_img_train=path_img_train, file_json_train=file_json_train,
#                            transform_train=transform_train, mode_train=mode_train, batch_train=batch_train,
#                            path_img_test=path_img_test, file_json_test=file_json_test,
#                            transform_test=transform_test, mode_test=mode_test, batch_test=batch_test,
#                            # ---
#                            is_train=cfg.IS_TRAIN, is_test=cfg.IS_TEST,
#                            is_multi_scale=cfg.IS_MULTI_SCALE, num_workers=num_workers)
#     return reses, dataset_name
#
#
# def get_face98_args(cfg, path_host, num_workers,
#                     batch_train, batch_test=None,
#                     mode_train=None, mode_test=None,
#                     transform_train=None, transform_test=None,
#                     ):
#     cfg.NUMS_VAL_DICT = {55: 3, 66: 1, 77: 1}  # 验证起始和频率
#     cfg.NUMS_TEST_DICT = {1: 1, 100: 1, 200: 1}  # 测试的起始和频率
#     cfg.NUM_WEIGHT_SAVE_DICT = {1: 1, 35: 1, 50: 1}
#     cfg.PRINT_FREQ = 15
#     cfg.VAL_FREQ = 20
#     cfg.NUM_CLASSES = 1
#
#     dataset_name = 'face98'
#     path_root = os.path.join(path_host, '/AI/datas/face_98')
#     assert mode_train is not None, 'mode_train必须传'
#     path_img_train = os.path.join(path_root, 'images_train_5316')
#     file_json_train = os.path.join(path_root, 'annotations/keypoints_train_7500_5316.json')
#
#     if mode_test is None:
#         mode_test = mode_train  # bbox segm keypoints caption
#     if batch_test is None:
#         batch_test = batch_train
#     path_img_test = os.path.join(path_root, 'images_test_2118')
#     file_json_test = os.path.join(path_root, 'annotations/keypoints_test_2500_2118.json')
#
#     reses = cre_dataloader(path_img_train=path_img_train, file_json_train=file_json_train,
#                            transform_train=transform_train, mode_train=mode_train, batch_train=batch_train,
#                            path_img_test=path_img_test, file_json_test=file_json_test,
#                            transform_test=transform_test, mode_test=mode_test, batch_test=batch_test,
#                            # ---
#                            is_train=cfg.IS_TRAIN, is_test=cfg.IS_TEST,
#                            is_multi_scale=cfg.IS_MULTI_SCALE, num_workers=num_workers)
#     return reses, dataset_name
