#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File : f4_eee_test.py 
@Contact : buweiqiang@civaonline.cn
@MTime : 2019-12-03 18:53 
@Author: buweiqiang
@Version: 1.0
@Desciption: None
'''

import unittest
from conf import config
from conf.DemoProduct2 import p2_cfg
from common.url_builder import UrlBuilder
from patch import TestData, Priority, Tag
import requests


# 演示：常规测试用例
class Test(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        protocol = p2_cfg.getTeacherProtocol()
        host = p2_cfg.getTeacherHost()
        port = p2_cfg.getTeacherPort()

        cls.url_builder = UrlBuilder(protocol, host, port, 'f4')

    @Tag('common')
    @Priority(1)
    def test_common_case(self):
        print('这常规的测试用例1')
        print('ENV: {}'.format(config.ENV))
        print('step 1, 请求接口获取响应')
        print('request: {}'.format(self.url_builder.baseurl))
        ret = {'code': '0000', 'succeed': True, 'description': '请求成功'}
        print('step 2, 验证接口返回')
        self.assertEqual('0000', ret['code'], '验证失败，code不是0000')
        self.assertTrue(ret['succeed'], '验证失败，期望succeed应该为True')

    @Tag('common')
    @Priority(2)
    @TestData
    def test_common_case_with_data(self, data):
        print('常规的测试用例2')
        print('ENV: {}'.format(config.ENV))
        print('step 1, 准备请求数据')
        params = {
            'username': data['user'],
            'password': data['pwd'],
            'wd': 'test'
        }
        print('step 2, 请求接口获取响应')
        url = self.url_builder.baseurl + '/login'
        print('request: {}'.format(url))
        print('params: {}'.format(params))

        response = requests.get('http://www.baidu.com', params=params)
        print(response.status_code)
        # print(response.text)
        # ret = response.json()
        ret = {'code': '0000', 'succeed': True, 'description': '请求成功'}
        print('step 3, 验证接口返回')
        self.assertEqual('0000', ret['code'], '验证失败，code不是0000')
        self.assertTrue(ret['succeed'], '验证失败，期望succeed应该为True')
