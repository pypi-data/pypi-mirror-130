import hashlib, base64
from urllib import parse

"""
    加密相关的基类和方法
"""
# 加密类
class Encode:
    # 统一输出类型为str
    def bytes2str(self, b):
        return str(b, encoding='utf-8')

    def str2bytes(self, s):
        return bytes(s, encoding='utf-8')

    def encodeByMd5(self, s):
        return hashlib.md5(s.encode(encoding='utf-8')).hexdigest()

    # base64输出的为bytes类型 要转化为字符串
    def encodeByBase64(self, s):
        res = base64.encodebytes(s).strip()
        # 转换为字符串
        res = self.bytes2str(res)
        return res

    def encode0(self,s):
        return self.encodeByBase64(self.str2bytes(self.encodeByMd5(s)))

    @staticmethod
    def str2urlcode(s):
        '''
        将字符串转换为浏览器url编码格式
        '''
        return parse.quote(s)

    @staticmethod
    def urlcode2str(urlcode):
        '''
        将url编码转换为字符串格式
        '''
        return parse.unquote(urlcode)