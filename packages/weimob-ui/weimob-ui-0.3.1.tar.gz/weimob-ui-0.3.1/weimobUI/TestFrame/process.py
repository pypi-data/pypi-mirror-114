#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/7/23 3:07 下午
# @Author  : jianwei.lv

from weimobUI.actions.browser import Browser
from weimobUI.common.xlxs_handle import extract
from weimobUI.common import glo_var_controller
import os
from weimobUI.TestFrame.core import data_assert, ExSetting
import pytest
import time

"""获取settings地址"""
seetings_path = glo_var_controller.get_value('settings_abs_path')
"""通过settings获取testcases地址"""
# print('-----', seetings_path)
EXS = ExSetting(seetings_path)
testcases_file_dir = EXS.testcases_file_dir()
# testcases_file_dir = '/Users/lvjianwei/Desktop/workspace/weimob/ui-SDK/demo/0.233/weimobUI/testcases'
# print('------testcases_file_dir', testcases_file_dir)
"""组装excel列表，传入test_process批量执行，每张表是一条用例"""
xlxs_path_list = []
for root, dirs, files in os.walk(testcases_file_dir):
    for _file in files:
        xlxs_path = os.path.join(root, _file)
        xlxs_path_list.append(xlxs_path)
xlxs_path_list.sort()

@pytest.mark.parametrize('xlxs_path', xlxs_path_list, ids=xlxs_path_list)
def test_process(xlxs_path):
    ex = extract(xlxs_path)
    ws = ex.open_xlsx('Sheet')
    DS = data_assert()
    BS = Browser('Chrome')
    """A_line 操作方式"""
    A_line = ex.get_each_cell('A', 'A')
    for each in A_line:
        # 屏蔽第一行
        if each.value != '操作方法':
            line_num = str(each.row)
            """定位方式"""
            B_line = ws['B' + line_num].value
            """定位元素"""
            C_line = ws['C' + line_num].value
            """"输入内容"""
            D_line = ws['D' + line_num].value
            """断言定位方式"""
            G_line = ws['G' + line_num].value
            """断言判断"""
            H_line = ws['H' + line_num].value
            """断言定位元素"""
            I_line = ws['I' + line_num].value
            """断言预期结果"""
            J_line = ws['J' + line_num].value
            """sleeptime1"""
            E_line = ws['E' + line_num].value

            if each.value == "open":
                BS.open(D_line)
            elif each.value == "input":
                BS.Input(type=B_line, value=C_line, inputvalue=D_line)
            elif each.value == "click":
                 BS.Click(_type=B_line, value=C_line)

            else:
                # raise Exception("UnSupport value {} in A_line,please check".format(each.value))
                pass

            if E_line not in (None, ''):
                E_line = int(E_line)
                time.sleep(E_line)
            else:
                pass
            DS.main_diff(assert_type=G_line, assert_method=I_line,
                         exception_value=J_line, bs=BS, assert_judge=H_line)
            """sleeptime2"""
            K_line = ws['K' + line_num].value
            if K_line not in (None, ''):
                K_line = int(K_line)
                time.sleep(K_line)
        else:
            pass
    BS.close()

if __name__ == '__main__':
    pytest.main(['-s'])
