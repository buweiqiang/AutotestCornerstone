#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :  config.py
@Contact :  buweiqiang@civaonline.cn
@MTime :    2019/5/9 14:59
@Author:    buweiqiang
@Version:   1.0
@Desciption: None
'''

import argparse
import os
import sys

if sys.version > '3':
    PY3 = True
else:
    reload(sys)
    sys.setdefaultencoding('utf-8')
    PY3 = False

CONF_DIR = os.path.dirname(__file__)

if not PY3:
    import ConfigParser as configparser
else:
    import configparser


def getConfigFiles(product_name, env, has_product_dir=False):
    '''
    根据产品类型获取相关的配置文件
    :param product_name: 产品名称，不同的产品的配置放在以与产品名称相同的配置文件中，例如：product_name.cfg
    :param env: 指定要获取哪个环境的配置文件
    :param has_product_dir: 是否将不同产品的配置文件，放到以产品名称命名的不同的文件夹中，默认为False
   :return: 文件列表如：[global.cfg, product.global.cfig, product.env.cfg]
    '''
    configfiles = []
    # 加载全局配置文件,一定存在
    _global_file = os.path.join(CONF_DIR, 'global.cfg')
    configfiles.append(_global_file)

    # 加载指定产品组(config_type)的全局配置文件, 可能不存在
    _product_global_file = os.path.join(CONF_DIR, '{}.global.cfg'.format(product_name))
    if os.path.exists(_product_global_file):
        configfiles.append(_product_global_file)

    product_config_dir = ""
    if has_product_dir:
        product_config_dir = product_name

    # 加载指定env的配置文件config_type.env.cfg
    _product_config_file = None
    if env:
        _product_config_file = os.path.join(CONF_DIR, product_config_dir, '{}.{}.cfg'.format(product_name, env))
        if not os.path.exists(_product_config_file):
            print('%s not found, will use the default one' % _product_config_file)
            _product_config_file = None
    # 如不存在, 默认为config_type.cfg
    if not _product_config_file:
        _product_config_file = os.path.join(CONF_DIR, product_config_dir, '{}.cfg'.format(product_name))
    configfiles.append(_product_config_file)

    return configfiles


# 通过实现__new__方法实现单例模式
# 将一个类的实例绑定到类变量_instance上,
# 如果cls._instance为None说明该类还没有实例化过,实例化该类,并返回
# 如果cls._instance不为None,直接返回cls._instance
class Singleton(object):
    instance = None

    def __new__(cls, *args, **kw):
        # if not hasattr(cls, '__instance'):
        if not cls.instance:
            orig = super(Singleton, cls)
            cls.instance = orig.__new__(cls)
        return cls.instance


class CommonConfig(object):
    def __init__(self, config_files):
        if isinstance(config_files, str):
            config_files = config_files.split(',')
        self.config = configparser.RawConfigParser()
        if PY3:
            self.config.read(config_files, encoding='utf-8')
        else:
            self.config.read(config_files)

    def getItemValue(self, section, itemkey):
        return self.config.get(section, itemkey)

    def setItemValue(self, section, item_key, item_value):
        self.config.set(section, item_key, item_value)


class Config(Singleton, CommonConfig):
    def __init__(self, product_type):
        if not hasattr(self, 'config'):
            config_files = getConfigFiles(product_type, ENV)
            CommonConfig.__init__(self, config_files)

    def getTestUsername(self):
        if not self.config.has_option('test', 'username'):
            return ''
        return self.config.get('test', 'username')

    def getTestPassword(self):
        if not self.config.has_option('test', 'password'):
            return ''
        return self.config.get('test', 'password')


class GlobalConfig(Singleton, CommonConfig):
    def __init__(self):
        self.config_file = os.path.join(CONF_DIR, 'global.cfg')
        if not hasattr(self, 'config'):
            CommonConfig.__init__(self, self.config_file)

    def getENV(self):
        if not self.config.has_option('test', 'env'):
            return None
        env = self.config.get('test', 'env')
        if env.lower() in ("none", "default"):
            env = None
        return env

    def setENV(self, env):
        self.setItemValue('test', 'env', env)
        global ENV
        ENV = env
        print('- set env to {} in {}'.format(env, self.config_file))

    def getLogLevel(self):
        level = self.config.get('log', 'log_level')
        return level.upper()

    def getLogToFile(self):
        return self.config.get('log', 'log_to_file')

    def getLogDir(self):
        log_dir = self.config.get('log', 'log_dir')
        return os.path.join(CONF_DIR, log_dir)

    def getTestDataDir(self):
        data_dir = self.config.get('test', 'testdatadir')
        return os.path.join(CONF_DIR, data_dir)

    def getPCUserAgent(self):
        if not self.config.has_option('test', 'pc_user_agent'):
            return 'AutoTest/5.0'
        return self.config.get('test', 'pc_user_agent')

    def getMobileUserAgent(self):
        if not self.config.has_option('test', 'mobile_user_agent'):
            return 'Android 6.0'
        return self.config.get('test', 'mobile_user_agent')


def getGlobalConfig():
    return GlobalConfig()


# global.cfg是必须存在的，里面test.env是基础配置
global_cfg = GlobalConfig()
ENV = global_cfg.getENV()

if __name__ == '__main__':
    '根据环境加载配置文件'
    parser = argparse.ArgumentParser()
    parser.add_argument('env', nargs='?', help='specify the environment to be set to')
    parser.add_argument('-l', dest='log_level', default='', help='log level: debug/info/warn/error/fatal')

    args = parser.parse_args()
    # 修改global.cfg中的env参数
    if args.env:
        print('Setting env to ', args.env)
        global_cfg.setItemValue('test', 'env', args.env)
        print('- set env to {} in {}'.format(args.env, global_cfg.config_file))

    # 配置日志级别，方便调试时打印更多的信息
    if args.log_level:
        if not global_cfg.config.has_section('log'):
            global_cfg.config.add_section('log')
        global_cfg.config.set('log', 'log_level', args.log_level)
        print('- set log level to {} in {}'.format(args.log_level, global_cfg.config_file))

    with open(global_cfg.config_file, 'w') as fp:
        global_cfg.config.write(fp)

    print('current env is:', global_cfg.getENV())
