#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/7/21 7:26 下午
# @Author  : jianwei.lv

import os
from weimobUI import prog_name
from weimobUI.projectFolder import template_xls_filename, template_xls_path
from weimobUI.common.xlxs_handle import WR, extract

def testcases_folder(main_dir):
    os.mkdir(os.path.join(main_dir, prog_name, 'testcases'))

def create_xls_template(path):
    ex = extract(os.path.join(template_xls_path, template_xls_filename))
    ex.open_xlsx(sheet_name='Sheet1')
    ws_cell = ex.get_each_cell('A', 'L')
    cell_str = ex.get_cell_str()
    ex.close_xlsx()

    wr = WR()
    wr.get_active()
    for each_cell in ws_cell:
        for each in each_cell:
            wr.wr_xlsx(cell_str.__next__(), each.value)

    wr.save_xlsx(os.path.join(path, prog_name, 'testcases', 'template.xlsx'))
    wr.close_xlsx()