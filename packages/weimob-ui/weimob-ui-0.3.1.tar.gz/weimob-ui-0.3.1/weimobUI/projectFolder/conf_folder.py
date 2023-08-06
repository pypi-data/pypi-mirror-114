#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/7/21 2:21 下午
# @Author  : jianwei.lv

import os
from weimobUI import prog_name
from weimobUI.projectFolder import settings_filename, settings_model_pwd

# 配置文件目录
def conf_folder(main_pwd):
    conf_dir = os.path.join(main_pwd, prog_name, 'Conf')
    os.mkdir(conf_dir)
    return conf_dir

def create_settings(main_pwd):
    with open(settings_model_pwd, 'r', encoding='utf-8') as f:
        text = f.read()

    with open(os.path.join(main_pwd, prog_name, settings_filename), 'w', encoding='utf-8') as f:
        f.write(text)
    print('文件创建成功')