import re
"""
    字符处理相关的基类和方法
"""

class IsCheck_uchar:
    '''
        底层设计 —— 字符判断 输出均为布尔值
    '''
    @staticmethod
    def is_chinese(uchar):
        """判断一个unicode是否是汉字"""
        if(u'\u4e00' <= uchar <=u'\u9fa5'):
            return True
        else:
            return False

    @staticmethod
    def is_number(uchar):
        """判断一个unicode是否是数字"""
        if(u'\u0030' <= uchar <= u'\u0039'):
            return True
        else:
            return False

    @staticmethod
    def is_alphabet(uchar):
        """判断一个unicode是否是英文字母"""
        if(u'\u0041' <= uchar <= u'\u005a' or u'\u0061' <= uchar <= u'\u007a'):
            return True
        else:
            return False

    @staticmethod
    def is_other(uchar):
        """判断是否非汉字、非数字、非英文字符"""
        if(not (IsCheck_uchar.is_chinese(uchar) or IsCheck_uchar.is_number(uchar) or IsCheck_uchar.is_alphabet(uchar))):
            return True
        else:
            return False

    @staticmethod
    def all_isNumber(s):
        """验证字符串是否全部为数字"""
        p = re.compile('^[0-9]*$')
        result = p.match(s)
        if (result):
            # 说明全部位数字，返回1
            return True
        else:
            return False
