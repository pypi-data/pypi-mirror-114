#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import configparser
import os


config = configparser.ConfigParser()
config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'setting.ini')
config.read(config_path)


def get_setting(group, key):
    """
    用于获得全局配置文件中的参数值
    Args:
        group: ini文件中的组名称，如[Dataset]
        key: 组中的键

    Returns: (str) 参数值
    """
    return config.get(group, key)


if __name__ == '__main__':
    print(get_setting('Dataset', 'path'))
