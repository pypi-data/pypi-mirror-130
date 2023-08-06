from . import base_cleaner
from basement__ import ContralerDatabase


class Cleaner_Article(base_cleaner.Base_Cleaner):
    """
        文章内容 清洗需求
            1 只保留p标签和img标签
            2 清掉所有样式属性 img保留src
    """
    def __init__(self):
        self.cleanWordList = [
            '本报记者 ', '友情提示：'
        ]
        self.irrelevantWordList = ['图']
        self.baseClass = base_cleaner.Base_Cleaner  # 父类

    def clean_tag(self, content):
        pass

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

