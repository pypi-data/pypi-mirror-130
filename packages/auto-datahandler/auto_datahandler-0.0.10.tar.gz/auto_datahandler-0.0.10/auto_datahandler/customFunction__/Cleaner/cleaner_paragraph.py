from . import base_cleaner
from basement__ import ContralerDatabase

'''
    针对段落的清洁器类
'''
class Cleaner_Paragraph(base_cleaner.Base_Cleaner):
    def __init__(self):
        self.cleanWordList = [
            '●', '但是，', '所以，', '再说，', '虽然说，', '另外，', '最后，', '而且，',
            '其次，', '首先，', '再者，', '同时，', '不过，', '当然，', '当然啦，', '那么，', '虽然，',
            '其实，', '通常，', '接着，', '综上所述，', '因此，', '、'
        ]
        self.irrelevantWordList = ['图']
        self.baseClass = base_cleaner.Base_Cleaner  # 父类
        for i in range(1, 10):
            self.cleanWordList.append(str(i) + '.')
            self.cleanWordList.append(str(i) + '。')
            self.cleanWordList.append(str(i) + '，')
            self.cleanWordList.append(str(i) + '、')
            self.cleanWordList.append(str(i) + '：')
            self.cleanWordList.append('（' + str(i) + '）')
            self.cleanWordList.append(str(i) + '）')
            self.cleanWordList.append('(' + str(i) + ')')
            self.cleanWordList.append('[' + str(i) + ']')
            self.cleanWordList.append('【' + str(i) + '】')
        for item in self.universal_cleanWordDict['numList1']:
            self.cleanWordList.append(item + '、')
            self.cleanWordList.append(item + '。')
            self.cleanWordList.append('(' + item + ')')
        for item in self.universal_cleanWordDict['numList2']:
            self.cleanWordList.append(item + '、')
            self.cleanWordList.append(item + '，')
        for item in self.universal_cleanWordDict['alphabeticList']:
            self.cleanWordList.append(item + '.')

        self.cleanWordList = tuple(self.cleanWordList)

        # 从数据库获取股票名字和代码
        sql = "select name, code from `tb_namecode`"
        dbOperator = ContralerDatabase.Contraler_Database('stocksnamecode')
        self.stocksNameCodeList = dbOperator.getAllDataFromDB(sql)
        dbOperator.closeDb()
        del dbOperator

    def integratedOp(self, paragraph):
        # 清序号
        temp = self.baseClass.delHeaderNum(paragraph, cleanWordList=self.cleanWordList)
        # 清空格
        temp = self.baseClass.delSpace(temp)
        # 清序号
        temp = self.baseClass.delHeaderNum(temp, cleanWordList=self.cleanWordList)
        # 清股票
        # temp = self.delStocksNameAndCode(temp)
        # 清不相关的文字
        result = self.baseClass.delIrrelevantWord(temp, irrelevantWordList=self.irrelevantWordList)
        return result

