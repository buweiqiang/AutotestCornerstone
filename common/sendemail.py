#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :  sendemail.py
@Contact :  buweiqiang@civaonline.cn
@MTime :    2019/5/9 14:59
@Author:    buweiqiang
@Version:   1.0
@Desciption: None
'''

import os
import time
import requests
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from smtplib import SMTP_SSL

# 请将邮箱配置替换为自己的配置
MAIL_HOST = "smtp.civaonline.cn"
MAIL_PORT = 465
MAIL_USER = "test@civaonline.cn"
MAIL_PASSWD = "xxxxxxxx"


def send_email(mailto_list, title, html_path):
    """发送邮件
    :param mailto_list: 发送到的邮箱列表
    :param title: 邮件标题
    :param content: 邮件内容
    """
    mailto_str = ";".join(mailto_list)
    msg = MIMEText(html_path, 'html', 'utf-8')
    msg['Subject'] = title
    msg['From'] = MAIL_USER
    msg['To'] = mailto_str
    try:
        sender = smtplib.SMTP_SSL(MAIL_HOST, MAIL_PORT)
        sender.login(MAIL_USER, MAIL_PASSWD)
        sender.sendmail(MAIL_USER, mailto_list, msg.as_string())
        sender.close()
        print("发送邮件至：{}，结果：成功".format(mailto_str))
        return True
    except Exception as e:
        print("发送邮件至：{}，失败：{}".format(mailto_str, str(e)))
        return False


def send_html_report(mailto_list, title, html_path, is_local_html=True):
    if mailto_list:
        if is_local_html:
            with open(html_path, 'r', encoding='utf-8') as htmlfile:
                htmlcontent = htmlfile.read()
        else:
            res = requests.get(html_path)
            htmlcontent = res.text
        if len(htmlcontent) > 100:
            send_email(mailto_list, title, htmlcontent)
        else:
            print('邮件内容长度小于100，请检查测试报告是否正常')
    else:
        print('收件人列表为空，请输入正确的参数')


if __name__ == "__main__":
    mailto_list = ["test@civaonline.cn"]
    htmlpath = '/TestResult/自动化测试报告_2019-05-08_11-34-35.html'
    send_html_report(mailto_list, u"西西沃_Civa机器人自动化测试报告", htmlpath)
