**开发环境准备**

安装python：需要3.6以上的版本

安装开发工具：推荐pycharm

安装Git：https://git-scm.com/download

安装好Git后，配置用户名和用户邮箱

git config --global user.name "your_name"

git config --global user.email "your_email@gmail.com"

# 把Git设置成大小写敏感

git config core.ignorecase false

注：Git默认是大小写不敏感的，也就是说，将一个文件名或文件夹名做了大小写的修改，Git是忽略这个改动的，这样会导致在同步代码时候会出现错误，把Git设置成大小写敏感

# 本自动化框架的目标运行环境是linux和windows系统，所以请保持core.autocrlf=ture

操作命令：git config core.autocrlf true

关于windows和linux系统提交代码的兼容问题：

windows下的换行符为crlf（即\r\n），liunx和mac系统的换行符为lf（即\n）

Git默认配置中的core.autocrlf=ture，含意检出时将lf转化为crlf，提交时再将crlf转为lf，目的是在windows下开发时自动兼容在linux上开发和运行的工程

如果是运行在windows server操作系统的工程（如.net工程），则要关闭自动转换

即：git config core.autocrlf false

# 请不要将TestResult和TestLog提交至git仓库

为了避免误操作，最好在.gitignore中将其忽略掉

# 免密提交代码

需要生成密钥对，提供公钥给远程仓库，本地保留私钥

首先：ls ~/.ssh/

如果已经生成过密钥对，在本地的/Users/当前电脑用户/.ssh目录下会有两个文件id_rsa、id_rsa.pub，其中id_rsa文件保存的是私钥，保存于本地，id_rsa.pub文件保存的是公钥，需要将里面内容添加到远端仓库。

用下面的命令生产密钥对（如果本地已有，不需要再次生成）：

ssh-keygen -t rsa -C "yourname@youremail.com"

**自动化框架设计**

conf下面放所有的配置文件

conf/config.py封装了读取Config的类和方法，采用单例加工厂的模式，各业务的Config类会依次读取global.cfg和相应业务的xxx.cfg里的内容

global.cfg里面的配为全局配置，其他配置文件中的配置会继承和覆盖global.cfg里的配置

common下面放所有的公共方法

common/helper.py: 里是常用的公共方法，如生成随机串，计算文件md5，字符串加密等

patch.py: 核心，针对unittest框架的增强实现都在这个文件中，包括：

1. 在运行时对测试用例按照书写顺序进行编号

2. 支持通过指定tag和priority过滤测试用例，需事先对测试用例标记tag和priority

3. 测试数据装饰器，用来帮助测试用例从外部文件读入测试数据

log.py: 封装了初始化logger的方法

runner.py: 核心，测试执行入口

测试用例管理

测试用例统一放到TestCase下面

按照业务和功能模块分类，不同的人可以开发不同的测试，做到互不影响

测试数据管理

总体上将测试数据分为两类：参数变量和数据文件

参数变量：放到.cfg配置文件中，参数变量会因测试环境的不同而变化，所以配置文件应该有多份，每个环境一份，存储指定环境下的参数值

数据文件：统一放到TestData文件夹下，尽量不要频繁改动TestData文件夹下的文件，因为git对每次改动都保留副本，频繁改动数据文件会导致git占用空间过多

**测试执行**

有两种方式来指定测试环境： 

1. 先切换环境，再执行测试，切换环境命令：python conf/config.py {env}，这个会把默认配置文件的内容替换为指定环境的

2. 通过HtmlRunner.py执行时传入-e参数，这个会设置config中的ENV变量，读取指定环境的配置文件

为了方便灵活的执行测试用例，封装了HtmlRunner.py做为执行测试用例的入口，使用示例如下：

python HtmlRunner.py tests/demo_tests -p *test.py -e dev --mail buweiqiang@civaonline.cn --ding dingding-robot-token --notice 1

第一个参数tests/demo_tests是指定测试用例所在的文件夹
参数-p 含义是指定测试用例文件名的匹配格式 （非必填，默人为*test.py）
参数-e 含义是指定测试执行的环境 （非必填）
参数--mail 含义是指定测试报告邮件的接收人（非必填，默认为不发送邮件）
参数--ding 含义是指定钉钉通知机器人的token （非必填，默认为不发送钉钉提醒）
参数--notice 含义是设定发送邮件和钉钉提醒场景 （非必填，1 = 只有失败时发送, 2 = 成功和失败都发送, 默认为1）
参数--style，通过该参数可以指定输出测试报告的样式，目前支持4种样式，参数取值范围为[1,2,3,4]，默认为样式1

**命名规范**

测试用例：都遵守*_test.py的命名规则

测试方法：都遵守test_开头的规则

文件名：全小写,可使用下划线

模块：应该是简短的、小写的名字。如果下划线可以改善可读性可以加入。如mypackage或my_package。

类：总是使用驼峰命名法。如MyClass。内部类可以使用额外的前导下划线。

函数&方法：函数名应该为小写，可以用下划线风格单词以增加可读性。如：myfunction，my_example_function。

*注意*：方法名采用getLogger这种混合大小写仅被允许用于这种风格已经占据优势的时候，以便保持向后兼容。


**依赖包安装**

首先确保已经安装了pip，如果没有，请尝试：sudo easy_intall pip
或者用下面的方式安装pip:
$ curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py   # 下载安装脚本
$ sudo python get-pip.py    # 运行安装脚本

一键安装所有需要的包（所需要安装的包都在requirements.txt中）

pip3 install -r requirement.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/

指定国内的源安装包会很快：pip install -i https://pypi.tuna.tsinghua.edu.cn/simple/ package_name
出错请尝试：pip install --trusted-host https://pypi.tuna.tsinghua.edu.cn/simple/ package_name

网上找到的国内源：
http://pypi.douban.com/simple/  豆瓣
http://pypi.hustunique.com/simple/  华中理工大学
http://pypi.sdutlinux.org/simple/  山东理工大学
http://pypi.mirrors.ustc.edu.cn/simple/  中国科学技术大学
http://pypi.v2ex.com/simple/simple/
http://mirrors.aliyun.com/pypi/simple/ 阿里云

requests是必装的包：pip install requests
上传文件可安装requests帮助包requests-toolbelt: pip install requests-toolbelt

加解密需要安装pycrypto，但是pycrypto已经停止维护了，不推荐再用了，而且windows环境依赖Microsoft VC++ build tool才能安装成功
推荐安装pycryptodome，是pycrypto的延伸版，而且没有过分的依赖，十分好用:
pip install pycryptodome
安装完成后找到这个路径Python\Python36\Lib\site-packages，下面有一个文件夹叫做crypto,将小写c改成大写C就ok了。

如果缺少其他的包，安装方法同上pip install package_name

升级包：pip install --upgrade package_name

卸载包：pip uninstall package_name

如果测试websocket长链接需要安装websocket-client，注意，不是websocket

pip install websocket-client

解析网页内容推荐安装BeautifulSoup4(bs4)，可选，只有很少的case用到

pip install beautifulsoup4

或先从这里下载：htps://www.crummy.com/software/BeautifulSoup/bs4/download/

再安装：python setup.py install

据说如果安装了lxml，beautifulsoup4解析html的效率会更好，可以选择性安装lxml

easy install lxml

数据库操作推荐安装mysql-connector:

pip install mysql-connector==2.1.4

或从git下载安装mysql-connector-python

$  git clone https://github.com/mysql/mysql-connector-python.git

$  cd mysql-connector-python

$  python ./setup.py build

$  sudo python ./setup.py install

**关于生成protobuf代码文件**

speechgw下的proto文件如果有更新，所依赖的protobuf文件通过执行lib/speech目录下的protobuf_generate.py生成

python protobuf_generate.py

注：以后会将脚本升级，做到自动从gitlab接取最新的proto文件，然后生成相应的protobuf

**关于pyopenssl**

有同学经常遇到https请求报ssl相关的Error，安装pyopenssl后有可能解决问题：sudo pip install pyopenssl

如果pip安装不成功，可以尝试下载tar包可whl包安装，我目前用的版本是：https://pypi.python.org/pypi/pyOpenSSL/16.2.0

下载tar包后解压，到解压目录，执行安装：sudo python setup.py install

whl包安装需先安装wheel: sudo pip install wheel

wheel安装成功后可以安装whl包： sudo pip install xxx.whl

python3.6遇到wss报错：[SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed (_ssl.c:841) 的解决方法：
pip install --upgrade certifi

python3.6遇到wss报错：[SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed (_ssl.c:847) 的解决方法：
sudo /Applications/Python\ 3.6/Install\ Certificates.command

**关于分支管理**

与研发的上线流程类似：dev分支可以持续提交新的测试代码，只有稳定通过的测试代码才会到master分支

应用持续集成后，会每天执行自动化测试dev分支，dev分支上通过的测试代码会自动reset到master分支，不通过则不会reset

为了保证master的稳定性，初级测试开发只能提代码到dev分支，不能合代码，统一由高级测试开发将dev代码合并至master分支


