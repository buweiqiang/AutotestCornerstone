# coding=utf-8
import sys
import re
import string
import csv
import errno
import os
import random
import time
import hashlib
import shutil
import json
import base64
from uuid import uuid4

from datetime import datetime

if sys.version > '3':
    PY3 = True
else:
    PY3 = False


def get_uuid():
    return uuid4().hex


def random_select_files(target_dir, count, loop_subfolders=False):
    if count < 1:
        raise ValueError('Invalid parameter "count", should > 0')
    file_names = []
    if loop_subfolders:
        for root, dirs, files in os.walk(target_dir):
            file_paths = [os.path.join(root, f) for f in files]
            file_names.extend(file_paths)
    else:
        file_names = [os.path.join(target_dir, f) for f in os.listdir(target_dir) if
                      os.path.isfile(os.path.join(target_dir, f))]

    random_files = random.sample(file_names, count)
    return random_files


def random_select_file(target_dir, count, loop_subfolders=False):
    file_names = []
    if loop_subfolders:
        for root, dirs, files in os.walk(target_dir):
            file_paths = [os.path.join(root, f) for f in files]
            file_names.extend(file_paths)
    else:
        file_names = [os.path.join(target_dir, f) for f in os.listdir(target_dir) if
                      os.path.isfile(os.path.join(target_dir, f))]
    filename = random.choice(file_names)
    return filename


def random_select_files_with_size_limit(target_dir, count, size_limit_mb=10):
    if count < 1:
        raise ValueError('Invalid parameter "count", should > 0')
    file_names = [os.path.join(target_dir, f) for f in os.listdir(target_dir) if
                  os.path.isfile(os.path.join(target_dir, f))]
    file_names = [f for f in file_names if os.path.getsize(f) < size_limit_mb * 1024 * 1024]
    random_files = random.sample(file_names, count)
    return random_files


def random_select_file_with_size_limit(target_dir, size_limit_mb=10):
    file_names = [os.path.join(target_dir, f) for f in os.listdir(target_dir) if
                  os.path.isfile(os.path.join(target_dir, f))]
    file_names = [f for f in file_names if os.path.getsize(f) < size_limit_mb * 1024 * 1024]
    random_file = random.choice(file_names)
    return random_file


def random_select_files_with_size_limit_min_max(target_dir, count=1, size_limit_max=20, size_limit_min=10):
    if count < 1:
        raise ValueError('Invalid parameter "count", should > 0')
    file_names = [os.path.join(target_dir, f) for f in os.listdir(target_dir) if
                  os.path.isfile(os.path.join(target_dir, f))]
    file_names = [
        f for f in file_names if size_limit_min * 1024 * 1024 < os.path.getsize(f) < size_limit_max * 1024 * 1024]
    random_files = random.sample(file_names, count)
    return random_files


def random_select_file_with_size_limit_min_max(target_dir, size_limit_max=20, size_limit_min=10):
    file_names = [os.path.join(target_dir, f) for f in os.listdir(target_dir) if
                  os.path.isfile(os.path.join(target_dir, f))]
    file_names = [
        f for f in file_names if size_limit_min * 1024 * 1024 < os.path.getsize(f) < size_limit_max * 1024 * 1024]
    random_file = random.choice(file_names)
    return random_file


def list_compare(actual_list, expected_list):
    # 找出少的
    less = set(expected_list).difference(set(actual_list))
    # 找出多的
    more = set(actual_list).difference(set(expected_list))
    # 返回结果第一个是少了的，第二个是多了的
    return less, more


def get_random_string(length):
    ret = ''
    char = string.ascii_lowercase + string.digits + string.ascii_uppercase
    for i in range(length):
        ret += random.choice(char)
    return ret


def get_random_name(prefix="autotest"):
    name = '%s_%s_%s' % (prefix, get_random_string(3), get_current_time_string('%Y%m%d%H%M%S'))
    return name


def make_dir(path):
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


def delete_dir(file_path):
    try:
        shutil.rmtree(file_path)
    except OSError:
        pass


# 获取字符串的md5加密
def get_str_md5(str):
    if type(str) is not bytes:
        str = str.encode('utf-8')
    m = hashlib.md5()
    m.update(str)
    return m.hexdigest()


# 读取文件的md5值
def get_file_md5(filename):
    hashmethod = hashlib.md5()
    fp = open(filename, "rb")
    f_size = os.stat(filename).st_size

    _FILE_SLIM = (1 * 1024 * 1024)
    while (f_size > _FILE_SLIM):
        hashmethod.update(fp.read(_FILE_SLIM))
        f_size -= _FILE_SLIM
    if f_size > 0:
        hashmethod.update(fp.read())

    return hashmethod.hexdigest()


def aes_encrypt_cbc(text, key, iv, block_size=16):
    '''
    这里密钥长度必须为16（AES-128）,24（AES-192）,或者32 （AES-256）Bytes 长度
    需要将传入的text,key,iv都转为bytes类型，否则在python3.6中会报错：TypeError: Object type <class 'str'> cannot be passed to C code
    :param text: 需加密的文本
    :param key: 密钥
    :param iv: 模式为CBC时，需指定偏移量
    :param block_size: 可以是8,16,32,64
    :return: bytes，加密后的数据为byte数组
    '''
    from Crypto.Cipher import AES
    if not isinstance(key, bytes):
        key = key.encode('utf-8')
    if not isinstance(iv, bytes):
        iv = iv.encode('utf-8')
    btext = pkcs7_pad(text, block_size).encode()
    cryptor = AES.new(key, AES.MODE_CBC, iv)
    encrypt_bytes = cryptor.encrypt(btext)
    return encrypt_bytes


def aes_encrypt_ecb(text, key, block_size=16):
    '''
    aes encrypt with ecb mode
    :param text: text to encrypt
    :param key: key size should be times of 8
    :param block_size: block size
    :return: bytes，加密后的数据为byte数组
    '''
    from Crypto.Cipher import AES
    if not isinstance(key, bytes):
        key = key.encode('utf-8')
    btext = pkcs7_pad(text, block_size).encode('utf-8')
    cryptor = AES.new(key, AES.MODE_ECB)
    encrypt_bytes = cryptor.encrypt(btext)
    return encrypt_bytes


def aes_decrypt_ecb(text, key):
    from Crypto.Cipher import AES
    if not isinstance(text, bytes):
        text = text.encode('utf-8')
    if not isinstance(key, bytes):
        key = key.encode('utf-8')
    cryptor = AES.new(key, AES.MODE_ECB)
    decrypt_bytes = cryptor.decrypt(text)
    # 处理解密后的padding字符：难道不是decrypt方法自动处理的吗？
    last_byte = decrypt_bytes[-1:]
    padding_length = ord(last_byte)
    if decrypt_bytes.endswith(last_byte * padding_length):
        decrypt_bytes = decrypt_bytes[:0 - padding_length]
    return decrypt_bytes


def aes_decrypt_cbc(text, key, iv):
    '''
    这里密钥长度必须为16（AES-128）,24（AES-192）,或者32 （AES-256）Bytes 长度
    需要将传入的text,key,iv都转为bytes类型，否则在python3.6中会报错：TypeError: Object type <class 'str'> cannot be passed to C code
    :param text: 需加密的文本
    :param key: 密钥
    :param iv: 模式为CBC时，需指定偏移量
    :param block_size: 可以是8,16,32,64
    :return: bytes，加密后的数据为byte数组
    '''
    from Crypto.Cipher import AES
    if not isinstance(text, bytes):
        text = text.encode('utf-8')
    if not isinstance(key, bytes):
        key = key.encode('utf-8')
    if not isinstance(iv, bytes):
        iv = iv.encode('utf-8')
    cryptor = AES.new(key, AES.MODE_CBC, iv)
    decrypt_bytes = cryptor.decrypt(text)
    return decrypt_bytes


def des3_encrypt_cbc(text, key, iv=None, block_size=16):
    '''
    des加密只支持block_size=8，des3支持block_size为16，32，64
    :param text: 需加密的文本
    :param key: 密钥
    :param iv: 模式为CBC时，需指定偏移量
    :param block_size: des3支持block_size为16，32，64
    :return: bytes，加密后的数据为byte数组
    '''
    from Crypto.Cipher import DES3
    key = key.encode()
    btext = pkcs7_pad(text, block_size).encode()
    if iv:
        iv = iv.encode()
        cryptor = DES3.new(key, DES3.MODE_CBC, iv)
    else:
        cryptor = DES3.new(key, DES3.MODE_CBC)
    encrypted_bytes = cryptor.encrypt(btext)
    return encrypted_bytes


def des3_encrypt_ecb(text, key, block_size=16):
    '''
    des加密只支持block_size=8，des3支持block_size为16，32，64
    :param text: 需加密的文本
    :param key: 密钥
    :param block_size: des3支持block_size为16，32，64
    :return: bytes，加密后的数据为byte数组
    '''
    from Crypto.Cipher import DES3
    key = key.encode()
    btext = pkcs7_pad(text, block_size).encode()
    cryptor = DES3.new(key, DES3.MODE_ECB)
    encrypt_bytes = cryptor.encrypt(btext)
    return encrypt_bytes


# 公钥加密
def rsa_encrypt_by_public_key(text, public_key):
    '''
    公钥加密
    :param text:
    :param public_key: rsa_key (RSA.RsaKey or string or byte string):
    :return:
    '''
    from Crypto.PublicKey import RSA
    from Crypto.Cipher import PKCS1_v1_5 as PKCS1_chiper

    if not type(public_key) is RSA.RsaKey:
        public_key = load_rsa_pubkey_from_str(public_key)

    if isinstance(text, str):
        text = text.encode()

    encrypted_bytes = b''
    try:
        cipher = PKCS1_chiper.new(public_key)
        block_reversed_size = 11
        block_size = get_rsa_block_size(public_key) - block_reversed_size
        for i in range(0, len(text), block_size):
            block = text[i:i + block_size]
            cur_text = cipher.encrypt(block)
            encrypted_bytes += cur_text
    except Exception as err:
        print('RSA公钥加密失败', err)
    return encrypted_bytes


# 私钥解密
def rsa_decrypt_by_private_key(text, private_key):
    '''
    # 私钥解密
    :param text:
    :param private_key: rsa_key (RSA.RsaKey or string or byte string):
    :return:
    '''
    from Crypto.PublicKey import RSA
    from Crypto.Cipher import PKCS1_v1_5 as PKCS1_chiper

    if not type(private_key) is RSA.RsaKey:
        private_key = load_rsa_prikey_from_str(private_key)
    block_size = get_rsa_block_size(private_key)

    if isinstance(text, str):
        text = text.encode()

    decrypted_bytes = b''
    try:
        cipher = PKCS1_chiper.new(private_key)
        for i in range(0, len(text), block_size):
            block = text[i:i + block_size]
            cur_text = cipher.decrypt(block, '')
            decrypted_bytes += cur_text
    except Exception as err:
        print('RSA私钥解密失败', err)
    return decrypted_bytes


# 私钥加密
def rsa_encrypt_by_private_key(data, private_key):
    # todo: 实现私钥加密的代码，下面的代码还有问题
    raise NotImplementedError('实现私钥加密的代码，下面的代码还有问题')
    from rsa import transform, core
    from Crypto.PublicKey import RSA

    def encrypt(data_bytes, rsa_private_key):
        data_int = transform.bytes2int(data_bytes)
        encrypted_int = core.encrypt_int(data_int, rsa_private_key.e, rsa_private_key.n)
        block = transform.int2bytes(encrypted_int)
        return block

    encrypted_text = b''
    if isinstance(data, str):
        data = data.encode()
    if not type(private_key) is RSA.RsaKey:
        private_key = load_rsa_prikey_from_str(private_key)
    block_reversed_size = 11
    block_size = get_rsa_block_size(private_key) - block_reversed_size
    try:
        for i in range(0, len(data), block_size):
            block = data[i:i + block_size]
            cur_text = encrypt(block, private_key)
            encrypted_text += cur_text
    except Exception as err:
        print('RSA私钥加密失败', err)
    return encrypted_text


# 公钥解密
def rsa_decrypt_by_public_key(data, public_key):
    from rsa import transform, core
    from Crypto.PublicKey import RSA

    def decrypt(encrypted_bytes, rsa_public_key):
        # public_key = PublicKey.load_pkcs1(rsa_public_key)
        encrypted = transform.bytes2int(encrypted_bytes)
        decrypted_int = core.decrypt_int(encrypted, rsa_public_key.e, rsa_public_key.n)
        decrypted_bytes = transform.int2bytes(decrypted_int)
        if len(decrypted_bytes) > 0 and decrypted_bytes[0] == 1:
            pos = decrypted_bytes.find(b'\x00')
            if pos > 0:
                return decrypted_bytes[pos + 1:]
        print("公钥解密异常：", decrypted_bytes)
        return b''

    decrypted_bytes = b''
    if isinstance(data, str):
        data = data.encode()
    if not type(public_key) is RSA.RsaKey:
        public_key = load_rsa_pubkey_from_str(public_key)
    block_size = get_rsa_block_size(public_key)
    try:
        for i in range(0, len(data), block_size):
            block = data[i:i + block_size]
            cur_text = decrypt(block, public_key)
            decrypted_bytes += cur_text
    except Exception as err:
        print('RSA公钥解密失败', err)
    return decrypted_bytes


def load_rsakey_from_file(file_name):
    '''
    读取标准的rsa公钥或私钥pem文件，加载成功后可以通过has_private()判断是否私钥
    :param file_name: 公钥或私钥文件名
    :return: RSA.RsaKey
    '''
    from Crypto.PublicKey import RSA
    key = None
    try:
        keystr = open(file_name).read()
        key = RSA.importKey(keystr)
    except Exception as err:
        print('导入KEY文件出错', file_name, err)
    return key


def load_rsa_prikey_from_str(strkey):
    '''
    字符串密钥转rsa格式密钥，支持pkcs1，pkcs8格式的私钥
    :param strkey: 私钥字符串
    :return: RSA.RsaKey
    '''
    from Crypto.PublicKey import RSA
    ret = None
    if isinstance(strkey, str):
        strkey = strkey.encode()
    if not strkey.startswith(b'-----'):
        strkey = b'-----BEGIN RSA PRIVATE KEY-----\n' + strkey
        strkey += b'\n-----END RSA PRIVATE KEY-----'
    try:
        ret = RSA.importKey(strkey)
    except Exception as err:
        print('字符串密钥转rsa格式密钥错误:', err)
    return ret


def load_rsa_pubkey_from_str(strkey):
    '''
    仅支持pkcs1格式的公钥，其实不需要加载公钥，只需加载私钥即可，可以通过私钥的publickey()方法获取到公钥
    测试发现: pkcs8的公钥也能通过，添加-----BEGIN RSA PUBLIC KEY-----即可
    :param strkey: 公钥字符串
    :return: RSA.RsaKey
    '''
    from Crypto.PublicKey import RSA
    ret = None
    if isinstance(strkey, str):
        strkey = strkey.encode()
    if not strkey.startswith(b'-----'):
        strkey = b'-----BEGIN RSA PUBLIC KEY-----\n' + strkey
        strkey += b'\n-----END RSA PUBLIC KEY-----'
    try:
        ret = RSA.importKey(strkey)
    except Exception as err:
        print('字符串密钥转rsa格式密钥错误:', err)
    return ret


def load_rsa_pubkey_from_prikey(private_key):
    '''
    从私钥中获取公钥
    :param private_key:
    :return: RSA.RsaKey
    '''
    from Crypto.PublicKey import RSA
    ret = None
    if not type(private_key) is RSA.RsaKey:
        private_key = load_rsa_prikey_from_str(private_key)
    ret = private_key.publickey()
    return ret


def get_rsa_block_size(rsa_key):
    '''
    根据key长度计算分块大小
    :param rsa_key: 类型为RSA.RsaKey
    :return:
    '''
    try:
        # RSA仅支持限定长度内的数据的加解密，需要分块
        # 分块大小block_reversed_size=11
        from Crypto.PublicKey import RSA
        if not type(rsa_key) is RSA.RsaKey:
            rsa_key = RSA.importKey(rsa_key)

        key_size = rsa_key.size_in_bits()
        if (key_size % 8) != 0:
            raise RuntimeError('RSA 密钥长度非法')

        bs = int(key_size / 8)
        return bs
    except Exception as err:
        print('计算加解密数据块大小出错:', err)


def pkcs7_pad(text, block_size):
    '''
    2019-06-13：修复了一个bug，通过计算text.encode()后的长度，支持中文
    :param text:
    :param block_size:
    :return:
    '''
    length = len(text.encode('utf-8'))
    pad_size = block_size - (length % block_size)
    text = text + (chr(pad_size) * pad_size)
    return text


# 读取文件的sha1值
def get_file_sha1(filename):
    hashmethod = hashlib.sha1()
    fp = open(filename, "rb")
    f_size = os.stat(filename).st_size

    _FILE_SLIM = (1 * 1024 * 1024)
    while (f_size > _FILE_SLIM):
        hashmethod.update(fp.read(_FILE_SLIM))
        f_size -= _FILE_SLIM
    if f_size > 0:
        hashmethod.update(fp.read())

    return hashmethod.hexdigest()


def base64_encode_str(input):
    if isinstance(input, str):
        input = input.encode()
    encrypted_content = base64.b64encode(input)
    # 加密后的内容是bytes类型的，要解码为str类型返回
    return encrypted_content.decode()


# 输出字符串的16进制格式
def get_str_hex(input):
    # python3.5之前的python3版本，可以用如下方式转换为hex str
    # hex_text=''.join( [ "%02X" % x for x in text ] ).strip()
    # python3.6 可以直接用hex()函数
    if isinstance(input, str):
        input = input.encode()
    return input.hex()


def extract_string_in_bracket(text: str, opener='(', closer=')'):
    """
    获取括号中的字符串
    :param text: 要查找的字符串
    :param opener: 左括号，即开始符号
    :param closer: 右括号，即关闭符号
    :return: 查到的第一个字符串
    用正规表达式查找嵌套结构: 一不小心涉及了正则表达式一个很高级的功能，即平衡组/递归匹配，参考：
    https://blog.csdn.net/wrq147/article/details/6142285
    https://www.cnblogs.com/zs1111/archive/2009/11/12/1601951.html
    目前python还不支持平衡组的功能，所以只能自己实现了，参考：
    https://blog.csdn.net/maosijunzi/article/details/80092121

    none_oc_chars = "[^{0}{1}]*".format(opener, closer)
    p_str = r"\{0}" \
            r"{2}" \
            r"((" \
            r"(?'open'\{0})" \
            r"{2}" \
            r")+" \
            r"(" \
            r"(?'-open'\{1})" \
            r"{2}" \
            r")+)*" \
            r"(?(open)(?!))" \
            r"\{1}".format(opener, closer, none_oc_chars)
    """
    # 采用贪婪模式进行匹配，获取最外层括号里的内空
    p_str = r"\{0}(.*)\{1}".format(opener, closer)
    p = re.compile(p_str)
    result = re.search(p, text)
    if result:
        return result.group(1)
    return None


# 获取当前时间的可读格式
def get_current_time_string(fmt='%Y-%m-%d %H:%M:%S'):
    datetime_str = time.strftime(fmt)
    return datetime_str


def check_identifier_type(user_identifier):
    identifier_type = None
    pattern_phone = re.compile('^([0+]\d{2,3})?-?\d{7,11}$')
    pattern_mail = re.compile('^(\w)+(\.\w+)*@(\w)+((\.\w{2,3}){1,3})$')
    m_phone = pattern_phone.match(user_identifier)
    m_mail = pattern_mail.match(user_identifier)
    if m_phone:
        identifier_type = 'phone'
    elif m_mail:
        identifier_type = 'email'

    return identifier_type


# 检查一个字符串是不是匹配另外一个字符串，精确匹配判断相等，模糊匹配判断包含
def if_name_match(name_expect, name_actual, fuzzy_match):
    if fuzzy_match:
        return name_expect in name_actual
    else:
        return name_actual == name_expect


def read_pem_key_from_file(file_path):
    file_obj = open(file_path)
    print(file_obj)
    try:
        key = file_obj.read()
    finally:
        file_obj.close()
    return key


# 返回一个随机电话号码
def get_random_phone_number():
    list = ['139', '188', '185', '136', '155', '135', '158', '151', '152', '153']
    phone = random.choice(list) + ''.join(random.choice(string.digits) for i in range(8))
    return phone


# 返回一个随机邮箱
def get_random_email():
    suffix = ['com', 'net', 'cn', 'org', 'de', 'fr', 'jp', 'in']
    domain = get_random_string(5)
    first_name = get_random_string(6)
    last_name = get_random_string(3)
    email = "{}_{}@{}.{}".format(first_name, last_name, domain, suffix)
    return email


# 将json对象写入文件
def write_json_to_file(file_name, json_obj, append=False, sort_by_key=True):
    model = 'a' if append else 'w'
    file_writer = open(file_name, model)
    sorted_json_string = json.dumps(json_obj, ensure_ascii=False, sort_keys=sort_by_key)
    file_writer.write(sorted_json_string)
    file_writer.write("\n")


# 写文件是建议都用wb的方式,防止windows操作系统做对换行符做转换
def write_bytes(file_path, content, append=False):
    write_mode = 'ab+' if append else 'wb'
    with open(file_path, write_mode) as to_file:
        print('write content type:', type(content))
        # 在python3中,str和unicode都统一为str了,wb的话需要将string编码为bytes再写入
        # 在python2中str和bytes是同一类型,当content是unicode时,需要将unicode编码为str(bytes)
        if not isinstance(content, bytes):
            content = content.encode('utf-8')
        to_file.write(content)


# 注意中文版windows的默认写入的编码格式是gbk，这里强制采用utf-8格式进行写入
def write_file(file_path, str_row, append=False):
    write_mode = 'a+' if append else 'w'
    with open(file_path, write_mode, encoding='utf-8') as to_file:
        # print('write content type:', type(str_content))
        # 无论python2和3,只要content是str就行
        # python2需要将unicode编码为str,python3需将bytes类型解码为str
        to_file.write(str_row + '\n')


# 注意中文版windows的默认写入的编码格式是gbk，这里强制采用utf-8格式进行写入
def write_rows(file_path, rows: list, append=False):
    write_mode = 'a+' if append else 'w'
    rows = [r + '\n' for r in rows]
    with open(file_path, write_mode, encoding='utf-8') as to_file:
        # print('write content type:', type(str_content))
        # 无论python2和3,只要content是str就行
        # python2需要将unicode编码为str,python3需将bytes类型解码为str
        to_file.writelines(rows)


# 注意中文版windows的默认写入的编码格式是gbk
def write_csv(file_path, row, append=False):
    write_mode = 'a+' if append else 'w'
    with open(file_path, write_mode) as to_file:
        writer = csv.writer(to_file)
        writer.writerow(row)


def read_file(file_path):
    with open(file_path, 'r') as f:
        while True:
            l = f.readline()
            if not l:
                break
            print('read type:{}, content:{}'.format(type(l), l))


# 如果文件是text类型的话,建议还是用r吧,会自动解码
def read_bytes(file_path):
    # 在python2中,rb的读出的内容编码为str类型
    # 在python3中,rb的读出的内容编码为bytes类型,需要自己解码
    with open(file_path, 'rb') as f:
        while True:
            l = f.readline()
            if not l:
                break
            print('read type:{}, content:{}'.format(type(l), l))


def read_csv_last_line(file_path, ignore_empty_line=True):
    with open(file_path, 'r') as f:
        reader = csv.reader(f)
        last_line = []
        for line in reader:
            if ignore_empty_line:
                if line:
                    last_line = line
            else:
                last_line = line
    # print('csv last line type:', type(last_line))
    return last_line


def read_file_last_line(file_path, ignore_empty_line=True):
    # 中文windows下的sys.getdefaultencoding是utf-8,但是写入时默认gbk
    # print ('sys encoding:', sys.getdefaultencoding())
    last_line = ''
    with open(file_path, 'r') as f:
        while True:
            l = f.readline()
            # print ('--length: {}, content: {}'.format(len(l), l))
            if not l:
                break
            elif ignore_empty_line:
                last_line = l if l.strip() else last_line
            else:
                last_line = l
    # print('last line type is:', type(last_line))
    return last_line


# 通过rb的方式读出来的内容是bytes类型的,在解码时要根据写入时的类型来解码,解码格式不对会报错
# 注意中文版windows的默认编码格式是gbk
def read_file_last_line_bytes(file_path):
    last_line = ''
    with open(file_path, 'rb') as f:
        f.seek(0, 2)
        f_length = f.tell()
        count_line_found = 0
        if f_length > 0:
            # 如果文件长度大于0,从文件末尾开始向前移动2位(读取1个字符会导致指针后移1位)
            for i in range(f_length):
                f.seek(-i - 1, 2)
                c = f.read(1)
                if c == '\n':
                    count_line_found += 1
                # 至少要找到两个换行才break
                if count_line_found > 1:
                    break
            # 因为最后有一个读的操作导致指针向前移动了1位,所以最后要反向移一位
            f.seek(-1, 1)
            lines = f.readlines()
            last_line = lines[-1]  # 取最后一行
    # print('last line type is:', type(last_line))
    # 在python2中,rb的读出的内容编码为str类型,无需解码
    # 在python3中,rb的读出的内容编码为bytes类型,需要自己根据写入的编码类型解码
    return last_line


def get_intersection_of_2_time_period(start_time_1, end_time_1, start_time_2, end_time_2):
    '''
    取两个时间段的交集，前提条件是结束时间一定大于开始时间
    :param start_time_1:
    :param end_time_1:
    :param start_time_2:
    :param end_time_2:
    :return:
    '''

    if isinstance(start_time_1, str):
        start_time_1 = datetime.strptime(start_time_1, '%Y-%m-%d %H:%M:%S')
    if isinstance(end_time_1, str):
        end_time_1 = datetime.strptime(end_time_1, '%Y-%m-%d %H:%M:%S')
    if isinstance(start_time_2, str):
        start_time_2 = datetime.strptime(start_time_2, '%Y-%m-%d %H:%M:%S')
    if isinstance(end_time_2, str):
        end_time_2 = datetime.strptime(end_time_2, '%Y-%m-%d %H:%M:%S')

    # 取开始时间的大者，做为交集开始时间
    start_time = start_time_1 if start_time_1 > start_time_2 else start_time_2
    # 取结束时间的小者，做为交集结束时间
    end_time = end_time_1 if end_time_1 < end_time_2 else end_time_2
    # 如果结束时间大于开始时间，代表有交集，否则无交集
    if end_time > start_time:
        return start_time, end_time
    else:
        return None, None


def has_intersection_of_2_time_period(start_time_1, end_time_1, start_time_2, end_time_2):
    s, e = get_intersection_of_2_time_period(start_time_1, end_time_1, start_time_2, end_time_2)
    if s:
        return True
    else:
        return False


if __name__ == '__main__':
    prikey = load_rsakey_from_file('/Users/boweqiang/.ssh/id_rsa')
    # prikey = load_rsa_prikey_from_str(rsa_prikey)
    print(prikey.export_key().decode())
    pubkey = load_rsakey_from_file('/Users/boweqiang/.ssh/id_rsa.pub')
    # pubkey = prikey.publickey()
    print(pubkey.export_key().decode())

    test_str = 'boweiqiang测试' * 10
    # 公钥加密，私钥解密
    encrypted_str = rsa_encrypt_by_public_key(test_str, pubkey)
    # 加密后的byte数组不能直接decode，可以输出其16进制表示字符串
    print('密文是byte数组:', encrypted_str)
    print('密文的十六进制:', encrypted_str.hex())
    print('密文再做base64:', base64.b64encode(encrypted_str).decode())
    decrypted_str = rsa_decrypt_by_private_key(encrypted_str, prikey)
    print('解密结果:', decrypted_str.decode())
