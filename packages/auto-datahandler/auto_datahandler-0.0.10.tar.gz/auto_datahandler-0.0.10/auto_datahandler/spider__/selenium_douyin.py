from selenium import webdriver
from time import sleep
import requests
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from customFunction__.Poster.poster_video import Poster_Video as VideoPoster
from customFunction__.Filter.filter_video import DouyinFilter
from basement__.ContralerTime import Contraler_Time
from basement__ import Tools as tools
from basement__ import ContralerDatabase as dbOp
from customFunction__.Cracker import cracker_douyin
from customFunction__.Cleaner.cleaner_title import Cleaner_Title

# 已有图片链接下载图片的方法
def downVideo(urlpath, name, dstDirPath):
    print("下载： ", urlpath)
    r = requests.get(urlpath, verify=False)
    video = r.content       #响应的二进制文件
    with open(dstDirPath + str(name) + '.mp4','wb') as f:     #二进制写入
        f.write(video)
    r.close()   # 关闭很重要，确保不要过多的连接

# --------------------------- 爬取抖音视频的类 ----------------------------------
"""
    获得视频列表
    过滤视频列表
        筛选条件：
        1 判断视频时长 1~6min
        2 判断发布时间为当天
        3 标题筛选 筛掉包含过滤词的视频
        上传视频
"""
class Douyin_SpecialMethod:
    @staticmethod
    def check_publishtime_istoday(s: str):
        """
        根据抖音视频页面的发布时间表示情况写的方法 判断是否为当天
        :param s 类似 2021-12-07 的字符串
        :output Boolean
        """
        pubTime = "".join(s.split("-"))
        if (pubTime != Contraler_Time.getCurDate("%Y%m%d")):
            # 判断不是当天的视频则跳过
            return False
        else:
            return True

    @staticmethod
    def check_timelength_between(s, min=1, max=6):
        """
        判断视频长度是否符合条件
        :param s 视频长度字符串 如 06:30
        :param min 最小几分钟
        :param max 最大几分钟
        根据抖音视频页面的发布时间表示情况写的方法 判断视频长度是否符合要求： >=1min, <=6min
        """
        if (s.split(":")[0].startswith('0')):
            if (s.split(":")[0].replace('0', '') != ''):
                minute = s.split(":")[0].lstrip('0')
            else:
                minute = '0'
            if (int(minute) >= min and int(minute) <= max):
                # 符合条件
                return True
            else:
                return False
        else:
            return False

    # 处理滑块验证的方法：1 直接关闭 2 滑动验证
    def handleSlideCheck(self):
        sleep(5)
        try:
            self.EffectiveCookies0 = self.douyinCracker0.handle_SlideCheck(self.browser0)
        except Exception as e:
            print("browser0 无滑块出现")

        try:
            self.EffectiveCookies1 = self.douyinCracker1.handle_SlideCheck(self.browser1)
        except Exception as e:
            print("browser1 无滑块出现")

    # 设置上一次爬取最新的那个数据的信息
    def setTheNewestCrawledInfo(self, title):
        self.theNewestTitle = title

    # 下滑到最底部
    def moveToBottom(self, times=350):
        # 以当前位置为参照向下滚动
        # self.browser.execute_script('window.scrollBy(0 ,1000)') # 从当前位置向下滚动1000px
        for i in range(0, times):
            self.browser0.find_element_by_tag_name('body').send_keys(Keys.ARROW_DOWN)  # 在这里使用模拟的下方向键
            sleep(0.01)

    # 滑块验证 XX 滑块验证有点问题， 手动验证吧，自动化滑块验证还做不了
    # 遇到的问题，滑块验证采用拼图的形式，需要先检验待拼的位置坐标才行
    #   抖音的验证流程， 服务器发送一个cookie s_v_web_id:Value 到客户端，客户端进行滑块验证，验证成功的话发送一个成功的请求到服务器端，服务器端对 对应s_v_web_id  做一些调整（赋予权限），客户端就能正常浏览了
    #   s_v_web_id在一次会话结束时候失效
    def checkSlide(self, browser, x):
        sleep(2)
        # 实例化鼠标操作
        action = ActionChains(browser)
        # 按住滑块
        action.click_and_hold(browser.find_element_by_xpath("//*[@class='captcha_verify_img_slide react-draggable sc-VigVT ggNWOG']")).perform()
        for i in range(x):
            action.move_by_offset(1, 0)
        sleep(2)
        # 释放滑块
        action.release().perform()
        pass


class Crawler_Douyin(Douyin_SpecialMethod):
    def __init__(self, captchaPath, videoDirPath, chromeDriverPath=r'E:\Projects\webDriver\\chrome\\chromedriver.exe'):
        self.dboperator = dbOp.Contraler_Database(databaseName='postedurldatabase')
        self.filter = DouyinFilter(dirOriPath=videoDirPath)

        option = webdriver.ChromeOptions()
        option.add_experimental_option('excludeSwitches', ['enable-automation'])
        option.add_argument('--disable-blink-features=AutomationControlled')

        self.browser0 = webdriver.Chrome(executable_path=chromeDriverPath, options=option)
        self.browser1 = webdriver.Chrome(executable_path=chromeDriverPath, options=option)
        self.browser0.get('https://www.douyin.com')
        self.browser1.get('https://www.douyin.com')
        sleep(2)
        self.douyinCracker0 = cracker_douyin.DouyinCrack(captchaDstDirPath=captchaPath)
        self.douyinCracker1 = cracker_douyin.DouyinCrack(captchaDstDirPath=captchaPath)
        sleep(2)

        self.handleSlideCheck() # 滑块验证
        self.theNewestTitle = ''

        # 滑块验证参数
        self.captchaPath = captchaPath

    # 首次进入 move2BottomTimes 为向下滑动的次数 默认350
    def enterIndexDouyin(self, move2BottomTimes, douyinUrlIndex='https://www.douyin.com/search/%E8%82%A1%E7%A5%A8?publish_time=1&sort_type=2&source=normal_search&type=video'):
        self.browser0.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
            'source': 'Object.defneProperty(navigator, "webdriver", {get: () => undefined})'
        })
        self.browser0.get(douyinUrlIndex)
        # 滑块验证
        self.handleSlideCheck()

        # 2.通过浏览器向服务器发送URL请求
        self.browser0.get(douyinUrlIndex)
        # 滑块验证
        self.handleSlideCheck()

        # 等待某个元素是否出现
        WebDriverWait(self.browser0, 10).until(
            # EC.text_to_be_present_in_element((By.XPATH, ''))
            EC.presence_of_element_located((By.XPATH, "//ul[@class='_3636d166d0756b63d5645bcd4b9bcac4-scss']"))
        )
        self.handleSlideCheck()
        # 这里获取的ul用于判断
        try:
            ul = self.browser0.find_element_by_xpath("//ul[@class='_3636d166d0756b63d5645bcd4b9bcac4-scss']")
            liList = ul.find_elements_by_xpath("./li")
        except Exception as e:
            # 滑块验证
            self.handleSlideCheck()


        try:
            liFirstTitle = liList[0].find_element_by_xpath(".//a[@class='caa4fd3df2607e91340989a2e41628d8-scss a074d7a61356015feb31633ad4c45f49-scss _9c976841beef15a22bcd1540d1e84c02-scss']") # 获取标题
        except Exception as e:
            liFirstTitle = '空'
            # 滑块验证
            self.handleSlideCheck()

        liEffectiveList = []  # 可上传的视频信息列表
        # 判断是否有上一次爬取
        if(self.theNewestTitle!=''):
            # 说明有上一次爬取
            self.moveToBottom(move2BottomTimes)
            if(not(liFirstTitle == self.theNewestTitle)):
                # 说明有更新
                for li in liList:
                    # 每获取一个则下载上传一个
                    try:
                        a = li.find_element_by_xpath(".//a[@class='caa4fd3df2607e91340989a2e41628d8-scss a074d7a61356015feb31633ad4c45f49-scss _9c976841beef15a22bcd1540d1e84c02-scss']")
                    except Exception as e:
                        # 滑块验证
                        self.handleSlideCheck()
                        continue
                    try:
                        publishTime = li.find_element_by_xpath(".//span[@class='b32855717201aaabd3d83c162315ff0a-scss']").text
                        timeLength = li.find_element_by_xpath(".//span[@class='d170ababc38fdbf760ca677dbaa9206a-scss']")
                    except Exception as e:
                        # 滑块验证
                        self.handleSlideCheck()
                    title = a.text
                    videoPageUrl = a.get_attribute("href")

                    # 当爬取到最新的那个则跳出循环
                    if(title == self.theNewestTitle):
                        break
                    if (self.check_timelength_between(timeLength)):
                        liEffectiveList.append((title, videoPageUrl, publishTime))
                    else:
                        continue
                # 更新最新的那个数据
                self.setTheNewestCrawledInfo(
                    liList[0].find_element_by_xpath(
                        ".//a[@class='caa4fd3df2607e91340989a2e41628d8-scss a074d7a61356015feb31633ad4c45f49-scss _9c976841beef15a22bcd1540d1e84c02-scss']")
                )
            return liEffectiveList
        else:
            # 滑块验证
            self.handleSlideCheck()
            # 向下滚动
            self.moveToBottom(move2BottomTimes)

            ul = self.browser0.find_element_by_xpath("//ul[@class='_3636d166d0756b63d5645bcd4b9bcac4-scss']")
            liList = ul.find_elements_by_xpath("./li")
            self.liList = liList
            for li in liList:
                # 每获取一个则下载上传一个
                try:
                    a = li.find_element_by_xpath(".//a[@class='caa4fd3df2607e91340989a2e41628d8-scss a074d7a61356015feb31633ad4c45f49-scss _9c976841beef15a22bcd1540d1e84c02-scss']")
                except Exception as e:
                    continue
                timeLength = li.find_element_by_xpath(".//span[@class='d170ababc38fdbf760ca677dbaa9206a-scss']").text
                publishTime = li.find_element_by_xpath(".//span[@class='b32855717201aaabd3d83c162315ff0a-scss']").text
                title = a.text
                videoPageUrl = a.get_attribute("href")
                if (self.check_timelength_between(timeLength)):
                    liEffectiveList.append((title, videoPageUrl, publishTime))
                else:
                    continue
                sleep(5)
            return liEffectiveList




    def getRealVideo(self, videoList_, videoDirPath, coverSavedPath):
        poster = VideoPoster(videoDirPath=videoDirPath, coverSavedPath=coverSavedPath)
        filter_video = DouyinFilter(dirOriPath=videoDirPath)
        if (videoList_):
            videoList = self.filter.filter_posted(videoList_) # 过滤掉上传过的视频
            videoList = tools.cleanRepeated(videoList)  # 去重
            # 过滤标题操作
            videoList = filter_video.filter_keywordFromTitle(videoList)
        else:
            return None
        i = 1
        if(videoList!=''):
            for item in videoList:
                # 2.通过浏览器向服务器发送URL请求
                self.browser1.get(item[1])
                # 滑块验证
                self.handleSlideCheck()
                self.browser1.get(item[1])
                sleep(5)
                # 说明出现了滑块验证处理一下
                self.handleSlideCheck()

                # 获取发布时间，判断发布时间是否是当天，是的话才进行下一步操作，不是的话跳出循环进入下一个循环
                pubTime = self.browser1.find_element_by_xpath("//span[@class='_87bab22a14dd86d6a0038ee4b3fdaea4-scss']").text.split("：")[1]
                if(not self.check_publishtime_istoday(pubTime)):
                    # 判断不是当天的视频则跳过
                    continue
                # 获取准确的可下载的视频链接
                try:
                    videoUrl = self.browser1.find_element_by_xpath("//video//source")
                    if (len(videoUrl) > 1):
                        videoUrl = videoUrl[0].get_attribute("src")
                    else:
                        videoUrl = videoUrl.get_attribute("src")
                except Exception as e:
                    continue


                # 抖音标题删除标签
                title = Cleaner_Title.clean_douyin_method2(title=item[0])
                if(title.replace(' ','')==''):
                    continue

                downVideo(urlpath=videoUrl, name=str(i), dstDirPath=videoDirPath)
                # 上传
                print("上传视频: ", i)
                poster.post_videoSingle(str(i) + '.mp4', title0=title)

                # 更新上传过的数据库 postedurldatabase
                sql = "INSERT INTO `postedurldatabase`.`tb_video_posted` (`title`) VALUES ('{}');".format(
                    item[0]
                )
                self.dboperator.insertData2DB(sql=sql)
                i = i + 1
            return videoList
        else:
            return '无更新'


