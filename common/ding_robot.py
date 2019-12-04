#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :  __init__.py.py
@Contact :  buweiqiang@civaonline.cn
@MTime :    2019/5/9 14:59
@Author:    buweiqiang
@Version:   1.0
@Desciption: None
'''

import requests


def send_message(webhook_token, text, atMobiles=[], isAtAll=False):
    msg = {
        "msgtype": "text",
        "text": {
            "content": text
        },
        "at": {
            "atMobiles": atMobiles,
            "isAtAll": isAtAll
        }
    }
    robot_webhook = 'https://oapi.dingtalk.com/robot/send?access_token=%s' % webhook_token
    resp = requests.post(robot_webhook, json=msg)
    print('发送钉钉消息至：{}，结果：{} {}'.format(webhook_token, resp.status_code, resp.text))
    return resp.json()


if __name__ == "__main__":
    report_url = 'https://ci.rokid.com/view/%E4%BA%91%E6%9C%8D%E5%8A%A1%E6%B5%8B%E8%AF%95%E7%BB%84/job/%E4%BA%91%E6%9C%8D%E5%8A%A1-%E8%AF%AD%E9%9F%B3%E4%B8%BB%E9%93%BE%E8%B7%AF%E5%9B%9E%E5%BD%92/ws/TestResult/%E8%AF%AD%E9%9F%B3%E4%B8%BB%E9%93%BE%E8%B7%AF-20190328-40.html'
    send_message('abcdefg', '卜伟强测试，查看自动化测试报告：{}'.format(report_url))
