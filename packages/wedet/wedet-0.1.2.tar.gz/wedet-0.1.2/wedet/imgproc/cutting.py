#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import numpy as np
import copy
# import torch


def image2squares(image, seg_size=1024, gap=100):
    """
    将输入Numpy图像(H,W,C)分割为一系列正方形子图像，返回这些子图像-和-每个子图像在输入图像的位置
    其中每个子分割图像的大小是一致的(seg_size,seg_size,C)
    Args:
        image: np.array (H,W,C), Numpy格式的输入图像
        seg_size: 分割子图像的边长
        gap: 两个分割图像之间交叉的像素值
    Return:
        List: [np.array, np.array,...], List: [[x,y,x,y],[x,y,x,y],...]
    """
    list_split_image = []
    list_position = []
    height, width, _ = image.shape
    slide = seg_size - gap

    left, up = 0, 0
    while left < width:
        if left + seg_size >= width:
            left = max(width - seg_size, 0)
        up = 0
        while up < height:
            if up + seg_size >= height:
                up = max(height - seg_size, 0)

            right = min(left + seg_size, width)
            down = min(up + seg_size, height)
            position = [left, up, right, down]
            # 深度拷贝子分割图像
            split_image = copy.deepcopy(image[up: (up + seg_size), left: (left + seg_size)])

            list_split_image.append(split_image)
            list_position.append(position)
            if up + seg_size >= height:
                break
            else:
                up = up + slide
        if left + seg_size >= width:
            break
        else:
            left = left + slide
    return list_split_image, list_position


if __name__ == '__main__':
    img = np.random.random((2323, 2324, 3))
    cut_imgs, cut_locs = image2squares(img)
    print('done!')
