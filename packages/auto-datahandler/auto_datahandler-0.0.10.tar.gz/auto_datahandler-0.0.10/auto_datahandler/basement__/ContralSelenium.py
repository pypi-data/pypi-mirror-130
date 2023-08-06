from selenium import webdriver
import time
from .universal import u_selenium
from selenium.webdriver import Remote
from selenium.webdriver.chrome import options
from selenium.common.exceptions import InvalidArgumentException

# Selenium driver多进程调用的类
class ReuseChrome(Remote):
    def __init__(self, command_executor, session_id):
        self.r_session_id = session_id
        Remote.__init__(self, command_executor=command_executor, desired_capabilities={})

    def start_session(self, capabilities, browser_profile=None):
        """重写该方法"""
        if(not isinstance(capabilities, dict)):
            raise InvalidArgumentException("Capabilities must be a dictionary")
        if(browser_profile):
            if("moz:firefoxOptions" in capabilities):
                capabilities["moz:firefoxOptions"]["profile"] = browser_profile.encoded
            else:
                capabilities.update({"firefox_profile": browser_profile.encoded})
        self.capabilities = options.Options().to_capabilities()
        self.session_id = self.r_session_id
        self.w3c = False

# 通过selenium获取指定信息的类
class Base_Selenium(
    u_selenium.Roll_To_Bottom,
    u_selenium.Close_Browser,
    u_selenium.Click_Element
):
    def __init__(self, *driverPath):
        if(driverPath!=()):
            self.browser = self.init_webdriver(chromeDriverPath=driverPath)

    def init_webdriver(self, chromeDriverPath):
        """
        创建输出webdriver对象
        :chromeDriverPath 引擎的路径
        :option
        """
        option = webdriver.ChromeOptions()
        option.add_experimental_option('excludeSwitches', ['enable-automation'])
        option.add_argument('--disable-blink-features=AutomationControlled')
        browser = webdriver.Chrome(executable_path=chromeDriverPath, options=option)
        return browser

    def add_agent(self, proxyHost="u7125.5.tp.16yun.cn", proxyPort= "6445", proxyUser="16OINIUS", proxyPass= "971935", browser_driver_path="E:\Projects\webDriver\\chrome\\chromedriver.exe"):
        """创建添加爬虫代理的browser 根据不同代理源再customFunction__.Contraler_selenium.contraler_selenium 中重写"""
        pass

    def getCookies(self, browser, *url):
        '''
        类方法，以对象形式输出指定链接返回的cookies
        :param url: 待打开的链接
        :param browser: 浏览器引擎
        :return: cookies对象
        '''
        # 获取cookie
        dictCookies = browser.get_cookies()
        cookies = {}
        for item in dictCookies:
            key = item['name']
            cookies[str(key)] = str(item['value'])
        return cookies

    def del_all_cookies(self):
        self.browser.delete_all_cookies()

    def get_params(self, url, *browser):
        if(browser==()):
            self.browser.get(url)
            time.sleep(1)
            cookies = self.getCookies(url, self.browser)
            headers = {}
            return {
                'cookies': cookies,
                'headers': headers
            }
        else:
            browser.get(url)
            time.sleep(1)
            cookies = self.getCookies(url, browser)
            headers = {}
            return {
                'cookies': cookies,
                'headers': headers
            }

    def closeBrowser(self, *browser):
        '''
        关闭指定浏览器，若浏览器为None则关闭对象浏览器
        :param browser:
        :return: None
        '''
        if(browser==()):
            self.browser.close()
        else:
            browser.close()



