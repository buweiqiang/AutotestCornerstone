#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/5/7 14:44
# @Author  : mogui@tsign.cn
# @File    : DemoProduct1.py
# @Version : 1.0
# @Software: AutotestCornerstone


import log
from conf.config import Config

logger = log.getLogger('DemoProduct1')


class Product1Config(Config):

    def __init__(self):
        # 注意大小写一定要和文件夹名，文件名保持一致
        self.product_name = 'DemoProduct1'
        Config.__init__(self, self.product_name)

    # 获取协议
    def get_teachcloud_protocol(self):
        if not self.config.has_option('teachcloud', 'protocol'):
            return 'http'
        return self.config.get('teachcloud', 'protocol')

    # 获取host
    def get_teachcloud_host(self):
        return self.config.get('teachcloud', 'host')

    # 获取端口
    def get_teachcloud_port(self):
        return self.config.get('teachcloud', 'port')

    def get_teachcloud_baseurl(self):
        protocol = self.get_teachcloud_protocol()
        host = self.get_teachcloud_host()
        port = self.get_teachcloud_port()
        baseurl = "{}://{}".format(protocol, host)
        if port:
            baseurl = "{}:{}".format(baseurl, port)
        return baseurl

    def getTeachCloudUserMoblie(self):
        """获取教学云平台登录手机号 """
        return self.config.get('teachcloud', 'mobile')

    def getTeachCloudPassword(self):
        return self.config.get('teachcloud', 'password')

    def getTeacherUserMoblie(self):
        """获取老师手机号 """
        return self.config.get('teacher', 'mobile')

    def getTeacherPassword(self):
        return self.config.get('teacher', 'password')

    def getTeacherUserName(self):
        return self.config.get('teacher', 'username')


p1_cfg = Product1Config()
