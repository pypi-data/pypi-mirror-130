from globalTools import globalTools
from basement__.ContralerTime import Contraler_Time
from basement__.ContralerDir import Contraler_Dir
from spider__ import selenium_douyin,selenium_sougou_weixin, selenium_kuaishou



# Selenium 爬取 爬取视频源 抖音
def run_douyin(proj_absPath, crawlUrl_list, oriDomain='douyin'):
    updateTime = Contraler_Time.getCurDate("%Y%m%d")
    videoDirPath = proj_absPath + '\\assets\\videos\\' + updateTime + '\\' + oriDomain + '\\'
    coverSavedPath = proj_absPath + '\\assets\\videos\\' + updateTime + '\\cover_douyin.jpg'
    captchaPath = proj_absPath + '\\assets\\captcha\\' + updateTime + '\\' + oriDomain + '\\'
    # 判断配置里的目录是否存在，不存在则创建对应目录
    Contraler_Dir.checkACreateDir(videoDirPath)
    Contraler_Dir.checkACreateDir(captchaPath)

    # 抖音视频的爬取及上传
    spider_douyin = selenium_douyin.Crawler_Douyin(captchaPath=captchaPath, videoDirPath=videoDirPath)
    for url in crawlUrl_list:
        lis = spider_douyin.enterIndexDouyin(move2BottomTimes=1, douyinUrlIndex=url)
        postResult = spider_douyin.getRealVideo(lis, videoDirPath, coverSavedPath)
    spider_douyin.browser0.close()
    spider_douyin.browser1.close()
    globalTools.finishTask()

def run_spider(origin):
    if(origin=='sougou'):
        sougou = selenium_sougou_weixin.Crawler_Sougou()
        sougou.run()
        globalTools.finishTask()
        del sougou
    elif (origin == 'kuaishou'):
        # 视频的爬取上传
        kuaishou = selenium_kuaishou.Crawler_Kuaishou()
        kuaishou.run()
        globalTools.finishTask()
        del kuaishou


