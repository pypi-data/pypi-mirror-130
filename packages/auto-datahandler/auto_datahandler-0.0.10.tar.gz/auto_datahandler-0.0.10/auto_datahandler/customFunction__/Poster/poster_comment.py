from . import base_poster
import requests
from requests_toolbelt import MultipartEncoder

class Poster_Comment(base_poster.Base_Poster):
    def __init__(self, interface):
        self.interface = interface

    def update_postedurldb(self, item):
        sql = "INSERT INTO `postedurldatabase`.`tb_comment_posted` (`comment`) VALUES (\'{}\');".format(item[0].strip())
        return self.dbOperator.insertData2DB(sql)

