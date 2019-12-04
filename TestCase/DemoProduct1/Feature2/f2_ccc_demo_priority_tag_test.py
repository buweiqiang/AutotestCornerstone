#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File : f2_ccc_test.py 
@Contact : buweiqiang@civaonline.cn
@MTime : 2019-12-03 18:52 
@Author: buweiqiang
@Version: 1.0
@Desciption: None
'''

import unittest
from patch import Priority, Tag


# 演示：设置优先级和tag
class Test(unittest.TestCase):
    @Priority(4)
    @Tag('demo', 'activate')
    def test_invalid_activate_code(self):
        '''激活码不正确：非法'''
        activate_code = 'xxxxxxxxx'
        print(activate_code)
        # 模拟接口请求，获取响应
        ret = {'code': '1080', 'description': '激活码不正确！'}
        self.assertEqual('1080', ret['code'])
        self.assertEqual('激活码不正确！', ret['description'])

    @Priority(5)
    @Tag('demo', 'activate')
    def test_empty_activate_code(self):
        '''激活码不正确：为空'''
        activate_code = ''
        print(activate_code)
        # 模拟接口请求，获取响应
        ret = {'code': '1080', 'description': '激活码不正确！'}
        self.assertEqual('1080', ret['code'])
        self.assertEqual('激活码不正确！', ret['description'])

    @Tag('demo')
    @Priority(3)
    def test_dddd(self):
        print('dddd')

    @Tag('demo')
    @Tag('smoke')
    @Priority(2)
    def test_cccc(self):
        print('cccc')

    @Tag('demo', 'smoke')
    @Priority(1)
    def test_aaaa(self):
        print('aaaa')
