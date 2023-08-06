#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import os
import json
import torch

from wedet.setting import get_setting


def saving_tensor(type_name, name, val):
    """
    保存torch.Tensor变量，但根据cake_setting.ini全局配置文件决定是否执行该操作
    Args:
        type_name: cake_setting.ini文件中的配置项，如[SavingTensor]-activation，则type_name=activation
        name: Tensor保存名称
        val: Tensor值

    Returns: None
    """
    saving = int(get_setting('SavingTensor', type_name))
    if saving:
        saving_path = get_setting('SavingTensor', '{}_path'.format(type_name))
        if os.path.splitext(name)[-1] != '.pt':
            name += '.pt'
        saving_fn = os.path.join(saving_path, name)
        torch.save(val, saving_fn)


def saving_json_dict(type_name, name, val):
    """
    保存Dict[JSON]变量，但根据cake_setting.ini全局配置文件决定是否执行该操作
    输入val的一个例子: {'a':1, 'b':2}
    Args:
        type_name: cake_setting.ini文件中的配置项，如[SavingTensor]-activation，则type_name=activation
        name: Tensor保存名称
        val: Tensor值

    Returns: None
    """
    saving = int(get_setting('SavingTensor', type_name))
    if saving:
        saving_path = get_setting('SavingTensor', '{}_path'.format(type_name))
        if os.path.splitext(name)[-1] != '.json':
            name += '.json'
        saving_fn = os.path.join(saving_path, name)
        with open(saving_fn, 'w') as file_obj:
            json.dump(val, file_obj, indent=2, sort_keys=True)


if __name__ == '__main__':
    saving_json_dict('activation', 'sayhello', {'a':1, 'b':2})
