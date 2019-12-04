#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File : f1_aaa_test.py 
@Contact : buweiqiang@civaonline.cn
@MTime : 2019-12-03 18:52 
@Author: buweiqiang
@Version: 1.0
@Desciption: None
'''

import unittest
from common.url_builder import UrlBuilder
from conf import config
from conf.DemoProduct1 import p1_cfg


class Test(unittest.TestCase):
    def test_get_server_configuration_of_different_env(self):
        '''获取被测试服务地址：不同的环境设置获取到的值不同'''
        protocol = p1_cfg.get_teachcloud_protocol()
        host = p1_cfg.get_teachcloud_host()
        port = p1_cfg.get_teachcloud_port()

        url_builder = UrlBuilder(protocol, host, port, 'f1')
        print('ENV: {}'.format(config.ENV))
        print(url_builder.server_url)
        print(url_builder.baseurl)

    def test_get_user_configuration_of_different_env(self):
        '''获取测试账号：不同的环境设置获取到的值不同'''
        user = p1_cfg.getTeachCloudUserMoblie()
        pwd = p1_cfg.getTeachCloudPassword()
        print('ENV: {}'.format(config.ENV))
        print('user: {}, pwd: {}'.format(user, pwd))
