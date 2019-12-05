#! /usr/bin/env python
# -*- coding: UTF-8 -*-
import time
import os
import io
import datetime
import sys
import unittest

result_data = dict()
result_data['testResult'] = []
current_class_name = ""
STATUS = {
    0: 'Pass',
    1: 'Fail',
    2: 'Error',
    3: 'Skip',
}


class _TestResult(unittest.TestResult):
    def __init__(self, verbosity=1):
        super().__init__(verbosity)
        self.outputBuffer = io.StringIO()
        self.raw_stdout = None
        self.raw_stderr = None
        self.success_count = 0
        self.failure_count = 0
        self.skip_count = 0
        self.error_count = 0
        self.verbosity = verbosity
        self.result = []
        self.start_time = 0
        self.time_cost = 0

    def startTest(self, test):
        self.start_time = time.time()
        super().startTest(test)
        self.raw_stdout = sys.stdout
        self.raw_stderr = sys.stderr
        sys.stdout = self.outputBuffer
        sys.stderr = self.outputBuffer

    def complete_output(self):
        self.time_cost = time.time() - self.start_time
        if self.raw_stdout:
            sys.stdout = self.raw_stdout
            sys.stderr = self.raw_stderr

        result = self.outputBuffer.getvalue()
        self.outputBuffer.seek(0)
        self.outputBuffer.truncate()
        return result

    def stopTest(self, test):
        self.complete_output()

    def addSuccess(self, test):
        self.success_count += 1
        super().addSuccess(test)
        output = self.complete_output()
        self.result.append((0, test, output, '', self.time_cost))

    def addError(self, test, err):
        self.error_count += 1
        super().addError(test, err)
        _, _exc_str = self.errors[-1]
        output = self.complete_output()
        self.result.append((2, test, output, _exc_str, self.time_cost))

    def addSkip(self, test, reason):
        self.skip_count += 1
        super().addSkip(test, reason)
        self.result.append((3, test, "", "", 0.0))

    def addFailure(self, test, err):
        self.failure_count += 1
        super().addFailure(test, err)
        _, _exc_str = self.failures[-1]
        output = self.complete_output()
        self.result.append((1, test, output, _exc_str, self.time_cost))


class HTMLTestRunner3(object):
    def __init__(self, stream=sys.stdout, verbosity=1, title=None, description=None):
        self.stream = stream
        self.verbosity = verbosity
        self.title = title
        self.description = description
        self.startTime = None
        self.stopTime = None

    def run(self, test):
        self.startTime = datetime.datetime.now()
        result = _TestResult(self.verbosity)
        test(result)
        self.stopTime = datetime.datetime.now()
        self.analyze_test_result(result)
        # log.info('Time Elapsed: {}'.format(self.stop_time - self.start_time))

        from report_style import style_3
        style_3.build_report(self.stream, result_data)
        return result

    @staticmethod
    def sort_result(case_results):
        rmap = {}
        classes = []
        for n, t, o, e, run_time in case_results:
            cls = t.__class__
            if cls not in rmap:
                rmap[cls] = []
                classes.append(cls)
            rmap[cls].append((n, t, o, e, run_time))
        r = [(cls, rmap[cls]) for cls in classes]
        return r

    def analyze_test_result(self, result):
        result_data["reportName"] = self.title
        result_data["beginTime"] = str(self.startTime)[:19]
        result_data["totalTime"] = str(self.stopTime - self.startTime)

        sorted_result = self.sort_result(result.result)
        for cid, (cls, cls_results) in enumerate(sorted_result):
            pass_num = fail_num = error_num = skip_num = 0
            for case_state, *_ in cls_results:
                if case_state == 0:
                    pass_num += 1
                elif case_state == 1:
                    fail_num += 1
                elif case_state == 2:
                    error_num += 1
                else:
                    skip_num += 1

            name = "{}.{}".format(cls.__module__, cls.__name__)
            global current_class_name
            current_class_name = name

            for tid, (state_id, t, o, e, run_time) in enumerate(cls_results):

                name = t.id().split('.')[-1]
                doc = t.shortDescription() or ""
                case_data = dict()
                case_data['className'] = current_class_name
                case_data['methodName'] = name
                case_data['spendTime'] = "{:.2}S".format(run_time)
                case_data['description'] = doc
                case_data['log'] = o + e
                if STATUS[state_id] == "Pass":
                    case_data['status'] = "成功"
                if STATUS[state_id] == "Fail":
                    case_data['status'] = "失败"
                if STATUS[state_id] == "Error":
                    case_data['status'] = "错误"
                if STATUS[state_id] == "Skip":
                    case_data['status'] = "跳过"
                result_data['testResult'].append(case_data)

        result_data["testPass"] = result.success_count
        result_data["testAll"] = result.success_count + result.failure_count + result.error_count + result.skip_count
        result_data["testFail"] = result.failure_count
        result_data["testSkip"] = result.skip_count
        result_data["testError"] = result.error_count


class HTMLTestRunner4(HTMLTestRunner3):
    def run(self, test):
        self.startTime = datetime.datetime.now()
        result = _TestResult(self.verbosity)
        test(result)
        self.stopTime = datetime.datetime.now()
        self.analyze_test_result(result)
        # log.info('Time Elapsed: {}'.format(self.stop_time - self.start_time))

        from report_style import style_4
        style_4.build_report(self.stream, result_data)
        return result
