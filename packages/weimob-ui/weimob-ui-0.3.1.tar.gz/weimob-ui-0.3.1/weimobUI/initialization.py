#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/7/21 11:03 上午
# @Author  : jianwei.lv

from weimobUI.projectFolder import main_folder, conf_folder, testcases_folder, report_folder
import sys

def main():
    if sys.argv[1] == '-c':
        pwd = main_folder.main_folder()
        conf_folder.conf_folder(pwd)
        conf_folder.create_settings(pwd)
        testcases_folder.testcases_folder(pwd)
        testcases_folder.create_xls_template(pwd)
        report_folder.report_folder(pwd)
    else:
        raise Exception('unkonow command')

if __name__ == '__main__':
    main()
