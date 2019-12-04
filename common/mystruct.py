import collections
import json


class Struct(dict):
    def __init__(self, input_dict):
        '''
        # 将json或dict类型的对象的key,value转为可以通过object.key方法获取的属性
        # 注：支持实例化后的字典赋值能通过属性获取到，反之，通过给属性赋值，也能通过字典的方式获取
        :param input_dict: 支持任意的继承自collections.Mapping的类型，如：tuple, list, set, frozenset
        '''

        json_dict = {}
        # 如果初始化时传入的对象本身就是struct对象，则将其_json_dict对象赋值给新实例的_json_dict属性
        if isinstance(input_dict, Struct):
            json_dict = input_dict
        elif isinstance(input_dict, collections.Mapping):
            json_dict = input_dict
        else:
            try:
                json_dict = json.loads(input_dict)
            except:
                raise ValueError('input must be a dict or valid json string')
        self.update(json_dict)

        # 递归将字典里的值转化为对象里的属性
        for name, value in self.items():
            setattr(self, name, self._wrap(value))

    def __setitem__(self, key, value):
        '''
        自定义__setitem__，使通过字典方式赋值时，也给属性赋值
        :param key: 字典key
        :param value: 字典值
        :return: 无
        '''
        self.update({str(key): value})
        setattr(self, key, self._wrap(value))

    def __setattr__(self, key, value):
        '''
        自定义__setattr__，使通过属性赋值时，也给更新字典
        :param key: 字典key
        :param value: 字典值
        :return: 无
        '''
        self.update({str(key): value})
        super().__setattr__(key, self._wrap(value))

    def _wrap(self, value):
        if isinstance(value, (tuple, list, set, frozenset)):
            return type(value)([self._wrap(v) for v in value])
        else:
            if isinstance(value, collections.Mapping):
                return Struct(value)
            else:
                return value
