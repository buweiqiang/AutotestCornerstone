#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File : f3_ddd_test.py 
@Contact : buweiqiang@civaonline.cn
@MTime : 2019-12-03 18:53 
@Author: buweiqiang
@Version: 1.0
@Desciption: None
'''

import unittest
from patch import Priority, Tag


# 演示：跳过，失败，报错
class Test(unittest.TestCase):
    @Tag('demo')
    @Priority(2)
    def test_1111(self):
        print('1111演示出错')
        a = '3s' + 1
        print(a)

    @Tag('demo')
    @Tag('smoke')
    @Priority(2)
    def test_2222(self):
        print('2222演示失败')
        a = 1
        assert a == 2, '验证失败'

    @Tag('demo')
    @Priority(2)
    def test_3333(self):
        print('3333正常通过')

    @Tag('demo')
    @Priority(2)
    @unittest.skip('演示跳过')
    def test_44444(self):
        print('4444演示跳过')
