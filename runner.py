# -*- coding: utf-8 -*-
__author__ = "Weiqiang Bu"
__version__ = "1.5"

"""
Version 1.5
* 支持--title参数，自定义测试报告的title
* 优化钉钉消息内容

Version 1.4
* 支持--index参数，在运行时对测试用例按照书写顺序进行编号（例如test_00001_case_name）

Version 1.3
* 支持--style参数，指定不同样式的测试报告，目前支持4种，参数取值范围为1-4，默认为样式1

Version 1.2
* 支持通过指定tag和priority过滤测试用例，需事先对测试用例标记tag和priority
* 支持dry run，即只加载测试用例，并不真正执行
* 调整报告title和日志打印

Version 1.1
* 默认将测试报告输出至固定的report.html，与jenkins的Publish Html reports插件集成

Version 1.0
* 支持通过参数的方式批量执行指定的测试用例，无需事先准备suite
"""

import argparse
import os
import time
import unittest
import patch
from conf import config
from common import sendemail, ding_robot

# 默认的测试结果存储文件夹为：当前文件所在目前下的TestResult文件夹
RESULT_FOLDER = os.path.join(os.path.dirname(__file__), 'TestResult')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('start_dir', help='start dir to discover tests')
    parser.add_argument('-p', dest='pattern', default='*_test.py', help='pattern of python test files')
    parser.add_argument('-o', dest='output', help='specify the output html')
    parser.add_argument('-e', dest='env', help='test environment to run tests')
    parser.add_argument('--clean', dest='days', default=30, help='delete report N days ago')
    parser.add_argument('--mail', dest='mail',
                        help='specify the mail list to send result to, separate by "," for multi addresses')
    parser.add_argument('--ding', dest='ding', help='specify the robot token to send result to dingding')
    parser.add_argument('--notice', dest='nm', default=1, type=int,
                        help='notice mode: 1 = only on fail, 2 = all, default is 1')
    parser.add_argument('--report-url', dest='report', help='the link to view test report')
    parser.add_argument('--priority', type=int, default=4, choices=[0, 1, 2, 3, 4],
                        help='filter test cases with specified priority')
    parser.add_argument('-t', '--tag', default=[], nargs='+',
                        help='filter test cases with specified tag')
    parser.add_argument('--dryrun', action='store_true', default=False,
                        help='just load and count test cases, not really run any of them')
    parser.add_argument('--style', type=int, default=1,
                        help='choice html report style')
    parser.add_argument('--index', action='store_true', default=False,
                        help='append index to test case name by its written order in file')
    parser.add_argument('--title', help='the title of the report')

    args = parser.parse_args()

    # 设置测试环境
    if args.env:
        config.global_cfg.setENV(args.env)

    # 删除N天前的测试报告和日志文件：最小不能小于7天
    if int(args.days) < 7:
        args.days = 7

    try:
        # try cleanup test reports and test log
        # what ever delete succeed or not, pass to run test cases
        from CleanUp import ResultCleaner, LogCleaner

        result_cleaner = ResultCleaner(RESULT_FOLDER)
        result_cleaner.delete_reports(before_days=args.days)
        log_cleaner = LogCleaner()
        log_cleaner.delete_logs(before_days=args.days)
    except Exception as e:
        print('Exception happened while cleaning test report & log: \"%s\"' % e)
        pass

    # 设置是否为测试用例按照书写顺序增加编号，以使其按照书写顺序被执行
    if args.index:
        patch.start_indexing_test_cases()

    # load tests
    test_loader = unittest.defaultTestLoader
    suite = test_loader.discover(start_dir=args.start_dir, pattern=args.pattern)
    print('pattern is: \"%s\", case discovered: %s' % (args.pattern, suite.countTestCases()))

    wanted_priority = args.priority
    wanted_tags = args.tag

    patch.filter_tests(suite, wanted_priority, wanted_tags)
    print('Priority={}, tag={}, match test case count: {}'.format(wanted_priority, wanted_tags, suite.countTestCases()))

    # 等一秒钟，做为jenkins打印测试用例树的缓冲
    time.sleep(1)

    # 定义测试报告输出位置和文件名
    if not os.path.exists(RESULT_FOLDER):
        os.mkdir(RESULT_FOLDER)
    if args.output:
        output_name = args.output.strip()
    else:
        output_name = 'report.html'
    if not output_name.endswith('.html'):
        output_name = output_name + '.html'
    output_file = os.path.join(RESULT_FOLDER, output_name)

    # run tests and generate report
    print('report output: %s' % output_file)

    # 如果未传入title参数，则以输出文件名做为title
    # report_title = f"{time.strftime('%Y-%m-%d %H:%M:%S')} {output_name}"
    report_title = args.title if args.title else output_name
    print('report title: {}'.format(report_title))

    # 定义测试报告的描述部分：如果传入了测试报告的查看链接，则在报告描述中插入此链接
    description = ''
    if args.report:
        # 置入测试报告链接
        description = '查看测试报告：{}'.format(args.report)
        print('report link: {}'.format(args.report))

    is_dryrun = args.dryrun
    if is_dryrun:
        print('--------- this is dry run ----------')
    else:
        if args.style == 2:
            from HTMLTestRunnerPie import HTMLTestRunner
        elif args.style == 3:
            from HTMLTestRunnerUTX import HTMLTestRunner3 as HTMLTestRunner
        elif args.style == 4:
            from HTMLTestRunnerUTX import HTMLTestRunner4 as HTMLTestRunner
        else:
            # 默认的html结果格式
            from HTMLTestRunnerCN import HTMLTestRunner

        with open(output_file, 'wb') as fp:
            runner = HTMLTestRunner(fp, title=report_title, description=description, verbosity=2)
            result = runner.run(suite)
            result_summary = 'Total: %s, succeed: %s, failure: %s, error: %s skip: %s' % (suite.countTestCases(),
                                                                                          result.success_count,
                                                                                          result.failure_count,
                                                                                          result.error_count,
                                                                                          result.skip_count)
            print(result_summary)
            # 判断本次执行是否失败，如果失败则最终抛出异常，以便jenkins能识别为任务执行失败
            fail_flag = result.failure_count > 0 or result.error_count > 0
        duration_total = (runner.stopTime - runner.startTime).total_seconds()
        start_time_str = runner.startTime.strftime('%Y-%m-%d %H:%M:%S')
        stop_time_str = runner.stopTime.strftime('%Y-%m-%d %H:%M:%S')

        # 根据入参确定是否要发送测试结果
        send_notice = args.nm == 2 or fail_flag

        # 通过邮件发送测试报告
        if args.mail and send_notice:
            mail_to = args.mail.split(',')
            sendemail.send_html_report(mail_to, report_title, output_file)

        # 发送钉钉通知测试结果
        if args.ding and send_notice:
            time_msg = f'{duration_total}s ({start_time_str} ~ {stop_time_str})'
            msg = '测试报告：{}\n执行时间：{}\n测试结果：{}\n{}'.format(report_title, time_msg, result_summary, description)
            ding_to = args.ding.split(',')
            for token in ding_to:
                ding_robot.send_message(token, msg)

        if fail_flag:
            raise AssertionError(result_summary)
