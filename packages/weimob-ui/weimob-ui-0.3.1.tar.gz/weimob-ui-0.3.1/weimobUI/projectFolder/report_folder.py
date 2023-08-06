#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/7/24 7:41 下午
# @Author  : jianwei.lv

import os
from weimobUI import prog_name

def report_folder(main_dir):
    print("creating report_folder.......")
    os.mkdir(os.path.join(main_dir, prog_name, 'report'))
    print("create report_folder success.!")
