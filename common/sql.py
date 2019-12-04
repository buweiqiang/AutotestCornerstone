#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File : sql.py 
@Contact : yangxx@civaonline.cn
@MTime : 2019/9/3 14:51 
@Author: yangxingxiang
@Version: 1.0
@Description: 封装常用的数据库使用方法
"""
import pymysql


class MySql(object):
    def __init__(self, host=None, port=None, username=None, password=None, db_name=None, charset='utf8'):
        self.host = host
        self.port = int(port)
        self.username = username
        self.password = password
        self.db_nmae = db_name
        self.charset = charset
        self.content_db = self.init_content_db()

    def init_content_db(self):
        """
        mysql数据库连接基本信息的封装
        :return:
        """
        content_info = pymysql.connect(
            host=self.host,
            port=self.port,
            user=self.username,
            password=self.password,
            db=self.db_nmae,
            charset=self.charset,
            cursorclass=pymysql.cursors.DictCursor
        )
        return content_info

    def data_total(self, sql):
        """
        统计sql查询出的总数
        :param sql:
        :return:
        """
        cnt = self.content_db
        cur = cnt.cursor()
        try:
            count = cur.execute(sql)
            # counts = cur.rowcount
            cnt.commit()
            return count
        except pymysql.Error as E:
            print('运行sql异常:', E)
        finally:
            cur.close()

    def data_info(self, sql):
        """
        输出数据的详细信息
        :param sql:
        :return:
        """
        cnt = self.content_db
        cur = cnt.cursor()
        try:
            count = cur.execute(sql)
            data_info = cur.fetchmany(count)
            return data_info
        except pymysql.Error as E:
            print('运行sql异常:', E)
        finally:
            cur.close()

    def close_db(self):
        cnt = self.content_db
        return cnt.close()


from pyhive import hive


class HiveSql(object):
    def __init__(self, host=None, port=None, username=None, password=None, db_name=None, auth=None):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.db_nmae = db_name
        self.auth = auth
        self.content_hive = self.init_content_hive()

    def init_content_hive(self):
        try:
            content_info = hive.connect(
                host=self.host,
                port=self.port,
                username=self.username,
                password=self.password,
                database=self.db_nmae,
                auth=self.auth
            )
            return content_info
        except hive.Error as E:
            print('连接hive库:', E)

    def data_total(self, sql):
        cnt = self.content_hive
        cur = cnt.cursor()
        try:
            cur.execute(sql)
            counts = cur.rownumber
            cnt.commit()
            return counts
        except hive.Error as E:
            print('运行sql异常:', E)
        finally:
            cur.close()

    def data_info(self, sql):
        cnt = self.content_hive
        cur = cnt.cursor()
        try:
            datas_info = cur.execute(sql)
            data_info = cur.fetchmany(datas_info)
            cnt.commit()
            return data_info
        except pymysql.Error as E:
            print('运行sql异常:', E)
        finally:
            cur.close()

    def close_db(self):
        cnt = self.content_hive
        return cnt.close()

# h = HiveSql(host='192.168.0.205',port='10000',username='hadoop',db_name='datacenter')
# h.content_hive()
# db_202 = MySql(host='192.168.0.202',
#                port=3306,username='ccwtest',password='#ccw.test@',db_name='teach')
# a = db_202.data_total('SELECT * FROM t_video limit 10')
