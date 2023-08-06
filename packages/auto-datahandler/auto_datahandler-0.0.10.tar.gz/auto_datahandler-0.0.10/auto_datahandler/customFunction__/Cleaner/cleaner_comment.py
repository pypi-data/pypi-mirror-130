from . import base_cleaner
from basement__ import ContralerDatabase

'''
    针对评论内容的清洁器类
'''
class Cleaner_Comment(base_cleaner.Base_Cleaner):
    def __init__(self):
        self.cleanWordList = []
        self.irrelevantWordList = ['图']
        self.baseClass = base_cleaner.Base_Cleaner  # 父类
        for i in range(1, 10):
            self.cleanWordList_headnum.append(str(i) + '.')
            self.cleanWordList_headnum.append(str(i) + '。')
            self.cleanWordList_headnum.append(str(i) + '，')
            self.cleanWordList_headnum.append(str(i) + '、')
            self.cleanWordList_headnum.append(str(i) + '：')
            self.cleanWordList_headnum.append('（' + str(i) + '）')
            self.cleanWordList_headnum.append(str(i) + '）')
            self.cleanWordList_headnum.append('(' + str(i) + ')')
            self.cleanWordList_headnum.append('[' + str(i) + ']')
            self.cleanWordList_headnum.append('【' + str(i) + '】')
        for item in self.universal_cleanWordDict['numList1']:
            self.cleanWordList_headnum.append(item + '、')
            self.cleanWordList_headnum.append(item + '。')
            self.cleanWordList_headnum.append('(' + item + ')')

    def integratedOp(self, comment):
        # 清空格
        temp = self.delSpace(comment)
        # 清序号
        temp = self.delHeaderNum(temp, self.cleanWordList_headnum)
        # 清标签
        result = self.del_webTag(temp)
        return result

