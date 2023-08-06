'''
    自动化引擎
        缩略图 清洗 筛选 并上传
'''
from globalTools import globalTools
from customFunction__.Poster import poster_img
from customFunction__.imgref import classifier as Classifier
from customFunction__.imgref import processing as Processing
from customFunction__.Filter import filter_image
from basement__ import ContralerDatabase as dbOp
from basement__.ContralerTime import Contraler_Time
from basement__.ContralerDir import Contraler_Dir
from basement__.Download import Downloader

def run(proj_absPath, oriDomain, database, tableNameList):
    # 将目录下的图片图片传到接口
    # 获取当前目录所在绝对路径
    # proj_absPath = os.path.abspath(os.path.dirname(__file__))
    updateTime = Contraler_Time.getCurDate("%Y%m%d")
    '''
    oriDomain = 'huxiu'
    '''
    setting = {
        # 爬取下来的图片的存放路径
        'imgsCrawledDir' : proj_absPath + '\\assets\imgsCrawled\\' + updateTime + '\\' + oriDomain + '\\',
        # 经过百度识别重命名后存放的目录路径
        'imgsReconizedDir': proj_absPath + '\\assets\imgsReconized\\' + updateTime + '\\' + oriDomain + '\\',
        # 初步处理过后的无水印的图片的目录
        'imgsDirDontHasWaterMask' : proj_absPath + '\\assets\imgsDontHasWaterMask\\' + updateTime + '\\' + oriDomain + '\\',
        # 初步处理过后有水印的图片的目录
        'imgsDirHasWaterMask' : proj_absPath + '\\assets\imgDirHasWaterMask\\' + updateTime + '\\' + oriDomain + '\\',
        # 处理完成的图片目录
        'imgsCleanedDir' : proj_absPath + '\\assets\imgsCleanedDir\\' + updateTime + '\\' + oriDomain + '\\',
        # 缩略图保存位置图片目录
        'imgsThumbnailDir' : proj_absPath + '\\assets\imgsThumbnailDir\\' + updateTime + '\\' + oriDomain + '\\',
    }

    # 判断配置里的目录是否存在，不存在则创建对应目录
    for item in setting.values():
        Contraler_Dir.checkACreateDir(item)

    # 从数据库获取图片链接 下载图片
    print("从数据库获取图片链接")
    dbOperator = dbOp.Contraler_Database(database)
    # 上传过的图片去重
    picList_posted_ = dbOperator.getAllDataFromDB("SELECT `origin_pic_path` FROM `postedurldatabase`.`tb_thumbnailimgs_posted`")
    picList_posted = []
    for item in picList_posted_:
        picList_posted.append(item[0])
    print(picList_posted)
    print("下面开始下载图片")
    for table in tableNameList:
        sql = "SELECT `id`,`origin_pic_path` FROM `" + table + "`;"
        imgUrlPathList = dbOperator.getAllDataFromDB(sql)
        print("数据表为 ", table, "获得图片链接数量： ", len(imgUrlPathList))
        for imgUrl in imgUrlPathList:
            if(imgUrl[1] in picList_posted):
                continue
            imgName = table + "_" + str(imgUrl[0])
            Downloader.download_img(urlpath=imgUrl[1], imgname=imgName, dstDirPath=setting["imgsCrawledDir"])
            insert_SQL = "INSERT INTO `postedurldatabase`.`tb_thumbnailimgs_posted` (`origin_pic_path`) VALUES (\'{}\');".format(imgUrl[1])
            dbOperator.insertData2DB(insert_SQL)

    print("图片下载完成")
    # 对爬取下来的图片进行处理 - 识别重命名、过滤、水印的识别及裁切 处理完后放在路径  ./assets/imgsCleanedDir 下
    # 2 重命名
    classifier = Classifier.imgsClassifier(crawledDirPath=setting['imgsCrawledDir'], savedDirPath=setting['imgsReconizedDir'])
    classifier.run()

    # 3 过滤 (关键词过滤、空文件过滤、水印识别及处理）
    print("下面开始过滤操作")
    filter = filter_image.imgsFilter(
        imgsDontHasWaterMaskDir=setting['imgsDirDontHasWaterMask'],
        imgDirHasWaterMask=setting['imgsDirHasWaterMask'],
        imgCleanedStep1 = setting['imgsCleanedDir'],
        # dirOriPath=setting['imgsReconizedDir']
        dirOriPath = setting['imgsCrawledDir']
    )
    filter.run_()    # 这里再做一下优化
    print("过滤操作完成")

    # 4 将过滤后的图片整成缩略图
    print("下面将图片整成缩略图")
    thumbnailOriDir = setting['imgsReconizedDir']
    thumbnailDstDir = setting['imgsThumbnailDir']
    imgprocesser = Processing.Imgs2ThumbnailByDir(thumbnailOriDirPath=thumbnailOriDir, thumbnailDstDirPath=thumbnailDstDir)
    imgprocesser.cutOff2ThumbnailByDir()

    print("下面将开始传送")
    # # 4 创建图片发送的poster 传送处理完成的图片
    # 传送缩略图
    imgposter0 = poster_img.Poster_Imgs(imgDirPath=setting['imgsThumbnailDir'])
    imgposter0.updateImgsThumbnail()
    globalTools.finishTask()
