from globalTools import globalTools
from basement__ import ContralerDatabase as dbOp
from spider__.selenium_jinritoutiao import Crawler_toutiao
from basement__.ContralSelenium import ReuseChrome
from basement__.ContralerDatabase import Contraler_Database
import time
from customFunction__.Poster import poster_article

def run(setting):
    """
    文章内容爬取需求：
        1 源： 今日头条财经频道 UC浏览器财经频道
        2 清洗： 去除 除p标签和img标签之外的其它标签 去除所有样式属性 img标签保留src属性
        3 字数： 大于500（若是文章内容为图片的话就不要了）
    """
    # setting = {
    #     'databaseName' : 'articledatabase',
    #     'databaseUser' : 'root',
    #     'databasePasswd' : 'root',
    #     "tableName": ['tb_article_toutiao_content'],
    #     'whichKind': 'articles'
    # }
    # setting['sql'] = "select id,comment from ``.``;"
    dbOperator = Contraler_Database(databaseName='data_usable_database')
    sql_get = 'SELECT * FROM `tb_selenium_info` WHERE `id`=\'1\';'
    driver_info = dbOperator.getOneDataFromDB(sql_get)
    browser_toutiao = ReuseChrome(command_executor=driver_info[1], session_id=driver_info[2])
    browser_toutiao.refresh()
    browser_toutiao.get("https://toutiao.com")
    c = Crawler_toutiao()
    time.sleep(5)
    c.click_chaijing(browser_toutiao)
    time.sleep(3)
    c.click_chaijing(browser_toutiao)
    time.sleep(2)
    c.roll_tobottom_method1(browser_toutiao, 600)
    # 1 上传列表
    articleList = c.get_articleContent(browser_toutiao) # 文章元组对象
    # 2 清洗数据并过滤掉不符合条件的数据
    postableList = []
    for article in articleList:
        # 文章字数过滤
        if(len(article[2])>500):
            postableList.append((article[0], article[1], article[2]))
    browser_toutiao.get('https://www.baidu.com')
    # 3 数据插入数据库
    # dbOperator = dbOp.Contraler_Database(databaseName=setting['databaseName'], user=setting['databaseUser'],passwd=setting['databasePasswd'])
    # for article in postableList:
    #     sql = "INSERT INTO `articledatabase`.`tb_article_toutiao_content` (`url`, `title`, `content`) VALUES ('{}', '{}', '{}');".format(
    #         article[0],
    #         article[1],
    #         article[2]
    #     )
    #     dbOperator.insertData2DB(sql=sql)

    # 3 上传数据
    print('可上传文章的数量：', len(postableList))
    poster = poster_article.Poster_Article('http://121.40.187.51:8088/api/article_get')
    poster.post_auto(postableList, 'article')

    # 4 将上传过的数据放到postedurldatabase中
    # postedDBOP = dbOp.Contraler_Database(databaseName='postedurldatabase', user='root', passwd='root')
    # for article in postableList:
    #     sql = "INSERT INTO `postedurldatabase`.`tb_article_posted` (`url`, `title`, `content`) VALUES (\'{}\', \'{}\');".format(
    #         article[0],
    #         article[1],
    #         article[2]
    #     )
    #     postedDBOP.insertData2DB(sql)
    globalTools.finishTask()

# setting = {
#         'databaseName' : 'articledatabase',
#         'databaseUser' : 'root',
#         'databasePasswd' : 'root',
#         "tableName": ['tb_article_toutiao_content'],
#         'whichKind': 'articles'
#     }
# run(setting)