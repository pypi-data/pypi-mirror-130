'''
    进行数据库的操作的基类及方法
'''
import pymysql

class Contraler_Database():
    def __init__(self, databaseName, user='root', passwd='root'):
        self.databaseName = databaseName
        self.user = user
        self.passwd = passwd
        self.openDB()

    def openDB(self):
        try:
            self.conn = pymysql.connect(
                host='localhost',
                user=self.user,
                passwd=self.passwd,
                db=self.databaseName,
                autocommit=True
            )
            self.cursor = self.conn.cursor()
            return self.databaseName+'数据库打开成功'
        except Exception as e:
            return self.databaseName+'数据库打开失败'

    def getAllDataFromDB(self, sql):
        try:
            self.cursor.execute(sql)
            data = self.cursor.fetchall()
            # 将数据转换成列表
            result = []
            for item in data:
                result.append(
                    [
                        item[i] for i in range(len(item))
                    ]
                )
            return result
        except Exception as e:
            print('getAllDataFromDB(sql)方法 出错： ', sql)
            return -1

    def getOneDataFromDB(self, sql):
        try:
            self.cursor.execute(sql)
            data = self.cursor.fetchone()
            # 查找不到的话返回None
            return data
        except Exception as e:
            # 报错才返回-1
            print(e, 'sql: ', sql)
            return -1

    def insertData2DB(self, sql):
        try:
            self.cursor.execute(sql)
            return '数据插入成功'
        except Exception as e:
            print(e, 'sql: ', sql)
            return -1


    def closeDb(self):
        try:
            self.cursor.close()
            self.conn.close()
            return "数据库 ", self.databaseName, " 关闭成功"
        except Exception as e:
            print("数据库 ", self.databaseName, " 关闭失败")
            return -1
