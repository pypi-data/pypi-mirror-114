#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import os
import glob
import torch
import time

import numpy as np


def tensor_mean_in_folder(folder):
    """
    计算指定文件夹(folder)中所有pt文件tensor的均值，并以dict形式返回，以文件名为key
    Args:
        folder(str): 指定文件夹的路径

    Returns: [Dict]
        key:pt文件名称, value:文件中tensor的均值
    """
    dict_res = {}
    for pt_fn in glob.glob(os.path.join(folder, '*.pt')):
        pt_bn = os.path.splitext(os.path.basename(pt_fn))[0]
        tensor = torch.load(pt_fn, map_location=torch.device('cpu'))
        tensor_mean = torch.mean(tensor).item()
        dict_res[pt_bn] = tensor_mean
    return dict_res


class DictMetric(object):
    """
    统计字典类型数据的均值与方差，update用来更新每次的新值
    输入:
        字典指标，如: {'l1': 0.141, 'l2': 0.253, 'l3': 0.949}
    输出:
        mean - {'l1': 0.141, 'l2': 0.253, 'l3': 0.949}
        std - {'l1': 0, 'l2': 0, 'l3': 0}
    """
    def __init__(self):
        self.metric_key_values = {}
        self.metric_key_count = {}

    def update(self, metrics):
        for key, value in metrics.items():
            if key in self.metric_key_values.keys():
                self.metric_key_values[key].append(value)
                self.metric_key_count[key] += 1
            else:
                self.metric_key_values[key] = [value]
                self.metric_key_count[key] = 1

    def mean(self):
        mean = {}
        for key, value in self.metric_key_values.items():
            assert len(value) == self.metric_key_count[key], "metric_key_count != len(key-values)"
            mean[key] = np.array(value).mean()
        return mean

    def std(self):
        std = {}
        for key, value in self.metric_key_values.items():
            assert len(value) == self.metric_key_count[key], "metric_key_count != len(key-values)"
            std[key] = np.array(value).std()
        return std


class FpsMe(object):
    """
    打印程序执行时的 FPS (Frame per Second)
    """

    def __init__(self):
        self.time_last = -1.
        self.time_cycle = 0.
        self.fps_count = 0
        self.fps_output = -1

    def spin(self):
        updated = False
        if self.time_last > 0:
            dt = time.time() - self.time_last
            self.time_cycle += dt
            self.fps_count += 1
            if self.time_cycle >= 1.:
                self.fps_output = self.fps_count
                self.time_cycle = 0.
                self.fps_count = 0
                updated = True

        self.time_last = time.time()
        return updated, self.fps_output


if __name__ == '__main__':
    a = tensor_mean_in_folder('/home/jario/exps/detectron2-activation')
    dm = DictMetric()
    dm.update(a)
    dm.update(a)
    dm.update(a)
    print(dm.mean())
    print(dm.std())
