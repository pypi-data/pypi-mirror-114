from collections import defaultdict


class FCFG_BASE:
    # 训练验证
    IS_MIXTURE_FIT = True  # 半精度训练 *
    FORWARD_COUNT = 1  # 多次前向一次反向 *
    IS_TRAIN = True  # 开启训练 *
    IS_VAL = False  # 开启验证 *
    IS_WARMUP = True  # 是否热身 *
    NUM_WARMUP = 2  # WARMUP 的轮数  n-1 *
    IS_EMA = False  # 参数平滑 *
    NUMS_LOCK_WEIGHT_DICT = None  # 锁定权重分段训练  [1, 10] epoch 与 FUN_LOCK 匹配 必须由小到大

    IS_TEST = True  # 开启测试 *
    IS_VISUAL = False  # 可视化模式 关联训练 和测试
    MODE_VIS = 'bbox'  # 验证的 计算模式 'keypoints','bbox' 关系到 可视化 nms等 *
    NUM_VIS_Z = 3  # 测试时可视化的图片数 超过就不再可视 *

    IS_DEBUG = True  # 调试模式

    # 预测参数
    PRED_CONF_THR = 0.05  # 用于预测的阀值 *
    PRED_NMS_THR = 0.5  # 提高 conf 提高召回, 越小框越少 *
    PRED_SELECT_TOPK = 500  # 预测时topk *

    MAP_RECORD = defaultdict(lambda: [0.5, 0.5])
    MAP_RECORD.update({
        'type3': [0.739, 0.485],
        'type4': [0.5321, 0.377],  # ema p542r368
        'face5': [0.983, 0.754],
        'face98': [0.465, 0.56],
        'coco2017': [0.4, 0.4],
        'cocomin': [0.5, 0.5],
    })

    # 频率参数
    PRINT_FREQ = 1  # 打印频率 与 batch * PRINT_FREQ
    NUMS_TEST_DICT = {2: 1, 35: 1, 50: 1}  # 测试的起始和频率
    NUM_WEIGHT_SAVE_DICT = {2: 1, 35: 1, 50: 1}  # 保存频率
    MAPS_DEF_MAX = [0.6, 0.5]  # MAP的最大值 触发保存

    # 数据集
    # BATCH_TRAIN = 3
    # BATCH_VAL = 1

    # 数据增强
    IS_MULTI_SCALE = False  # 开启多尺寸训练 只要用数据增强必须有
    MULTI_SCALE_VAL = [200, 300]  # 多尺寸训练的尺寸范围

    # 其它动态参数
    PATH_SAVE_WEIGHT = ''

    def __str__(self) -> str:
        s = '---------------- CFG参数 ------------------\n'
        for name in dir(self):
            if not name.startswith('__'):
                s += ('\t' + name + ' : ' + str(getattr(self, name)) + '\n')
        return s
