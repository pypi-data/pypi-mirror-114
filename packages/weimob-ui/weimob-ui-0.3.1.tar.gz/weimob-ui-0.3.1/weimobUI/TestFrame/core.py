#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/7/22 10:36 上午
# @Author  : jianwei.lv

import os
from weimobUI.common import glo_var_controller
import pytest
import time

class Run(object):
    def __init__(self, settings_abs_path):
        cwd = os.path.abspath(os.path.join(os.path.dirname(__file__), 'process.py'))
        glo_var_controller._init()
        glo_var_controller.set_value('settings_abs_path', settings_abs_path)
        EXS = ExSetting(settings_abs_path)
        report_dir = EXS.report_dir()
        now_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        report_file_name = os.path.join(report_dir, 'report' + now_time + '.html')
        pytest.main(['--html=' + report_file_name, cwd])

class data_assert(object):
    def __init__(self):
        pass

    def main_diff(self, assert_type, assert_method, assert_judge, exception_value, bs):
        if assert_type not in (None, ''):
            result_value = self.get_element_diff(bs=bs, assert_type=assert_type, assert_method=assert_method)
            if assert_judge == '=':
                print('--------result_value', result_value)
                print('--------exception_value', exception_value)
                assert result_value == exception_value
            else:
                raise Exception('unsupport assert_method')
        else:
            print('pass assert')

    def get_element_diff(self, bs, assert_type, assert_method):
        if assert_type == "xpath":
            result = bs.get_element(type=assert_type, value=assert_method)
            return result

class ExSetting(object):
    def __init__(self, settings_abs_path):
        with open(settings_abs_path, 'r', encoding='utf-8') as f:
            self.lines = f.readlines()

    def testcases_file_dir(self):
        for line in self.lines:
            if 'testcases_file_dir' in line:
                # print('----1line', line)
                testcases_file_dir = eval(line.split('=', )[1])
                # print('-----2',testcases_file_dir)
                return testcases_file_dir

    def report_dir(self):
        for line in self.lines:
            if 'report_dir' in line:
                # print('----1line', line)
                report_dir = eval(line.split('=', )[1])
                # print('-----2',testcases_file_dir)
                return report_dir


if __name__ == '__main__':
    # Run('/Users/lvjianwei/Desktop/workspace/weimob/ui-SDK/sdk/weimobUI/TestFrame/process.py')

    Run('/Users/lvjianwei/Desktop/workspace/weimob/ui-SDK/sdk/weimobUI/projectFolder/settings.py')
    # print(os.path.join(os.path.dirname(__file__)))