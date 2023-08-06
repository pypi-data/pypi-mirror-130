import json
import requests, hashlib
from basement__.ContralerTime import Contraler_Time
from basement__.ContralerDatabase import Contraler_Database
from requests_toolbelt import MultipartEncoder


class Base_Poster:
    interface = ''
    userName = 'qin'
    password = 'qin123456'
    contralTime = Contraler_Time()
    curDate = str(contralTime.getCurDate(formatStr="%Y%m%d"))
    key = hashlib.md5(('datapool' + userName + password + curDate).encode('utf-8')).hexdigest()
    dbOperator = Contraler_Database(databaseName='postedurldatabase')


    # 上传单个数据列表的方法
    @staticmethod
    def poster(postableData, interface):
        '''
        上传单条数据的方法
        :param postableData:
        :param interface: 接口
        :return:
        '''
        # 这里传文件的时候用绝对路径传，不然传了之后显示不了
        formData = (postableData)
        m = MultipartEncoder(formData)
        headers2 = {
            "Content-Type": m.content_type
        }
        paragraphPostResult = requests.post(url=interface, data=m, headers=headers2)
        return paragraphPostResult


    def post_auto(self, effectiveDataList, whichKind):
        for item in effectiveDataList:
            if (whichKind == 'keyParagraph'):
                postableData = {
                    "key": self.key,
                    "account": self.userName,
                    "password": self.password,
                    'content': item[0],
                    'keyword': item[1],
                    'rekeyword': '配资'
                }
                self.poster(postableData=postableData, interface=self.interface)
            elif (whichKind == 'relativeParagraph'):
                postableData = {
                    "key": self.key,
                    "account": self.userName,
                    "password": self.password,
                    'content': item[0],
                    'keyword': item[1]
                }
                self.poster(postableData=postableData, interface=self.interface)
            elif (whichKind == 'articleComment'):
                comment = item[0].strip()
                sql = "SELECT * FROM `postedurldatabase`.`tb_comment_posted` where `comment` = \'{}\';".format(comment)
                if (self.dbOperator.getOneDataFromDB(sql)):
                    # 数据库中存在对应评论
                    continue
                postableData = {
                    "key": self.key,
                    "account": self.userName,
                    "password": self.password,
                    'comment': item[0].replace(item[1], '股票').replace('&nbsp;', ' ')
                }
                self.poster(postableData=postableData, interface=self.interface)
                # 更新数据库
                self.update_postedurldb(item)
            elif(whichKind == 'article'):
                postableData = {
                    "key": self.key,
                    "account": self.userName,
                    "password": self.password,
                    'title': item[1],
                    'content': item[2]
                }
                self.poster(postableData=postableData, interface=self.interface)
            elif (whichKind == 'question'):
                postableData = {
                    "key": self.key,
                    "account": self.userName,
                    "password": self.password,
                    'question': str(item[0]),
                    'answer': json.dumps(item[1])
                }
                res = self.poster(postableData=postableData, interface=self.interface)
                print(res.text)
