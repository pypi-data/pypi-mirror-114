#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import os
import glob
import json
import re

import numpy as np
import matplotlib.pyplot as plt


def parse_detectron2_log(
    detectron2_log_fn,
    title='title',
    xlabel='x',
    ylabel='y',
):
    with open(detectron2_log_fn, 'r') as f:
        lines = f.readlines()
        results = {}
        for line in lines:
            line = line.strip()
            if '#DEB' in line:
                _index = re.findall('#DEB(.*?),', line)[0]
                _time = re.findall('\[(.*?)\]', line)[0]
                _value = line[line.rfind(' '):]
                # print(_index, _time, _value)
                if _index in results.keys():
                    results[_index].append(float(_value))
                else:
                    results[_index] = [float(_value)]
        for k in results.keys():
            print("key: {}, len: {}".format(k, len(results[k])))

        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        # plt.xlim(1, 12)
        # plt.ylim(0, 100)
        xs = [np.arange(len(results[k])) for k in results.keys()]
        ys = [results[k] for k in results.keys()]
        xs, ys = np.array(xs), np.array(ys)
        plt.plot(xs.transpose(), ys.transpose())
        plt.legend(results.keys())
        # plt.xticks(xs[0], keys)
        plt.grid(color='r', linestyle='--', linewidth=1, alpha=0.3)
        plt.show()


if __name__ == '__main__':
    log_fn = '/tmp/VisDrone-FRCNN-FPN-R50-FPNAttrAttenUNI-GN-0_5x/log.txt'
    parse_detectron2_log(log_fn)
