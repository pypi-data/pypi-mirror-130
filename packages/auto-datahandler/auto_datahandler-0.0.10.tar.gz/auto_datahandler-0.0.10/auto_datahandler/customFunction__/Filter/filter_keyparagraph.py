from . import base_filter
from ..Cleaner import cleaner_paragraph
from basement__ import ContralerDatabase as dbOp

class Filter_Keyparagraph(base_filter.Base_Filter):
    def integratedOp(self, paragraphList, databaseName, tableName, tableName4Tag, tagRefSqlKind='id'):
        result = []
        cleanerInstance = cleaner_paragraph.Cleaner_Paragraph()
        dbOperator = dbOp.Contraler_Database(databaseName=databaseName)
        for item in paragraphList:
            # 筛选有标签的
            if (self.filter_hasTag_keyParagraph(item)):
                # 进行清洗操作
                item[1] = cleanerInstance.integratedOp(item[1])
                # 筛选判断 ： 1 字符串长度不在125-250之间；2 段落含有股票名或代码 3 段落包含日期关键词
                ##          但凡满足上面任何一个的段落筛选条件的段落都过滤掉
                check = (not self.filter_BetweenNumberOfWords(item[1],whichKind='keyParagraph')) or self.filter_hasStockCode(item[1], self.stocksNameCodeList) or self.filter_dateRef(item[1], self.dateRefList)
                if (check):
                    # 进入该判断条件说明对应段落无效跳过， 因此希望有效段落的check最终为false
                    continue
                if (tagRefSqlKind == 'id'):
                    sql = "SELECT `tag_origin` FROM " + databaseName + "." + tableName4Tag + " WHERE `id`=" + str(
                        item[2]) + ";"
                elif (tagRefSqlKind == 'url'):
                    sql = "SELECT `tag_origin` FROM " + databaseName + "." + tableName4Tag + " WHERE `url`='" + str(
                        item[2]) + "';"
                result.append(
                    (
                        item[1],  # 段落内容
                        dbOperator.getOneDataFromDB(sql)[0],  # 段落关键词
                    )
                )
            else:
                continue
        dbOperator.closeDb()
        del dbOperator
        return result