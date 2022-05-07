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
        print('1111演示用例运行出错，注意与失败的区别')
        a = '3s' + 1
        print(a)

    @Tag('demo')
    @Tag('smoke')
    @Priority(2)
    def test_2222(self):
        print('2222演示用例结果失败，注意与出错的区别是，这里的运行是正常的，是校验结果失败')
        a = 1
        assert a == 2, '验证失败，a不等于2'

    @Tag('demo')
    @Priority(2)
    def test_3333(self):
        print('3333正常通过')
        assert 3 == 3, "验证失败，3不等于3"

    @Tag('demo')
    @Priority(2)
    @unittest.skip('演示跳过')
    def test_44444(self):
        print('4444演示跳过')

    @Tag('demo')
    @Priority(3)
    def test_55555(self):
        print('55555正常通过')
        assert 5 == 5, "验证失败，5不等于5"
