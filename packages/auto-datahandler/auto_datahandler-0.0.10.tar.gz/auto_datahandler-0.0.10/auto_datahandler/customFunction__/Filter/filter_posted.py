from basement__ import ContralerDatabase as dbOp
from ..Cleaner import cleaner_comment
'''
    过滤上传过的内容的类
'''
class Filter_Posted():
    def __init__(self):
        self.dbOperator = dbOp.Contraler_Database(databaseName='postedurldatabase')

    # paragraph 为待处理上传的数据
    def filterPosted(self, paragraph):
        paragraph = paragraph.strip()  # 清除一下左右空格
        sql = "SELECT * FROM `postedurldatabase`.`tb_article_posted` where `paragraph` = \'{}\';".format(paragraph)
        check = self.dbOperator.getOneDataFromDB(sql)
        if(check):
            # 上传过130 12
            return True
        else:
            return False

    def run(self, dataOriList):
        result = []
        for item in dataOriList:
            if(not self.filterPosted(paragraph=item[1])):
                # 没上传过，加入结果
                result.append(item)
        return result


class Filter_Posted_Comment():
    def __init__(self):
        self.dbOperator = dbOp.Contraler_Database(databaseName='postedurldatabase')
        self.cleaner = cleaner_comment.Cleaner_Comment()

    # comment 为待处理上传的数据
    def filterPosted(self, comment):
        comment = self.cleaner.integratedOp(comment)
        comment = comment.strip()  # 清除一下左右空格
        sql = "SELECT * FROM `postedurldatabase`.`tb_comment_posted` where `comment` = \'{}\';".format(comment)

        check = self.dbOperator.getOneDataFromDB(sql)
        if(check):
            return True
        else:
            return False

    def run(self, dataOriList):
        result = []
        for item in dataOriList:
            if(not self.filterPosted(comment=item[1])):
                # 没上传过，加入结果
                result.append(item)
        return result