# -*- coding: UTF-8 -*-
# author : 杨佳
# datetime :2019/5/22 17:39
# software : PyCharm
# file : __init__.py.py

from conf.config import Config


class Product2Config(Config):

    def __init__(self):
        # 注意大小写一定要和文件夹名，文件名保持一致
        self.product_type = 'DemoProduct2'
        Config.__init__(self, self.product_type)

    def getTeacherProtocol(self):
        if not self.config.has_option('teacher', 'protocol'):
            return 'https'
        return self.config.get('teacher', 'protocol')

    def getTeacherHost(self):
        return self.config.get('teacher', 'host')

    def getTeacherPort(self):
        if not self.config.has_option('teacher', 'port'):
            return ''
        return self.config.get('teacher', 'port')

    def getTeacherUserMoblie(self):
        """获取老师手机号 """
        return self.config.get('teacher', 'mobile')

    def getTeacherPassword(self):
        return self.config.get('teacher', 'password')

    def getTeacherUserName(self):
        return self.config.get('teacher', 'username')

    def getTeaacherV3Protocol(self):
        if not self.config.has_option('teacher_v3', 'protocol'):
            return 'https'
        return self.config.get('teacher_v3', 'protocol')

    def getTeacherV3Host(self):
        return self.config.get('teacher_v3', 'host')

    def getTeacherV3Port(self):
        if not self.config.has_option('teacher_v3', 'port'):
            return ''
        return self.config.get('teacher_v3', 'port')

    def getStudentUserMoblie(self):
        return self.config.get('teacher', 'stu_mobile')

    def getStudentPassword(self):
        return self.config.get('teacher', 'stu_password')

    def getStudentName(self):
        return self.config.get('teacher', 'stu_name')


p2_cfg = Product2Config()
