#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File : f1_bbb_test.py 
@Contact : buweiqiang@civaonline.cn
@MTime : 2019-12-03 18:52 
@Author: buweiqiang
@Version: 1.0
@Desciption: None
'''

import unittest
from patch import TestData, Priority
from conf import config


class Test(unittest.TestCase):
    @TestData
    @Priority(1)
    def test_get_data1(self, dataobj):
        '''获取测试数据1'''
        print('ENV: {}'.format(config.ENV))
        print('index={}'.format(dataobj['index']))
        print('video_id={}'.format(dataobj['video_id']))

    @TestData
    @Priority(1)
    def test_get_data2(self, dataobj):
        '''获取测试数据2'''
        print('ENV: {}'.format(config.ENV))
        print('name=', dataobj['name'])
        print('demo=', dataobj['demo'])
