import random
import numpy as np
import cv2
import math
import matplotlib.pyplot as plt


def get_flip_matrix(prob=0.5):
    '''
    随机水平翻转
    :param prob: 概率
    :return:
    '''
    F = np.eye(3)
    if random.random() < prob:
        F[0, 0] = -1
    return F


def get_perspective_matrix(perspective=0):
    """

    :param perspective:
    :return:
    """
    P = np.eye(3)
    P[2, 0] = random.uniform(-perspective, perspective)  # x perspective (about y)
    P[2, 1] = random.uniform(-perspective, perspective)  # y perspective (about x)
    return P


def get_rotation_matrix(degree=0):
    """

    :param degree:
    :return:
    """
    R = np.eye(3)
    a = random.uniform(-degree, degree)
    R[:2] = cv2.getRotationMatrix2D(angle=a, center=(0, 0), scale=1)
    return R


def get_scale_matrix(ratio=(1, 1)):
    """

    :param width_ratio:
    :param height_ratio:
    """
    Scl = np.eye(3)
    scale = random.uniform(*ratio)
    Scl[0, 0] *= scale
    Scl[1, 1] *= scale
    return Scl


def get_stretch_matrix(width_ratio=(1, 1), height_ratio=(1, 1)):
    """

    :param width_ratio:
    :param height_ratio:
    """
    Str = np.eye(3)
    Str[0, 0] *= random.uniform(*width_ratio)
    Str[1, 1] *= random.uniform(*height_ratio)
    return Str


def get_shear_matrix(degree):
    """

    :param degree:
    :return:
    """
    Sh = np.eye(3)
    Sh[0, 1] = math.tan(random.uniform(-degree, degree) * math.pi / 180)  # x shear (deg)
    Sh[1, 0] = math.tan(random.uniform(-degree, degree) * math.pi / 180)  # y shear (deg)
    return Sh


def get_translate_matrix(translate, width, height):
    """

    :param translate:
    :return:
    """
    T = np.eye(3)
    T[0, 2] = random.uniform(0.5 - translate, 0.5 + translate) * width  # x translation
    T[1, 2] = random.uniform(0.5 - translate, 0.5 + translate) * height  # y translation
    return T


def get_resize_matrix(raw_shape, dst_shape, keep_ratio):
    """
    Get resize matrix for resizing raw img to input size
    :param raw_shape: (width, height) of raw image
    :param dst_shape: (width, height) of input image
    :param keep_ratio: whether keep original ratio
    :return: 3x3 Matrix
    """
    r_w, r_h = raw_shape
    d_w, d_h = dst_shape
    Rs = np.eye(3)
    if keep_ratio:
        C = np.eye(3)
        C[0, 2] = - r_w / 2
        C[1, 2] = - r_h / 2

        if r_w / r_h < d_w / d_h:
            ratio = d_h / r_h
        else:
            ratio = d_w / r_w
        Rs[0, 0] *= ratio
        Rs[1, 1] *= ratio

        T = np.eye(3)
        T[0, 2] = 0.5 * d_w
        T[1, 2] = 0.5 * d_h
        return T @ Rs @ C
    else:
        Rs[0, 0] *= d_w / r_w
        Rs[1, 1] *= d_h / r_h
        return Rs


def random_heighten(img_np, target, dst_shape, keep_ratio=True):
    h_src, w_src = img_np.shape[:2]  # shape(h,w,c)

    # center
    C = np.eye(3)
    C[0, 2] = - w_src / 2
    C[1, 2] = - h_src / 2

    # do not change the order of mat mul
    if random.randint(0, 1):
        # 随机透视0.0
        P = get_perspective_matrix()
        C = P @ C
    if random.randint(0, 1):
        # 缩放[0.6, 1.4]
        Scl = get_scale_matrix([0.6, 1.4])
        C = Scl @ C
    if False:
        # 拉伸[[1, 1], [1, 1]]
        Str = get_stretch_matrix(width_ratio=(1, 1), height_ratio=(1, 1))
        C = Str @ C
    if False:
        # 旋转没用
        R = get_rotation_matrix(degree=0)
        C = R @ C
    if False:
        # 切变没用
        Sh = get_shear_matrix(degree=0)
        C = Sh @ C
    if random.randint(0, 1):
        # 翻转0.5
        F = get_flip_matrix(prob=1.0)
        C = F @ C
    if False:
        # 随机移动
        T = get_translate_matrix(0.5, w_src, h_src)
    else:
        T = get_translate_matrix(0, w_src, h_src)
    M = T @ C
    # M = T @ Sh @ R @ Str @ P @ C
    ResizeM = get_resize_matrix((w_src, h_src), dst_shape, keep_ratio)
    M = ResizeM @ M
    img_np_new = cv2.warpPerspective(img_np, M, dsize=tuple(dst_shape))
    target['warp_matrix'] = M
    if 'boxes' in target:
        boxes = target['boxes']
        target['boxes'] = warp_boxes(boxes, M, dst_shape[0], dst_shape[1])
    if 'gt_masks' in target:
        for i, mask in enumerate(target['gt_masks']):
            target['gt_masks'][i] = cv2.warpPerspective(mask, M, dsize=tuple(dst_shape))

    return img_np_new


def warp_boxes(boxes, M, width, height):
    n = len(boxes)
    if n:
        # warp points
        xy = np.ones((n * 4, 3))
        xy[:, :2] = boxes[:, [0, 1, 2, 3, 0, 3, 2, 1]].reshape(n * 4, 2)  # x1y1, x2y2, x1y2, x2y1
        xy = xy @ M.T  # transform
        xy = (xy[:, :2] / xy[:, 2:3]).reshape(n, 8)  # rescale
        # create new boxes
        x = xy[:, [0, 2, 4, 6]]
        y = xy[:, [1, 3, 5, 7]]
        xy = np.concatenate((x.min(1), y.min(1), x.max(1), y.max(1))).reshape(4, n).T
        # clip boxes
        xy[:, [0, 2]] = xy[:, [0, 2]].clip(0, width)
        xy[:, [1, 3]] = xy[:, [1, 3]].clip(0, height)
        return xy.astype(np.float32)
    else:
        return boxes


# def warp_keypoints(keypoints, M, width, height):
#     n = len(keypoints)
#     if n:
#
#         # warp points
#         xy = np.ones((n * 4, 3))
#         xy[:, :2] = boxes[:, [0, 1, 2, 3, 0, 3, 2, 1]].reshape(n * 4, 2)  # x1y1, x2y2, x1y2, x2y1
#         xy = xy @ M.T  # transform
#         xy = (xy[:, :2] / xy[:, 2:3]).reshape(n, 8)  # rescale
#         # create new boxes
#         x = xy[:, [0, 2, 4, 6]]
#         y = xy[:, [1, 3, 5, 7]]
#         xy = np.concatenate((x.min(1), y.min(1), x.max(1), y.max(1))).reshape(4, n).T
#         # clip boxes
#         xy[:, [0, 2]] = xy[:, [0, 2]].clip(0, width)
#         xy[:, [1, 3]] = xy[:, [1, 3]].clip(0, height)
#         return xy


if __name__ == '__main__':
    file_img = r'/_test_pic/test_99.jpg'  # 650 466
    img_np = cv2.imread(file_img)  # 这个打开是hwc bgr
    img_np = cv2.cvtColor(img_np, cv2.COLOR_BGR2RGB)
    target = {}
    img_np_new = random_heighten(img_np, target, dst_shape=(320, 320))
    plt.imshow(img_np_new)
    plt.show()
    # img_np = cv2.cvtColor(img_np, cv2.COLOR_BGR2RGB)
    pass
