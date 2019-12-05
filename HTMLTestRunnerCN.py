# -*- coding: utf-8 -*-
"""
A TestRunner for use with the Python unit testing framework. It
generates a HTML report to show the result at a glance.
The simplest way to use this is to invoke its main method. E.g.
    import unittest
    import HTMLTestRunner
    ... define your tests ...
    if __name__ == '__main__':
        HTMLTestRunner.main()
For more customization options, instantiates a HTMLTestRunner object.
HTMLTestRunner is a counterpart to unittest's TextTestRunner. E.g.
    # output to a file
    fp = file('my_report.html', 'wb')
    runner = HTMLTestRunner.HTMLTestRunner(
                stream=fp,
                title='My unit test',
                description='This demonstrates the report output by HTMLTestRunner.'
                )
    # Use an external stylesheet.
    # See the Template_mixin class for more customizable options
    runner.STYLESHEET_TMPL = '<link rel="stylesheet" href="my_stylesheet.css" type="text/css">'
    # run the test
    runner.run(my_test_suite)
------------------------------------------------------------------------
Copyright (c) 2004-2007, Wai Yip Tung
All rights reserved.
Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are
met:
* Redistributions of source code must retain the above copyright notice,
  this list of conditions and the following disclaimer.
* Redistributions in binary form must reproduce the above copyright
  notice, this list of conditions and the following disclaimer in the
  documentation and/or other materials provided with the distribution.
* Neither the name Wai Yip Tung nor the names of its contributors may be
  used to endorse or promote products derived from this software without
  specific prior written permission.
THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS
IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED
TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A
PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER
OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

# URL: http://tungwaiyip.info/software/HTMLTestRunner.html

__author__ = "Wai Yip Tung,  Findyou"
__version__ = "0.8.4"

"""
Change History
Version 0.8.4
* Collect and show time cost of each test case (Weiqiang Bu).

Version 0.8.3
* Use Bootstrap (Zhang Xin)
* Change to Chinese (Zhang Xin)

Version 0.8.2.1 -Findyou
* 支持中文，汉化
* 调整样式，美化（需要连入网络，使用的百度的Bootstrap.js）
* 增加 通过分类显示、测试人员、通过率的展示
* 优化“详细”与“收起”状态的变换
* 增加返回顶部的锚点

Version 0.8.2
* Show output inline instead of popup window (Viorel Lupu).
Version in 0.8.1
* Validated XHTML (Wolfgang Borgert).
* Added description of test classes and test cases.
Version in 0.8.0
* Define Template_mixin class for customization.
* Workaround a IE 6 bug that it does not treat <script> block as CDATA.
Version in 0.7.1
* Back port to Python 2.3 (Frank Horowitz).
* Fix missing scroll bars in detail log (Podi).
"""

# TODO: color stderr
# TODO: simplify javascript using ,ore than 1 class in the class attribute?

import datetime
import sys
import time
import unittest
from unittest.case import _UnexpectedSuccess

if sys.version > '3':
    PY3 = True
    import io as StringIO
else:
    reload(sys)
    sys.setdefaultencoding('utf-8')
    PY3 = False
    import StringIO

# ------------------------------------------------------------------------
# The redirectors below are used to capture output during testing. Output
# sent to sys.stdout and sys.stderr are automatically captured. However
# in some cases sys.stdout is already cached before HTMLTestRunner is
# invoked (e.g. calling logging.basicConfig). In order to capture those
# output, use the redirectors for the cached stream.
#
# e.g.
#   >>> logging.basicConfig(stream=HTMLTestRunner.stdout_redirector)
#   >>>


TestResult = unittest.TestResult


class _TestResult(TestResult):
    # note: _TestResult is a pure representation of results.
    # It lacks the output and reporting ability compares to unittest._TextTestResult.

    def __init__(self, verbosity=1):
        TestResult.__init__(self)
        self.outputBuffer = StringIO.StringIO()
        self.raw_stdout = None
        self.raw_stderr = None
        self.success_count = 0
        self.failure_count = 0
        self.error_count = 0
        self.skip_count = 0
        self.verbosity = verbosity
        self.start_time = 0
        self.time_cost = 0

        # result is a list of result in 4 tuple
        # (
        #   result code (0: success; 1: fail; 2: error),
        #   TestCase object,
        #   Test output (byte string),
        #   stack trace,
        # )
        self.result = []
        # 增加一个测试通过率 --Findyou
        self.passrate = float(0)

    def startTest(self, test):
        TestResult.startTest(self, test)
        # just one buffer for both stdout and stderr
        # self.outputBuffer = StringIO.StringIO()

        self.raw_stdout = sys.stdout
        self.raw_stderr = sys.stderr
        sys.stdout = self.outputBuffer
        sys.stderr = self.outputBuffer
        self.start_time = time.time()

    def complete_output(self):
        """
        Disconnect output redirection and return buffer.
        Safe to call multiple times.
        """
        if self.raw_stdout:
            sys.stdout = self.raw_stdout
            sys.stderr = self.raw_stderr
        output = self.outputBuffer.getvalue()
        # need clear buffer after each test
        self.outputBuffer.truncate(0)
        self.outputBuffer.seek(0)
        return output

    def stopTest(self, test):
        # Usually one of addSuccess, addError or addFailure would have been called.
        # But there are some path in unittest that would bypass this.
        # We must disconnect stdout in stopTest(), which is guaranteed to be called.
        self.complete_output()

    def addSuccess(self, test):
        self.success_count += 1
        TestResult.addSuccess(self, test)
        output = self.complete_output()
        self.time_cost = '{0} s'.format(round(time.time() - self.start_time, 2))
        self.result.append((0, test, output, '', self.time_cost))
        if self.verbosity > 1:
            sys.stderr.write('ok ')
            sys.stderr.write(str(test))
            sys.stderr.write('\n')
        else:
            sys.stderr.write('.')

    def addError(self, test, err):
        self.error_count += 1
        TestResult.addError(self, test, err)
        _, _exc_str = self.errors[-1]
        output = self.complete_output()
        self.time_cost = '{0} s'.format(round(time.time() - self.start_time, 2))
        self.result.append((2, test, output, _exc_str, self.time_cost))
        if self.verbosity > 1:
            sys.stderr.write('E  ')
            sys.stderr.write(str(test))
            sys.stderr.write('\n')
        else:
            sys.stderr.write('E')

    def addFailure(self, test, err):
        self.failure_count += 1
        TestResult.addFailure(self, test, err)
        _, _exc_str = self.failures[-1]
        output = self.complete_output()
        self.time_cost = '{0} s'.format(round(time.time() - self.start_time, 2))
        self.result.append((1, test, output, _exc_str, self.time_cost))
        if self.verbosity > 1:
            sys.stderr.write('F  ')
            sys.stderr.write(str(test))
            sys.stderr.write('\n')
        else:
            sys.stderr.write('F')

    def addSkip(self, test, reason):
        self.skip_count += 1
        super().addSkip(test, reason)
        output = self.complete_output()
        self.time_cost = '{0} s'.format(round(time.time() - self.start_time, 2))
        self.result.append((3, test, output, reason, self.time_cost))
        if self.verbosity > 1:
            sys.stderr.write('S  ')
            sys.stderr.write(str(test))
            sys.stderr.write('\n')
        else:
            sys.stderr.write('S')

    def addExpectedFailure(self, test, err):
        self.addSuccess(test)

    def addUnexpectedSuccess(self, test):
        try:
            raise _UnexpectedSuccess("Expect Fail but Success")
        except _UnexpectedSuccess:
            self.addFailure(test, sys.exc_info())


class HTMLTestRunner(object):
    """
    """
    result_data = dict()

    def __init__(self, stream=sys.stdout, verbosity=1, title=None, description=None):
        self.stream = stream
        self.verbosity = verbosity
        self.title = title
        self.description = description
        self.startTime = None
        self.stopTime = None

    def run(self, test):
        "Run the given test case or test suite."
        self.startTime = datetime.datetime.now()
        result = _TestResult(self.verbosity)
        test(result)
        self.stopTime = datetime.datetime.now()
        self.analyze_test_result(result)

        from report_style import style_1
        style_1.generate_report(self.stream, self.result_data)

        print('\nTime Elapsed: %s' % (self.stopTime - self.startTime))
        return result

    def sort_result(self, result_list):
        # unittest does not seems to run in any particular order.
        # Here at least we want to group them together by class.
        rmap = {}
        classes = []
        for result_code, tc, stdout, stderr, cost in result_list:
            cls = tc.__class__
            if not cls in rmap:
                rmap[cls] = []
                classes.append(cls)
            rmap[cls].append((result_code, tc, stdout, stderr, cost))
        r = [(cls, rmap[cls]) for cls in classes]
        return r

    # 分析整理测试结果为生成report所需要的格式
    def analyze_test_result(self, result):
        """
        Return report attributes as a list of (name, value).
        Override this to add custom attributes.
        """
        startTime = str(self.startTime)[:19]
        duration = str(self.stopTime - self.startTime)
        result_summary = []
        total_count = result.success_count + result.failure_count + result.error_count
        result_summary.append('共 %s' % (total_count))
        if result.success_count:
            result_summary.append('通过 %s' % result.success_count)
        if result.failure_count:
            result_summary.append('失败 %s' % result.failure_count)
        if result.error_count:
            result_summary.append('错误 %s' % result.error_count)
        if total_count:
            self.passrate = str("%.2f%%" % (float(result.success_count) / float(total_count) * 100))
            result_summary.append("通过率= " + self.passrate)
            result_summary = '，'.join(result_summary)
        else:
            self.passrate = '0.00%'
            result_summary = 'No test case found'

        self.result_data['result_summary'] = dict(
            count=str(total_count),
            total=str(total_count),
            Pass=str(result.success_count),
            fail=str(result.failure_count),
            error=str(result.error_count),
            skip=str(result.skip_count),
            passrate=self.passrate,
        )

        self.result_data['report_attrs'] = dict(
            title=self.title,
            description=self.description,
            start_time=startTime,
            duration=duration,
            summary=result_summary,
        )

        self.result_data['test_result'] = self.sort_result(result.result)
