#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/7/21 3:43 下午
# @Author  : jianwei.lv

from selenium import webdriver

class Browser():
    def __init__(self, type):
        if type == "Chrome":
            self.driver = webdriver.Chrome()
        elif type == "Firefox":
            self.driver = webdriver.Firefox()
        elif type == "IE":
            self.driver = webdriver.Ie()
        else:
            raise Exception("Unknow Browser type")

    # 打开网址
    def open(self, url):
        self.driver.get(url)

    # 前进
    def forward(self):
        self.driver.forward()

    def back(self):
        self.driver.back()

    # 退出
    def quit(self):
        self.driver.quit()

    # 鼠标点击
    def Click(self, _type, value):
        if _type == "xpath":
            self.driver.find_element_by_xpath(value).click()
        elif _type == "class_name":
            self.driver.find_element_by_class_name(value).click()
        elif _type == "id":
            self.driver.find_element_by_id(value).click()
        elif _type == "name":
            self.driver.find_element_by_name(value).click()
        elif _type == "link_text":
            self.driver.find_element_by_link_text(value).click()
        elif _type == "partial_link_text":
            self.driver.find_element_by_partial_link_text(value).click()
        elif _type == "css":
            self.driver.find_element_by_css_selector(value).click()
        else:
            raise Exception('Unknow click type')

    # 输入内容
    def Input(self, type, value, inputvalue):
        if type == "xpath":
            self.driver.find_element_by_xpath(value).send_keys(inputvalue)
        elif type == "class_name":
            self.driver.find_element_by_class_name(value).send_keys(inputvalue)
        elif type == "id":
            self.driver.find_element_by_id(value).send_keys(inputvalue)
        elif type == "name":
            self.driver.find_element_by_name(value).send_keys(inputvalue)
        elif type == "link_text":
            self.driver.find_element_by_link_text(value).send_keys(inputvalue)
        elif type == "partial_link_text":
            self.driver.find_element_by_partial_link_text(value).send_keys(inputvalue)
        elif type == "css":
            self.driver.find_element_by_css_selector(value).send_keys(inputvalue)
        else:
            raise Exception('Unknow input type')

    # 获取元素的值
    def get_element(self, type, value):
        if type == "xpath":
            result = self.driver.find_element_by_xpath(value).text
            return result

    #关闭浏览器
    def close(self):
        self.driver.close()

if __name__ == '__main__':
    bs = Browser('Chrome')
    bs.open('https://www.baidu.com')
