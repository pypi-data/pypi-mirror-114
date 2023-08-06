#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/7/21 2:13 下午
# @Author  : jianwei.lv

import os
from weimobUI import prog_name

# 主目录
def main_folder():
    try:
        pwd = os.getcwd()
        project_dir = os.path.join(pwd, prog_name)
        os.mkdir(project_dir)
        return pwd
    except FileExistsError as e:
        print(e)

if __name__ == '__main__':
    main_foler()