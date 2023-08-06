from . import base_filter
from ..Cleaner import cleaner_paragraph

class Filter_Relativeparagraph(base_filter.Base_Filter):
    # -> 关联段落的集成操作方法
    def integratedOp(self, paragraphList, keywordList):
        result = []
        cleanerInstance = cleaner_paragraph.Cleaner_Paragraph()
        for item in paragraphList:
            # 1 进行清洗操作
            item[1] = cleanerInstance.integratedOp(item[1])
            for keyword in keywordList:
                # 2 根据字符串长度125-250间进行筛选
                if (not self.filter_BetweenNumberOfWords(item[1], whichKind='relativeParagraph')):
                    # 段落字数再125-250间，有用可传
                    continue
                # 3 对每个段落进行关键词筛选 若有关键词则跳出当前循环
                if (self.checkIfHasKeyword_relativeParagraph(item[1], keyword)):
                    # 4 根据筛选结果导入可上传的数据
                    result.append(
                        (
                            item[1],  # 段落内容
                            keyword,  # 相关关键词
                        )
                    )
                    break
        return result