import time

"""
    时间（时间戳、日期、年月日等）处理相关的基类和方法
"""
# 时间处理类
class Contraler_Time:
    @staticmethod
    def getMilliSecond():
        '''
        返回毫秒级时间戳
        '''
        return int(round(time.time() * 1000))

    # 获取当前日期
    @staticmethod
    def getCurDate(formatStr:str):
        '''
        获取当前日期
        :param formatStr: 指定格式 如 "%Y%m%d"
        :return:
        '''
        return time.strftime(formatStr, time.localtime())

    # 返回指定日期时间戳 时间格式 '%Y%m%d %H:%M:%S' 20210924 00：00：00 该方法用于哔哩哔哩时间的判断
    @staticmethod
    def getSecondByDate(date):
        b = time.strptime(date, '%Y%m%d %H:%M:%S')
        return time.mktime(b)