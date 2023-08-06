#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import os
import glob
import json

import numpy as np
import matplotlib.pyplot as plt


def plot_json_dir(
    json_dir,
    title='title',
    xlabel='x',
    ylabel='y',
    xticks=None,
    legend_names=None
):
    xs, ys = [], []
    labels = None
    if legend_names is None:
        pt_fns = glob.glob(os.path.join(json_dir, '*.json'))
    else:
        pt_fns = [os.path.join(json_dir, l + '.json') for l in legend_names]
    for pt_fn in pt_fns:
        with open(pt_fn, 'r') as file_obj:
            name = os.path.splitext(os.path.basename(pt_fn))[0]
            load_dict = json.load(file_obj)
            keys, values = [], []
            if xticks is None:
                for key, value in load_dict.items():
                    keys.append(key)
                    values.append(value)
            else:
                for xtick in xticks:
                    keys.append(xtick)
                    values.append(load_dict[xtick])

            x = np.arange(1, len(load_dict) + 1, 1)
            y = np.array(values)
            plt.plot(x, y, label=name)
            xs.append(x)
            ys.append(y)
            if labels is None:
                labels = keys

    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend()
    # plt.xlim(1, 12)
    # plt.ylim(0, 100)
    xs, ys = np.array(xs), np.array(ys)
    # plt.plot(xs.transpose(), ys.transpose())
    plt.xticks(xs[0], keys)
    # plt.grid(color='r', linestyle='--', linewidth=1, alpha=0.3)
    plt.show()
    print(pt_fn)
    pass


if __name__ == '__main__':
    xticks = ['stem', 'res2_1', 'res2_2', 'res2_3', 'res3_1', 'res3_2', 'res3_3', 'res3_4', 'res4_1', 'res4_2',
              'res4_3', 'res4_4', 'res4_5', 'res4_6', 'res5_1', 'res5_2', 'res5_3', 'fpn1', 'fpn2', 'fpn3', 'fpn4',
              'fpn5', 'rpn1', 'rpn2', 'rpn3', 'rpn4', 'rpn5', 'roihead1', 'roihead2', 'roihead3', 'roihead4',
              'roihead5']
    legend_names = ['bird_view', 'front_view', 'side_view', 'low_altitude', 'medium_altitude', 'high_altitude',
                    'daylight', 'night']
    plot_json_dir('/home/jario/exps/detectron2-activation-std', xticks=xticks, legend_names=None)
