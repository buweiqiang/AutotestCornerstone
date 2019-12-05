import os
import functools
import glob
import unittest

TEST_DATA_ATTR = '__test_data__'
PRIORITY_ATTR = '__priority__'
TAG_ATTR = '__tag__'


class TestDataType:
    ini = 'ini'
    json = 'json'
    xml = 'xml'


data_file_ext = ['ini', 'data', 'cfg', 'json', 'xml']


class dataobject:
    '''
    # 数据模板：
    {
        "xxx_class":
            {
                "xxx_case":
                    {
                        "key1": "value1",
                        "key2": "value2"
                    }
            }
    }
    '''

    def __init__(self, file_name, data_type=TestDataType.ini):
        if not file_name:
            raise ValueError("file_name can't be null or empty")
        if not os.path.exists(file_name):
            raise IOError("file {} not exists".format(file_name))
        self.filename = file_name
        self.data_type = data_type
        self.data = self.loadtestdata()

    def loadtestdata(self):
        # load test data from file, based on data_type
        loader_switcher = {
            'ini': load_test_data_from_ini,
            'json': load_test_data_from_json,
            'xml': load_test_data_from_xml
        }

        load_func = loader_switcher.get(self.data_type)
        if load_func:
            data = load_func(self.filename)
            return data
        else:
            raise NotImplementedError("loader for {} is not implemented".format(self.data_type))

    def gettestcasedata(self, class_name, case_name):
        cls_data = self.data.get(class_name, {})
        case_data = cls_data.get(case_name, {})
        return case_data


class Meta(type):
    '''
    对测试用例按顺序进行编号，如test_00001_case_name
    考虑两种情况：
    1. 先过滤再编号，在编号前先对测试用例进行过滤，只对需要执行的测试用例编号，无需执行的测试用例不编号，保持编号的连续性
    2. 先编号再过滤，只做编号，不做过滤，后续测试用例被过滤后会出现编号不连续
    最终采用方案2，保持单一职责，过滤后导致编号不会连续，这样也好，可以直观的看到多少测试用例被过滤了
    '''

    def __new__(cls, clsname, bases, attrs):
        case_index = 0
        # 从原来的attrs中找出测试用例方法，并对方法进行改名，如test_00001_case_name
        attrs_new = dict()
        # testMethodPrefix=unittest.defaultTestLoader.testMethodPrefix
        testMethodPrefix = 'test_'
        for i in attrs:
            func = attrs[i]
            if i.startswith(testMethodPrefix):
                case_index += 1
                new_func_name = i.replace(testMethodPrefix, "{}{:05d}_".format(testMethodPrefix, case_index))
                attrs_new[new_func_name] = func
            else:
                attrs_new[i] = func

        return super(Meta, cls).__new__(cls, clsname, bases, attrs_new)


DefaultTestCase = unittest.TestCase


def start_indexing_test_cases():
    class _TestCase(unittest.TestCase, metaclass=Meta):
        pass

    unittest.TestCase = _TestCase


def stop_indexing_test_cases():
    unittest.TestCase = DefaultTestCase


def load_test_data_from_ini(file_name):
    import configparser
    data = {}
    config = configparser.RawConfigParser()
    config.read(file_name)
    for section in config.sections():
        _cls, _tc = section.split('.')
        if not _cls in data:
            data[_cls] = {}
        data[_cls][_tc] = dict(config.items(section))
    return data


def load_test_data_from_json(file_name):
    import json
    with open(file_name) as json_file:
        json_data = json.load(json_file)
        return json_data


def load_test_data_from_xml(file_name):
    import xml.etree.ElementTree as ET
    xml_dict = {}
    xtree = ET.parse(file_name)
    root = xtree.getroot()
    for cls_node in root.findall('testclass'):
        cls_name = cls_node.attrib['name']
        xml_dict[cls_name] = {}
        for tc_node in cls_node:
            tc_name = tc_node.attrib['name']
            xml_dict[cls_name][tc_name] = {}
            for kv in tc_node:
                xml_dict[cls_name][tc_name][kv.tag] = kv.text

    return xml_dict


def discover_test_data_file(py_file_name, env):
    file_name = ''
    # 通过splitext拿到去除后缀的数据文件名
    _name, _ext = os.path.splitext(py_file_name)

    # 找到所有符合条件的数据文件
    if env:
        # 优先使用符合环境参数的数据文件
        path_format = "{}.{}.*".format(_name, env)
        find_result = glob.glob(path_format)
        if find_result and len(find_result) > 0:
            file_name = os.path.abspath(find_result[0])

    # 如果未找到相应的数据文件，使用默认规则查找数据文件
    if not file_name:
        for ext in data_file_ext:
            default_file = "{}.{}".format(_name, ext)
            if os.path.exists(default_file):
                file_name = os.path.abspath(default_file)
                break

    # 如果仍未找到相应的数据文件，抛出异常
    # if not file_name:
    #    raise FileNotFoundError("data file for {} not found".format(py_file_name))

    # 数据文件类型默认是ini
    data_type = TestDataType.ini
    # 根据文件后缀最终确定文件的类型
    f_name, f_ext = os.path.splitext(file_name)
    if "json" in f_ext:
        data_type = TestDataType.json
    if "xml" in f_ext:
        data_type = TestDataType.xml

    return file_name, data_type


def Priority(value: int):
    '''
    给测试用例加优先级标签，不加此注释的用例优先级默认为4，用法举例：
    @Priority(3)
    def test_002_began_show(self):
        """开始表演:ebookid为空"""
        # action
        r = self.robot_app.play_show.began01_show(ebookId="")
        # #assert
        self.assertEqual(r['returnNo'], '0013')
        self.assertEqual(r['returnInfo'], '参数不全哦')

    :param value: 优先级，支持0~4的整数
    :return: 附加了属性后的testmethod
    '''

    def decorator(testmethod):
        if not hasattr(testmethod, PRIORITY_ATTR):
            # Priority属性只支持指定一次
            setattr(testmethod, PRIORITY_ATTR, value)
        return testmethod

    return decorator


def Tag(*value: str):
    '''
    给测试用例加标签，在执行时可以以根据标签进行过滤，用法举例：
    @Tag('show', 'civa')
    @Tag('smoke')
    def test_003_began_show(self):
        """开始表演:ebookid错误"""
        # action
        r = self.robot_app.play_show.began01_show(ebookId="123")
        # #assert
        self.assertEqual(r['returnNo'], '0000')
        self.assertEqual(r['returnInfo'], 'oh yeah,通过了')

    :param value: 标签，支持添加多个
    :return: 附加了属性后的testmethod
    '''

    def decorator(testmethod):
        if not hasattr(testmethod, TAG_ATTR):
            tags = []
            tags.extend(value)
            setattr(testmethod, TAG_ATTR, tags)
        else:
            tags = getattr(testmethod, TAG_ATTR)
            tags.extend(value)
        return testmethod

    return decorator


def TestData(testmethod):
    """
    decorator of test method
    :param testmethod: the original method which has been decorated
    :return: a test method with a test data object
    """
    try:
        from conf.config import ENV
    except ImportError:
        # 如果从配置文件中读取环境变更失败，则默认ENV=None
        ENV = None

    @functools.wraps(testmethod)
    def testdata_wrapper(*args, **kwargs):
        tc_data = {}
        if len(args) > 0:
            # print('data2: {}'.format(args[0].__class__.__dict__))
            # print('data test name: {}'.format(args[0]._testMethodName))
            # print("data module name: {}".format(args[0].__module__))
            # module_name = testmethod.__module__
            func_code = testmethod.__code__
            class_name = args[0].__class__.__name__
            case_name = testmethod.__name__

            # find the data file which has the same name with module name
            data_file, data_type = discover_test_data_file(func_code.co_filename, ENV)

            # load test data from the data_file
            if data_file:
                data = dataobject(data_file, data_type)
                # get key/value list for test case, append to args
                tc_data = data.gettestcasedata(class_name, case_name)
            else:
                # 如果未找到datafile，抛出异常，或读取conf/testdata.cfg
                raise FileNotFoundError("data file for {} not found".format(func_code.co_filename))
                # tc_data = load_test_data_from_cfg(os.path.basename(func_code.co_filename), class_name, case_name)

        args += (tc_data,)
        setattr(testmethod, TEST_DATA_ATTR, f'{data_file}.{data_type}')
        return testmethod(*args, **kwargs)

    return testdata_wrapper


def filter_tests(testsuite, priority, tags):
    # 递归遍历suite中的tests，过滤需要执行的测试用例
    def _filter_tests(testsuite, depth=0):
        prefix = '- ' * depth
        print(f'{prefix}+ {testsuite.countTestCases()}')

        reserved_tests = []
        for s in testsuite:
            if isinstance(s, unittest.TestSuite):
                # 如果子节点仍然是TestSuite类型，代表是容器，下面仍有子节点
                sub_depth = depth + 1
                subtests = _filter_tests(s, sub_depth)
                # 经过滤后，如子节点不为空，则将其追加到保留的测试列表中
                if len(subtests) > 0:
                    reserved_tests.append(s)
            else:
                # 当子条目不是TestSuite类型是，s的类型为具体的测试类(继承自TestCase)
                # 每一个测试方法都被化为测试类的实例，可以通过_testMethodName获取到方法名
                # 获取testcase的方法名
                testMethodName = getattr(s, '_testMethodName')
                # 根据方法名获取实际的方法func
                testMethod = getattr(s, testMethodName)

                # 获取装饰在方法上的priority属性，默认优化先级最低为4
                priority_attr = getattr(testMethod, PRIORITY_ATTR, 4)
                # 判断用例priority是否小于指定的priority条件
                priority_match = int(priority_attr) <= priority

                # 判断tag是否符合
                # 获取装饰在方法上的tag属性，默认为空列表
                tag_attr = getattr(testMethod, TAG_ATTR, [])
                # 判断tag是否符合：
                # 1 没有指定tag，则默认为True
                # 2 case的tag与指定的tag是否有交集，即只要其中一个tag match即为符合条件
                tag_match = True if not tags else set(tags).intersection(tag_attr)

                # 定义输出标记，对于符合过滤条件(需同时满足priority和tag条件)的，标记为m
                label = '-'
                if priority_match and tag_match:
                    label = 'm'
                    reserved_tests.append(s)
                print(f'{prefix}  {label} p{priority_attr} {testMethodName} (tag={tag_attr})')

        testsuite._tests = reserved_tests
        return reserved_tests

    _filter_tests(testsuite)

    return testsuite


if __name__ == '__main__':
    f, t = discover_test_data_file(r'..\tests\media_tests\media_test.py', 'test')
    print(f, t)
