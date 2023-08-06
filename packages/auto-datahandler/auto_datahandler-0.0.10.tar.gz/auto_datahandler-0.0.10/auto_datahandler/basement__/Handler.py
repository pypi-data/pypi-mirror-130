import re

"""
    通用的一些处理
"""


# 字符串正则处理类
class Handler_String_ByRe:
    def extract_StrByRe(self, string, patternStr=r'[[](.*?)[]]'):
        '''
        正则匹配字符串获取指定内容(匹配[]包括这的内容)
        :param string: 待匹配的字符串
        :param patternStr: 正则表达式模式
        :return: 列表
        '''
        pattern = re.compile(patternStr, re.S)  # 最小匹配
        return re.findall(pattern, string)



class Handle_PackageInfo:
    '''
        处理报文信息 如 cookie和headers字符串和对象的转换
    '''
    def translate_Cookies_Row2Obj(self, cookiesRow):
        cookieList = cookiesRow.split(";")
        self.cookies = {}
        for cookieItem in cookieList:
            i = cookieItem.strip().split("=")
            k = i[0]
            v = i[1]
            self.cookies[k] = v
        return self.cookies

    def translate_Headers_Row2Obj(self, headersRow):
        headerList = headersRow.split('\n')
        self.headers = {}
        for headerItem in headerList:
            i = headerItem.strip().split(":")
            if (i != ['']):
                k = i[0]
                v = i[1]
                self.headers[k] = v
        return self.headers