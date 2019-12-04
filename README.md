# 介绍
此工程取名叫AutotestCornerstone，意在于提供一个自动化测试的基础框架工程，其中包含了众多的自动化测试需要用到的基础功能，下载下来编写测试用例即可，解决了入门同学不知道如何设计测试框架的痛苦。

有能力的同学可以在此基础框架的上进行一些修改，以符合自己所在公司和团队的需求。

主要功能有：

## 多测试环境支持
- 一份测试用例，多测试环境运行（如开发，测试，预发，生产）
- 为不同的测试环境准备不同的配置
- 快速切换测试环境，两种方法

    - 先切换环境，再执行测试（推荐）
        切换环境命令：
        ```
        python conf/config.py {env}
        ```
    - 执行时传入环境参数
        通过runner.py执行时传入-e参数

## TestData装饰器
- 测试数据与代码分离，避免hardcode
- 支持不同的测试环境，准备不同的测试数据
- 通过TestData装饰器获取，简单易行
- 支持ini, json, xml三种数据表达方式
    ```python
    from patch import TestData
    class Test(unittest.TestCase):
        @TestData
        def test_get_data1(self, dataobj):
            '''获取测试数据1'''
            print('index={}'.format(dataobj['index']))
            print('video_id={}'.format(dataobj['video_id']))
    ```

## 测试用例筛选和过滤
- 支持对测试用例标记Tag
- 支持对测试用例标记Priority
- 通过runner.py传入-t/--tag和--priority参数进行过滤
    ```python
    from patch import Tag, Priority
    class Test(unittest.TestCase):
        @Tag('demo')
        @Tag('smoke')
        @Priority(2)
        def test_cccc(self):
            print('cccc')
        
        @Tag('demo', 'smoke')
        @Priority(1)
        def test_aaaa(self):
            print('aaaa')
    ```

## 测试用例按书写顺序编号和执行
- 非侵入式的设计，无需修改原来的测试用例
- 在运行时对测试用例按照书写顺序进行编号（例如test_00001_case_name）
- 通过runner.py传入--index参数指定
- 这个实现参照了utx作者的实现：https://github.com/jianbing/utx.git

## 支持4种样式的测试报告
- 通过runner.py传入--style参数指定
- 在report_style文件夹中有样例，可供查看
- 其中style3和style4是从utx作者那里拿过来的，再次感谢utx作者

## 其它
- 支持邮件发送测试报告
- 支持将测试结果发送至dingding群
- 支持删除过期的测试报告和日志文件（默认30天）
- 支持自定义测试报告名称
- 支持在测试报告中插入链接（目前中在style1中实现了支持）

# 自动化测试框架设计

## 核心文件
patch.py: 核心，针对unittest框架的增强实现都在这个文件中，包括：

1. 在运行时对测试用例按照书写顺序进行编号

2. 支持通过指定tag和priority过滤测试用例，需事先对测试用例标记tag和priority

3. 测试数据装饰器，用来帮助测试用例从外部文件读入测试数据

runner.py: 核心，测试执行入口

conf/config.py 封装了读取Config基类和方法，实现了快速切换测试环境

## 配置文件

所有的配置文件都在conf下面

conf/config.py 封装了读取Config基类和方法，实现了快速切换测试环境

global.cfg里面的配为全局配置，其他配置文件中的配置会继承和覆盖global.cfg里的配置

conf下的配置文件按照产品进行分类，产品的配置文件可以覆盖global.cfg里面的配置

产品配置文件夹中的__init__.py中继承Config基类，实现对产品配置文件的读取

## 公共方法

公共方法都放到common下面

common/helper.py: 里是常用的公共方法，如生成随机串，计算文件md5，字符串加密等

## 测试用例管理

测试用例统一放到TestCase下面

按照产品和功能模块分类，不同组的人可以开发不同的测试用例，做到互不影响

## 测试数据管理

总体上将测试数据分为两类：参数变量和文件数据

参数变量：

- 放到conf配置文件中，参数变量会因测试环境的不同而变化，所以配置文件应该有多份，每个环境一份，存储指定环境下的参数值
- 放到与测试用例同名的测试数据文件中，通过TestData装饰器获取

文件数据：统一放到TestData文件夹下，尽量不要频繁改动TestData文件夹下的文件，因为git对每次改动都保留副本，频繁改动数据文件会导致git占用空间过多

## 测试执行

为了方便灵活的执行测试用例，封装了runner.py做为执行测试用例的入口，使用示例如下：
```angular2
python runner.py tests/demo_tests -p *test.py -e dev --mail buweiqiang@civaonline.cn --ding dingding-robot-token --notice 1
```
第一个参数必填，是指定查找测试用例的文件夹

其它参数都是选填的：

- 参数-p 含义是指定测试用例文件名的匹配格式 （非必填，默人为*test.py）
- 参数-e 含义是指定测试执行的环境 （非必填）
- 参数--mail 含义是指定测试报告邮件的接收人（非必填，默认为不发送邮件）
- 参数--ding 含义是指定钉钉通知机器人的token （非必填，默认为不发送钉钉提醒）
- 参数--notice 含义是设定发送邮件和钉钉提醒场景 （非必填，1 = 只有失败时发送, 2 = 成功和失败都发送, 默认为1）
- 参数--style 通过该参数可以指定输出测试报告的样式，目前支持4种样式，参数取值范围为[1,2,3,4]，默认为样式1
- 参数-t或--tag 指定要过滤测试用例的tag，只要有一个tag匹配，测试用例将被执行 
- 参数--priority 指定要过滤测试用例的优先级，小于指定优先级的测试用例将不会被执行
- 参数--index 指定对测试用例进行编号，以使其按照书写顺序执行
- 参数--clean 指定清理多少天的测试报告和日志，默认为30天，最小为7天
- 参数--report-url 传入一个链接，此链接会被放入到测试报告中
- 参数--dryrun 只执行加载测试用例至过滤测试用例的过程，并不真正执行测试用例

# 开发环境准备

安装python：需要3.6以上的版本

安装开发工具：推荐pycharm

安装Git：https://git-scm.com/download

## Git配置

### 配置用户名和用户邮箱
```angular2
git config --global user.name "your_name"
git config --global user.email "your_email@gmail.com"
```

### 设置Git为大小写敏感
```angular2
git config core.ignorecase false
```

注：Git默认是大小写不敏感的，也就是说，将一个文件名或文件夹名做了大小写的修改，Git是忽略这个改动的，这样会导致在同步代码时候会出现错误，把Git设置成大小写敏感

### 关于windows和linux系统提交代码的兼容问题

windows下的换行符为crlf（即\r\n），liunx和mac系统的换行符为lf（即\n）

Git默认配置中的core.autocrlf=ture，含意检出时将lf转化为crlf，提交时再将crlf转为lf，目的是在windows下开发时自动兼容在linux上开发和运行的工程

如果是运行在windows server操作系统的工程（如.net工程），则要关闭自动转换
```angular2
git config core.autocrlf false
```

本自动化框架的运行环境支持linux和windows系统，所以请保持git的默认设置core.autocrlf=ture
```angular2
git config core.autocrlf true
```

### 配置.gitignore
请不要将测试结果和日志文件提交至git仓库

为了避免误操作，最好在.gitignore中将TestResult和TestLog文件夹忽略掉

### 免密提交代码

需要生成密钥对，提供公钥给远程仓库，本地保留私钥

首先查看本机是不是已经有密钥对：
```angular2
ls ~/.ssh/
```

如果已经生成过密钥对，在本地的/Users/当前电脑用户/.ssh目录下会有两个文件id_rsa、id_rsa.pub，其中id_rsa文件保存的是私钥，保存于本地，id_rsa.pub文件保存的是公钥，需要将公钥里面内容添加到远端仓库
```angular2
cat ~/.ssh/id_rsa.pub
```

如果没有密钥对，用下面的命令生产密钥对：
```angular2
ssh-keygen -t rsa -C "yourname@youremail.com"
```

# 依赖包安装

首先确保已经安装了pip，如果没有，请尝试：
```angular2
sudo easy_intall pip
```

mac下可以用下面的方式安装pip:
```angular2
$ curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py   # 下载安装脚本
$ sudo python get-pip.py    # 运行安装脚本
```

一键安装所有需要的包（所需要安装的包都在requirements.txt中）
```angular2
pip3 install -r requirement.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/
```

指定国内的源安装包会快很多：
```angular2
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple/ package_name
```
出错请尝试：
```angular2
pip install --trusted-host https://pypi.tuna.tsinghua.edu.cn/simple/ package_name

```
网上找到的国内源：

- http://pypi.douban.com/simple/  豆瓣
- http://pypi.hustunique.com/simple/  华中理工大学
- http://pypi.sdutlinux.org/simple/  山东理工大学
- http://pypi.mirrors.ustc.edu.cn/simple/  中国科学技术大学
- http://pypi.v2ex.com/simple/simple/
- http://mirrors.aliyun.com/pypi/simple/ 阿里云

对于接口测试，requests是必装的包：
```
pip install requests
```
如需上传文件可安装requests帮助包requests-toolbelt: 
```angular2
pip install requests-toolbelt
```
加解密需要安装pycrypto，但是pycrypto已经停止维护了，不推荐再用了，而且windows环境依赖Microsoft VC++ build tool才能安装成功
推荐安装pycryptodome，是pycrypto的延伸版，而且没有过分的依赖，十分好用:
```angular2
pip install pycryptodome
```
如果安装完成后不能用，找到这个路径Python\Python36\Lib\site-packages，下面有一个文件夹叫做crypto,将小写c改成大写C就ok了。

如果缺少其他的包，安装方法同上
```angular2
pip install package_name
```
升级包：
```angular2
pip install --upgrade package_name
```
卸载包：
```angular2
pip uninstall package_name
```

如果测试websocket长链接需要安装websocket-client，注意，不是websocket
```angular2
pip install websocket-client
```
解析网页内容推荐安装BeautifulSoup4(bs4)，可选，只有很少的case用到
```angular2
pip install beautifulsoup4
```
或从这里下载：https://www.crummy.com/software/BeautifulSoup/bs4/download/

据说如果安装了lxml，beautifulsoup4解析html的效率会更好，可以选择性安装lxml
```angular2
easy install lxml
```
数据库操作推荐安装mysql-connector:
```angular2
pip install mysql-connector==2.1.4
```
或从git下载安装mysql-connector-python
```angular2
$  git clone https://github.com/mysql/mysql-connector-python.git

$  cd mysql-connector-python

$  python ./setup.py build

$  sudo python ./setup.py install
```

# 关于https和pyopenssl

有同学经常遇到https请求报ssl相关的Error，安装pyopenssl后有可能解决问题：
```angular2
sudo pip install pyopenssl
```

如果pip安装不成功，可以尝试下载tar包可whl包安装，我目前用的版本是：https://pypi.python.org/pypi/pyOpenSSL/16.2.0

下载tar包后解压，到解压目录，执行安装命令：
```angular2
sudo python setup.py install
```
下载whl包的话，需先安装wheel: 
```angular2
sudo pip install wheel
```
wheel安装成功后可以安装whl包：
```angular2
sudo pip install xxx.whl
``` 
python3.6遇到wss报错：[SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed (_ssl.c:841) 的解决方法：
```angular2
pip install --upgrade certifi
```
python3.6遇到wss报错：[SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed (_ssl.c:847) 的解决方法：
```angular2
sudo /Applications/Python\ 3.6/Install\ Certificates.command
```
