#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/7/21 2:30 下午
# @Author  : jianwei.lv

import os

"""setting_file info"""
settings_model_path = os.path.abspath(os.path.join(os.path.dirname(__file__)))
settings_filename = 'settings.py'
settings_model_pwd = os.path.join(settings_model_path, settings_filename)

"""xls_template info"""
template_xls_path = os.path.abspath(os.path.join(os.path.dirname(__file__)))
template_xls_filename = 'template.xlsx'
template_xls_pwd = os.path.join(template_xls_path, template_xls_filename)