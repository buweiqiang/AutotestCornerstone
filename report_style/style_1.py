#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File : style_1.py
@Contact : buweiqiang@civaonline.cn
@MTime : 2019-12-02 10:56 
@Author: buweiqiang
@Desciption: None
'''

from xml.sax import saxutils

__version__ = "0.8.4 by bwq"


# ----------------------------------------------------------------------
# Template

class Template_mixin(object):
    """
    Define a HTML template for report customerization and generation.
    Overall structure of an HTML report
    HTML
    +------------------------+
    |<html>                  |
    |  <head>                |
    |                        |
    |   STYLESHEET           |
    |   +----------------+   |
    |   |                |   |
    |   +----------------+   |
    |                        |
    |  </head>               |
    |                        |
    |  <body>                |
    |                        |
    |   HEADING              |
    |   +----------------+   |
    |   |                |   |
    |   +----------------+   |
    |                        |
    |   REPORT               |
    |   +----------------+   |
    |   |                |   |
    |   +----------------+   |
    |                        |
    |   ENDING               |
    |   +----------------+   |
    |   |                |   |
    |   +----------------+   |
    |                        |
    |  </body>               |
    |</html>                 |
    +------------------------+
    """

    STATUS = {
        0: u'通过',
        1: u'失败',
        2: u'错误',
        3: u'跳过',
    }

    DEFAULT_TITLE = '自动化测试报告'
    DEFAULT_DESCRIPTION = ''

    # ------------------------------------------------------------------------
    # HTML Template

    HTML_TMPL = r"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
    <title>%(title)s</title>
    <meta name="generator" content="%(generator)s"/>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8"/>
    <link href="https://libs.baidu.com/bootstrap/3.0.3/css/bootstrap.min.css" rel="stylesheet">
    <script src="https://libs.baidu.com/jquery/2.0.0/jquery.min.js"></script>
    <script src="https://libs.baidu.com/bootstrap/3.0.3/js/bootstrap.min.js"></script>
    %(stylesheet)s
</head>
<body >
<script language="javascript" type="text/javascript">
output_list = Array();
/*level 调整增加只显示通过用例的分类 --Findyou
修必测试用例的id，优化showCase的实现方式 --weiqiang bu
0:summary //all hiddenRow
1:failed  //fail_tc none, other hiddenRow
2:error   //error_tc none, other hiddenRow
3:pass    //pass_tc none, other hiddenRow
4:all     //all none
*/
function showCase(level) {
    trs = document.getElementsByTagName("tr");
    for (var i = 0; i < trs.length; i++) {
        tr = trs[i];        
        id = tr.id;
        if (id) {
            if (level == "all" || id.indexOf(level.toLowerCase()) != -1) {
                tr.className = '';
            }
            else {
                tr.className = 'hiddenRow';
            }
        }
        // 测试类总结行的最后一列显示详细还是收起 --weiqiang bu
        if (tr.children.length==6) {
            detail_node=tr.children[5].firstChild;
            if (level == "all") {
                detail_node.innerHTML="收起";
            }
            if (level == "summary") {
                detail_node.innerHTML="详细";
            }
        }   
    }
}
function showClassDetail(cid, count) {
    var id_list = Array(count);
    var toHide = 1;
    for (var i = 0; i < count; i++) {
        //ID修改 点 为 下划线 -Findyou
        tid0 = '_tc_' + cid.substr(1) + '_' + (i+1);
        tid = 'fail' + tid0;
        tr = document.getElementById(tid);
        if (!tr) {
            tid = 'error' + tid0;
            tr = document.getElementById(tid);
        }
        if (!tr) {
            tid = 'pass' + tid0;
            tr = document.getElementById(tid);
        }
        if (!tr) {
            tid = 'skip' + tid0;
            tr = document.getElementById(tid);
        }
        id_list[i] = tid;
        if (tr.className) {
            toHide = 0;
        }
    }
    for (var i = 0; i < count; i++) {
        tid = id_list[i];
        //修改点击无法收起的BUG，加入【详细】切换文字变化 --Findyou
        if (toHide) {
            document.getElementById(tid).className = 'hiddenRow';
            document.getElementById(cid).innerText = "详细"
        }
        else {
            document.getElementById(tid).className = '';
            document.getElementById(cid).innerText = "收起"
        }
    }
}


function showTestDetail(div_id){
    var details_div = document.getElementById(div_id)
    var displayState = details_div.style.display
    // alert(displayState)
    if (displayState != 'block' ) {
        displayState = 'block'
        details_div.style.display = 'block'
    }
    else {
        details_div.style.display = 'none'
    }
}


function html_escape(s) {
    s = s.replace(/&/g,'&amp;');
    s = s.replace(/</g,'&lt;');
    s = s.replace(/>/g,'&gt;');
    return s;
}

</script>
%(heading)s
%(report)s
%(ending)s
</body>
</html>
"""
    # variables: (title, generator, stylesheet, heading, report, ending)

    # ------------------------------------------------------------------------
    # Stylesheet
    #
    # alternatively use a <link> for external style sheet, e.g.
    #   <link rel="stylesheet" href="$url" type="text/css">

    STYLESHEET_TMPL = """
<style type="text/css" media="screen">
body        { font-family: Microsoft YaHei,Tahoma,arial,helvetica,sans-serif;padding: 20px; font-size: 80%; }
table       { font-size: 100%; }
/* -- heading ---------------------------------------------------------------------- */
.heading {
    margin-top: 0ex;
    margin-bottom: 1ex;
}
.heading .description {
    margin-top: 4ex;
    margin-bottom: 6ex;
}
/* -- report ------------------------------------------------------------------------ */
#show_detail_line {
    margin-top: 3ex;
    margin-bottom: 1ex;
}
#result_table {
    width: 99%;
}
#header_row {
    font-weight: bold;
    color: white;
    background-color: #777;
}
#total_row  { font-weight: bold; }
.passClass  { background-color: #74A474; }
.failClass  { background-color: #FDD283; }
.errorClass { background-color: #FF6600; }
.passCase   { color: #5cb85c; }
.errorCase  { color: #d9534f; font-weight: bold; }
.failCase   { color: #f0ad4e; font-weight: bold; }
.hiddenRow  { display: none; }
.testcase   { margin-left: 2em; }
</style>
"""

    # ------------------------------------------------------------------------
    # Heading
    #

    HEADING_TMPL = """<div class='heading'>
<h1 style="font-family: Microsoft YaHei">%(title)s</h1>
%(parameters)s
</div>
<p class='description'>%(description)s</p>
</div>
"""  # variables: (title, parameters, description)

    HEADING_ATTRIBUTE_TMPL = """<p class='attribute'><strong>%(name)s : </strong> %(value)s</p>
"""  # variables: (name, value)

    # ------------------------------------------------------------------------
    # Report
    #
    # 汉化,加美化效果 --Findyou
    REPORT_TMPL = """
<p id='show_detail_line'>
<a class="btn btn-primary" href='javascript:showCase("summary")'>概要{ %(passrate)s }</a>
<a class="btn btn-warning" href='javascript:showCase("fail")'>失败{ %(fail)s }</a>
<a class="btn btn-danger" href='javascript:showCase("error")'>错误{ %(error)s }</a>
<a class="btn btn-success" href='javascript:showCase("Pass")'>通过{ %(Pass)s }</a>
<a class="btn btn-info" href='javascript:showCase("all")'>所有{ %(count)s }</a>
</p>
<table id='result_table' class="table table-condensed table-bordered table-hover">
<colgroup>
<col align='left' />
<col align='right' />
<col align='right' />
<col align='right' />
<col align='right' />
<col align='right' />
</colgroup>
<tr id='header_row' class="text-center success" style="font-weight: bold;font-size: 14px;">
    <td>用例集/测试用例</td>
    <td>总计</td>
    <td>通过</td>
    <td>失败</td>
    <td>错误</td>
    <td>详细</td>
</tr>
%(test_list)s
<tr id='total_row' class="text-center active">
    <td>总计</td>
    <td>%(count)s</td>
    <td>%(Pass)s</td>
    <td>%(fail)s</td>
    <td>%(error)s</td>
    <td>通过率：%(passrate)s</td>
</tr>
</table>
"""  # variables: (test_list, count, Pass, fail, error ,passrate)

    REPORT_CLASS_TMPL = r"""
<tr class='%(style)s warning'>
    <td>%(desc)s</td>
    <td class="text-center">%(count)s</td>
    <td class="text-center">%(Pass)s</td>
    <td class="text-center">%(fail)s</td>
    <td class="text-center">%(error)s</td>
    <td class="text-center"><a href="javascript:showClassDetail('%(cid)s',%(count)s)" class="detail" id='%(cid)s'>详细</a></td>
</tr>
"""  # variables: (style, desc, count, Pass, fail, error, cid)

    # 错误的样式，红色按钮效果  -weiqiang
    REPORT_TEST_ERROR_TMPL = r"""
    <tr id='%(tid)s' class='%(Class)s'>
    <td class='%(style)s'><div class='testcase'>%(desc)s</div></td>
    <td colspan='4' align='left'>
    <!--默认收起错误信息 -Findyou
    <button id='btn_%(tid)s' type="button"  class="btn btn-danger btn-xs collapsed" data-toggle="collapse" data-target='#div_%(tid)s'>%(status)s</button>
    <div id='div_%(tid)s' class="collapse">  -->
    <!-- 默认展开错误信息 -Findyou -->
    <button id='btn_%(tid)s' type="button"  class="btn btn-danger btn-xs" data-toggle="collapse" data-target='#div_%(tid)s'>%(status)s</button>
    <div id='div_%(tid)s' class="collapse in">
    %(script)s
    </div>
    </td>
    <td align='center'>%(cost)s</td>
    </tr>
    """  # variables: (tid, Class, style, desc, status)

    # 失败的样式，橙色按钮效果  -weiqiang
    REPORT_TEST_FAIL_TMPL = r"""
        <tr id='%(tid)s' class='%(Class)s'>
        <td class='%(style)s'><div class='testcase'>%(desc)s</div></td>
        <td colspan='4' align='left'>
        <!-- 默认展开错误信息 -Findyou -->
        <button id='btn_%(tid)s' type="button"  class="btn btn-warning btn-xs" data-toggle="collapse" data-target='#div_%(tid)s'>%(status)s</button>
        <div id='div_%(tid)s' class="collapse in">
        %(script)s
        </div>
        </td>
        <td align='center'>%(cost)s</td>
    </tr>
    """  # variables: (tid, Class, style, desc, status)

    # 通过的样式：绿色按钮效果  -weiqiang
    REPORT_TEST_SUCCESS_TMPL = r"""
    <tr id='%(tid)s' class='%(Class)s'>
    <td class='%(style)s'><div class='testcase'>%(desc)s</div></td>
    <td colspan='4' align='left'>
    <!-- <span class="label label-success success">%(status)s</span> -->
    <button id='btn_%(tid)s' type="button"  class="btn btn-success btn-xs" data-toggle="collapse" data-target='#div_%(tid)s'>%(status)s</button>
    <div id='div_%(tid)s' class="collapse in">
    %(script)s
    </div>
    </td>
    <td align='center'>%(cost)s</td>
    </tr>
    """  # variables: (tid, Class, style, desc, status,cost)

    # 跳过的样式：普通效果  -weiqiang
    REPORT_TEST_SKIP_TMPL = """
    <tr id="%(tid)s" class="%(Class)s">
            <td class="%(style)s">
                <div class="testcase">%(desc)s</div>
            </td>
            <td colspan="4" align="center">
            <span class="label label-info success">%(status)s</span>
            </td>
            <td align='center'>%(cost)s</td>
    </tr>
    """

    REPORT_TEST_OUTPUT_TMPL = r"""
<pre>
%(id)s: 
%(output)s
</pre>
"""  # variables: (id, output)

    # ------------------------------------------------------------------------
    # ENDING
    #
    # 增加返回顶部按钮  --Findyou
    ENDING_TMPL = """<div id='ending'>&nbsp;</div>
    <div style=" position:fixed;right:50px; bottom:30px; width:20px; height:20px;cursor:pointer">
    <a href="#"><span class="glyphicon glyphicon-eject" style = "font-size:30px;" aria-hidden="true">
    </span></a></div>
    """

    def generate_report(self, file_stream, result_data: dict):
        generator = 'HTMLTestRunner %s' % __version__
        stylesheet = self._generate_stylesheet()
        report_attrs = result_data.get('report_attrs')
        heading = self._generate_heading(report_attrs)
        sorted_result = result_data.get('test_result')
        result_summary = result_data.get('result_summary')
        report = self._generate_report(sorted_result, result_summary)
        ending = self._generate_ending()

        output = self.HTML_TMPL % dict(
            title=saxutils.escape(report_attrs.get('title')),
            generator=generator,
            stylesheet=stylesheet,
            heading=heading,
            report=report,
            ending=ending,
        )
        file_stream.write(output.encode('utf8'))

    def _generate_stylesheet(self):
        return self.STYLESHEET_TMPL

    def _generate_heading(self, report_attrs: dict):
        line_attrs = [
            (u'开始时间', report_attrs.get('start_time')),
            (u'合计耗时', report_attrs.get('duration')),
            (u'测试总结', report_attrs.get('summary')),
        ]

        a_lines = []
        for name, value in line_attrs:
            line = self.HEADING_ATTRIBUTE_TMPL % dict(
                name=saxutils.escape(name),
                value=saxutils.escape(value),
            )
            a_lines.append(line)

        heading = self.HEADING_TMPL % dict(
            title=saxutils.escape(report_attrs.get('title')),
            parameters=''.join(a_lines),
            description=saxutils.escape(report_attrs.get('description')),
        )
        return heading

    # 生成报告  --Findyou添加注释
    def _generate_report(self, sorted_result, result_summary: dict):
        rows = []
        # sorted_result = self.sort_result(result.result)
        for cid, (cls, cls_results) in enumerate(sorted_result):
            # subtotal for a class
            no_pass = no_fail = no_error = no_skip = 0
            for result_code, tc, stdout, stderr, cost in cls_results:
                if result_code == 0:
                    no_pass += 1
                elif result_code == 1:
                    no_fail += 1
                elif result_code == 3:
                    no_skip += 1
                else:
                    no_error += 1

            # format class description
            if cls.__module__ == "__main__":
                name = cls.__name__
            else:
                name = "%s.%s" % (cls.__module__, cls.__name__)
            doc = cls.__doc__ and cls.__doc__.split("\n")[0] or ""
            desc = doc and '%s: %s' % (name, doc) or name

            cid = cid + 1
            class_row = self.REPORT_CLASS_TMPL % dict(
                style=no_error > 0 and 'errorClass' or no_fail > 0 and 'failClass' or 'passClass',
                desc=desc,
                count=no_pass + no_fail + no_error + no_skip,
                Pass=no_pass,
                fail=no_fail,
                error=no_error,
                cid='c%s' % cid,
            )
            rows.append(class_row)

            for tid, (result_code, tc, stdout, stderr, cost) in enumerate(cls_results):
                test_row = self._generate_report_test(cid, tid, result_code, tc, stdout, stderr, cost)
                rows.append(test_row)

        report_data = dict(
            test_list=''.join(rows),
        )
        report_data.update(result_summary)
        report = self.REPORT_TMPL % report_data

        return report

    def _generate_report_test(self, cid, tid, result_code, tc, stdout, stderr, cost=0):
        # e.g. 'pt1.1', 'ft1.1', etc
        if_success = result_code in (0, 3)
        # ID修改点为下划线,支持Bootstrap折叠展开特效 - Findyou
        if result_code == 3:
            tid = 'skip' + '_tc_%s_%s' % (cid, tid + 1)
            tmpl = self.REPORT_TEST_SKIP_TMPL
        else:
            tid = (result_code == 0 and 'pass' or (result_code == 1 and 'fail' or 'error')) + '_tc_%s_%s' % (
                cid, tid + 1)
            tmpl = if_success and self.REPORT_TEST_SUCCESS_TMPL or (
                    result_code == 1 and self.REPORT_TEST_FAIL_TMPL or self.REPORT_TEST_ERROR_TMPL)
        name = tc.id().split('.')[-1]
        doc = tc.shortDescription() or ""
        desc = doc and ('%s: %s' % (name, doc)) or name

        # utf-8 支持中文 - Findyou
        # o and e should be byte string because they are collected from stdout and stderr?
        if isinstance(stdout, str):
            # TODO: some problem with 'string_escape': it escape \n and mess up formating
            # uo = unicode(o.encode('string_escape'))
            uo = stdout
        else:
            uo = stdout
        if isinstance(stderr, str):
            # TODO: some problem with 'string_escape': it escape \n and mess up formating
            # ue = unicode(e.encode('string_escape'))
            ue = stderr
        else:
            ue = stderr
        output = uo + ue
        if output:
            script = self.REPORT_TEST_OUTPUT_TMPL % dict(
                id=tid,
                output=saxutils.escape(uo + ue),
            )
        else:
            script = output

        row = tmpl % dict(
            tid=tid,
            Class=(result_code == 0 and 'hiddenRow'),
            style=result_code == 2 and 'errorCase' or (result_code == 1 and 'failCase' or 'passCase'),
            desc=desc,
            script=script,
            status=self.STATUS[result_code],
            cost=cost,
        )
        return row

    def _generate_ending(self):
        return self.ENDING_TMPL


# -------------------- The end of the Template class -------------------

def generate_report(file_stream, result_data: dict):
    Template_mixin().generate_report(file_stream, result_data)
