import numpy as np
import cv2
import torch
from PIL import Image, ImageDraw, ImageFont
from torchvision import transforms
import matplotlib.pyplot as plt

'''
plt 常用颜色: 'lightgreen' 'red' 'tan'
'''


def _draw_grid4plt(size, grids):
    '''

    :param size:
    :param grids:
    :return:
    '''
    # colors_ = STANDARD_COLORS[random.randint(0, len(STANDARD_COLORS) - 1)]
    colors_ = 'Pink'
    w, h = size
    xys = np.array([w, h]) / grids
    off_x = np.arange(1, grids[0])
    off_y = np.arange(1, grids[1])
    xx = off_x * xys[0]
    yy = off_y * xys[1]

    for x_ in xx:
        # 画列
        plt.plot([x_, x_], [0, h], color=colors_, linewidth=1., alpha=0.3)
    for y_ in yy:
        # 画列
        plt.plot([0, w], [y_, y_], color=colors_, linewidth=1., alpha=0.3)


def _draw_box4plt(boxes, texts=None, font_size=10, color='red', ax=None, recover_sizewh=None, linewidth=1):
    '''

    :param boxes:
    :param texts: 与 boxes 对应的 文本 list
    :param font_size:
    :param color:
    :param ax:  ax = plt.gca()
    :return:
    '''
    if recover_sizewh is not None:
        whwh = np.tile(np.array(recover_sizewh), 2)  # 整体复制 tile
        boxes = boxes * whwh

    if texts is not None:
        try:
            font = ImageFont.truetype('simhei.ttf', font_size, encoding='utf-8')  # 参数1：字体文件路径，参数2：字体大小
        except IOError:
            font = ImageFont.load_default()
        text_w, text_h = font.getsize(texts[0])
        margin = np.ceil(0.05 * text_h)

    for i, box in enumerate(boxes):
        l, t, r, b = box
        w = r - l
        h = b - t

        if ax is None:
            plt.Rectangle((l, t), w, h, color=color, fill=False, linewidth=linewidth)
        else:
            ax.add_patch(plt.Rectangle((l, t), w, h, color=color, fill=False, linewidth=linewidth))

        if texts is not None:
            if ax is None:
                plt.text(l + margin, t - text_h - margin, texts[i],
                         color="r", ha='center', va='center',
                         bbox={'facecolor': 'blue', 'alpha': 0.5, 'pad': 1})
            else:
                ax.text(l + margin, t - text_h - margin, texts[i],
                        color="r", ha='center', va='center',
                        bbox={'facecolor': 'blue', 'alpha': 0.5, 'pad': 1})

        x = l + w / 2
        y = t + h / 2
        plt.scatter(x, y, marker='x', color=color, s=40, label='First')


def f_show_od_ts4plt_v3(img_ts, g_ltrb=None, p_ltrb=None, is_recover_size=False,
                        p_texts=None, g_texts=None, is_normal=False, is_torgb=False,
                        grid_wh_np=None, title=None):
    assert isinstance(img_ts, torch.Tensor)
    # c,h,w -> h,w,c
    if is_normal:
        from ftools.datas.dta_heighten.f_data_pretreatment4np import f_recover_normalization4ts, \
            f_recover_normalization4ts_v2
        img_ts = img_ts.clone()
        img_ts = f_recover_normalization4ts_v2(img_ts)
    img_np = img_ts.cpu().numpy().astype(np.uint8).transpose((1, 2, 0))
    if is_torgb:
        img_np = cv2.cvtColor(img_np, cv2.COLOR_BGR2RGB)
    f_show_od_np4plt_v3(img_np, g_ltrb=g_ltrb, p_ltrb=p_ltrb,
                        is_recover_size=is_recover_size,
                        title=title,
                        p_texts=p_texts, g_texts=g_texts, grid_wh_np=grid_wh_np)


def f_show_od_np4plt_v3(img_np, g_ltrb=None, p_ltrb=None, other_ltrb=None, title=None,
                        is_recover_size=False, p_texts=None, g_texts=None, grid_wh_np=None,
                        ):
    img_np = _convert_uint8(img_np)
    plt.imshow(img_np)
    # plt.show()
    ax = plt.gca()

    if is_recover_size:
        recover_sizewh = img_np.shape[:2][::-1]  # npwh
    else:
        recover_sizewh = None

    if grid_wh_np is not None:
        wh = img_np.shape[:2][::-1]  # npwh
        _draw_grid4plt(wh, grid_wh_np)

    if title is not None:
        plt.title(title)
    else:
        if p_ltrb is not None:
            plt.title(
                '%s x %s (num_pos = %s)' % (str(img_np.shape[1]), str(img_np.shape[0]), str(len(p_ltrb))))
        else:
            plt.title('%s x %s ' % (str(img_np.shape[1]), str(img_np.shape[0])))

    if other_ltrb is not None:
        _draw_box4plt(other_ltrb, color='tan', ax=ax, recover_sizewh=recover_sizewh)

    if g_ltrb is not None:
        _draw_box4plt(g_ltrb, texts=g_texts, color='lightgreen', ax=ax, recover_sizewh=recover_sizewh, linewidth=3)

    if p_ltrb is not None:
        _draw_box4plt(p_ltrb, texts=p_texts, color='red', ax=ax, recover_sizewh=recover_sizewh)

    plt.show()


def draw_text_chinese4cv(img_np, text, left, top, textColor=(0, 255, 0), textSize=20):
    # 图片，添加的文字，左上角坐标，字体，字体大小，颜色，字体粗细
    # img_np = cv2.putText(img_np, text_, (0, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
    #                      (0, 255, 0), 1)
    img_pil = Image.fromarray(cv2.cvtColor(img_np, cv2.COLOR_BGR2RGB))
    # 创建一个可以在给定图像上绘图的对象
    draw = ImageDraw.Draw(img_pil)
    # 字体的格式
    fontStyle = ImageFont.truetype("font/simsun.ttc", textSize, encoding="utf-8")
    # 绘制文本
    draw.text((left, top), text, textColor, font=fontStyle)
    # 转换回OpenCV格式
    return cv2.cvtColor(np.asarray(img_pil), cv2.COLOR_RGB2BGR)
    # return img_np


# ********************   新方法在上面

def keypoint_painter(images, maps, img_h, img_w, numpy_array=False,
                     phase_gt=False, center_map=None):
    images = images.clone().cpu().data.numpy().transpose([0, 2, 3, 1])
    maps = maps.clone().cpu().data.numpy()
    if center_map is not None:
        center_map = center_map.clone().cpu().data.numpy()
    imgs_tensor = []
    if phase_gt:
        for img, map, c_map in zip(images, maps, center_map):
            img = cv2.resize(img, (img_w, img_h))
            for m in map[:14]:
                h, w = np.unravel_index(m.argmax(), m.shape)
                x = int(w * img_w / m.shape[1])
                y = int(h * img_h / m.shape[0])
                img = cv2.circle(img.copy(), (x, y), radius=1, thickness=2, color=(255, 0, 0))
            h, w = np.unravel_index(c_map.argmax(), c_map.shape)
            x = int(w * img_w / c_map.shape[1])
            y = int(h * img_h / c_map.shape[0])
            img = cv2.circle(img.copy(), (x, y), radius=1, thickness=2, color=(0, 0, 255))
            if numpy_array:
                imgs_tensor.append(img.astype(np.uint8))
            else:
                imgs_tensor.append(transforms.ToTensor()(img))
    else:

        for img, map_6 in zip(images, maps):
            img = cv2.resize(img, (img_w, img_h))
            for step_map in map_6:
                img_copy = img.copy()
                for m in step_map[:14]:
                    h, w = np.unravel_index(m.argmax(), m.shape)
                    x = int(w * img_w / m.shape[1])
                    y = int(h * img_h / m.shape[0])
                    img_copy = cv2.circle(img_copy.copy(), (x, y), radius=1, thickness=2, color=(255, 0, 0))
                if numpy_array:
                    imgs_tensor.append(img_copy.astype(np.uint8))
                else:
                    imgs_tensor.append(transforms.ToTensor()(img_copy))
    return imgs_tensor


def _convert_uint8(img_np):
    if img_np.dtype is not np.uint8:
        img_np_uint8 = img_np.copy()
        img_np_uint8 = img_np_uint8.astype(np.uint8)
    else:
        return img_np
    return img_np_uint8


def f_show_pic_np4plt(img_np):
    '''
    不支持float32
    :param pic:
    :return:
    '''
    img_np = _convert_uint8(img_np)
    plt.imshow(img_np)
    plt.show()


def f_show_pic_np4cv(img_np):
    img_np = _convert_uint8(img_np)
    cv2.imshow('Example', img_np)
    cv2.waitKey(0)


def f_show_kp_np4plt(img_np, boxes_ltrb_input, kps_xy_input, mask_kps, g_ltrb=None,
                     plabels_text=None, p_scores_float=None,
                     is_recover_size=True):
    '''

    :param img_np:
    :param boxes_ltrb_input:
    :param kps_xy_input:
    :param mask_kps:  预测时自动生成一个  torch.ones_like(p_keypoints_f, dtype=torch.bool)
    :param g_ltrb:
    :param plabels_text: [类型名称,]
    :param p_scores_float:[对应分数的list]
    :param is_recover_size:
    :return:
    '''
    img_np = _convert_uint8(img_np)

    assert isinstance(img_np, np.ndarray)
    # import matplotlib.pyplot as plt
    plt.title('%s x %s (num_pos = %s)' % (str(img_np.shape[1]), str(img_np.shape[0]), str(len(boxes_ltrb_input))))
    # plt.imshow(img_np)
    # plt.show()
    whwh = np.tile(np.array(img_np.shape[:2][::-1]), 2)  # 整体复制
    # plt.figure(whwh)  #要报错
    plt.imshow(img_np, alpha=0.7)
    current_axis = plt.gca()
    if g_ltrb is not None:
        if is_recover_size:
            g_ltrb = g_ltrb * whwh
        for box in g_ltrb:
            l, t, r, b = box
            plt_rectangle = plt.Rectangle((l, t), r - l, b - t, color='lightcyan', fill=False, linewidth=3)
            current_axis.add_patch(plt_rectangle)
            # x, y = c[:2]
            # r = 4
            # # 空心
            # # draw.arc((x - r, y - r, x + r, y + r), 0, 360, fill=color)
            # # 实心
            # draw.chord((x - r, y - r, x + r, y + r), 0, 360, fill=_color)

    for i, box_ltrb_input in enumerate(boxes_ltrb_input):
        l, t, r, b = box_ltrb_input
        # ltwh
        current_axis.add_patch(plt.Rectangle((l, t), r - l, b - t, color='green', fill=False, linewidth=2))
        _xys = kps_xy_input[i][mask_kps[i]]

        ''' 就这里不一样 与f_plt_od_np'''
        # 这个是多点连线 加参数后 marker='o' 失效,变成多点连线
        plt.scatter(_xys[::2], _xys[1::2],
                    color='r', s=3, alpha=0.5)
        # plt.plot(_xys[::2], _xys[1::2],
        #          marker='o',
        #          markerfacecolor='red',  # 点颜⾊
        #          markersize=3,  # 点⼤⼩
        #          markeredgecolor='green',  # 点边缘颜⾊
        #          markeredgewidth=2,  # 点边缘宽度
        #          )

        if plabels_text is not None:
            # labels : tensor -> int
            show_text = text = "{} : {:.3f}".format(plabels_text[i], p_scores_float[i])
            current_axis.text(l + 8, t - 10, show_text, size=8, color='white',
                              bbox={'facecolor': 'blue', 'alpha': 0.1})
    plt.show()


def f_show_cpm4input(img_np, kps_xy_input, heatmap_center_input):
    '''

    :param img_np:
    :param kps_xy_input: (14, 2)
    :param heatmap_center_input: (368, 368)
    :return:
    '''
    img_np = _convert_uint8(img_np)
    plt.imshow(img_np, alpha=0.7)
    for xy in kps_xy_input:
        plt.scatter(xy[0], xy[1], color='r', s=5, alpha=0.5)
    plt.imshow(heatmap_center_input, alpha=0.5)
    plt.show()


def f_show_cpm4t_all(img_np, kps_xy_input, heatmap_center_input, heatmap_t, size_wh_input):
    '''
    弄到input进行处理
    :param img_np:
    :param kps_xy_t: (14, 2)
    :param heatmap_center_input: (368, 368,1)
    :param heatmap_t: (46, 46, 14)
    :param size_wh_t: (46, 46, 15)
    :return:
    '''
    img_np = _convert_uint8(img_np)
    plt.imshow(img_np, alpha=1.0)
    for xy in kps_xy_input:
        plt.scatter(xy[0], xy[1], color='r', s=5, alpha=0.5)
    plt.imshow(heatmap_center_input, alpha=0.3)

    h, w, c = heatmap_t.shape
    img_heatmap_z = np.zeros((size_wh_input[1], size_wh_input[0], 1), dtype=np.uint8)
    for i in range(c):
        img_heatmap = heatmap_t[..., i][..., None]
        img_heatmap = cv2.resize(img_heatmap, size_wh_input)  # wh
        # img_heatmap = _convert_uint8(img_heatmap)
        img_heatmap_z = np.maximum(img_heatmap_z, img_heatmap[..., None])

    plt.imshow(img_heatmap_z, alpha=0.3)
    plt.show()


if __name__ == '__main__':
    file_img = r'D:\tb\tb\ai_code\fkeypoint\_test_pic\street.jpg'
    img_np_bgr = cv2.imread(file_img)
    boxes = np.array([
        [1, 1, 100, 100],
        [120, 120, 200, 200],
    ])
    gtexts = ['123', '445566']

    f_show_od_np4plt_v3(img_np_bgr, g_ltrb=boxes, g_texts=gtexts)
