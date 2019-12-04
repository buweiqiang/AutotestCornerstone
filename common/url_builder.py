class UrlBuilder(object):
    def __init__(self, protocol, host, port='', base_path=''):
        self.__protocol = protocol
        self.__host = host
        self.__port = port
        self.__base_path = base_path
        self.baseurl = "{}://{}".format(self.__protocol, self.__host)
        if port:
            self.baseurl = "{}:{}".format(self.baseurl, self.__port)

        self.server_url = self.baseurl

        if base_path:
            self.baseurl = "{}/{}".format(self.baseurl, self.__base_path.strip('/'))
        self.init_urls()

    def init_urls(self):
        '''
        初始化urls，基类默认不初始化任何url,请在子类中实现这个方法
        :return: 无
        '''
        pass
        # raise NotImplementedError('请在子类中实现这个方法')
