from selenium import webdriver
import time
import urllib.parse
import json
import requests
import os

from selenium.webdriver.common.desired_capabilities import DesiredCapabilities 

import data.youkuAccount as youkuAccount

Keys = webdriver.common.keys.Keys
ActionChains = webdriver.ActionChains
DesiredCapabilities = webdriver.common.desired_capabilities.DesiredCapabilities

d = DesiredCapabilities.CHROME
d['goog:loggingPrefs'] = { 'performance':'ALL' }

option = webdriver.ChromeOptions()
option.add_argument('log-level=3')

# LoggingPreferences logPrefs = new LoggingPreferences();
# logPrefs.enable( LogType.PERFORMANCE, Level.ALL );
# option.setCapability( "goog:loggingPrefs", logPrefs )

# videoHtmlUrl = 'https://v.youku.com/v_show/id_XMjY4NjM5Mzc0MA==.html'
videoHtmlUrl = 'https://v.youku.com/v_show/id_XNDE4MjY1NjEyOA==.html'

# browser.get(videoHtmlUrl)

singleBrower = None
isLogin = False
class ChromeCatch:
    global isLogin

    def __init__(self, videoIndex, videoName, videoUrl, videoGroupName):
        self.__videoIndex = videoIndex
        self.__videoName = videoName
        self.__videoUrl = videoUrl
        self.__videoGroupName = videoGroupName
        # self.__browser = None # = webdriver.Chrome(options=option, desired_capabilities=d)

    # 使用vip账号，免去广告
    def login(self):
        '''
            使用vip账号，免去广告
        '''

        global isLogin
        global singleBrower
        if isLogin:
            return False
            
        # self.__browser = webdriver.Chrome(options=option, desired_capabilities=d)
        
        singleBrower = webdriver.Chrome(options=option, desired_capabilities=d)
        browser = singleBrower
        
        loginUrl = 'https://account.youku.com/'

        browser.get(loginUrl)

        browser.switch_to_frame("alibaba-login-box")
        browser.find_element_by_class_name('icon-password').click()

        user = youkuAccount.account.get('user')
        pwd = youkuAccount.account.get('pwd')

        browser.find_element_by_id('fm-login-id').send_keys(user)
        browser.find_element_by_id('fm-login-password').send_keys(pwd)
        
        browser.find_element_by_class_name('password-login').click()
        
        isLogin = True
        return True

    # 下载视频中间文件 包括m3u8,视频ts文件,字幕ass文件
    def downloadVideoMidFile(self):
        # browser = self.__browser
        global singleBrower
        
        browser = singleBrower
        browser.get(self.__videoUrl)

        # 切换为1080P
        # browser.execute_script('$(\'.quality-dashboard [data-val="1080p"]\').click()')

        time.sleep(1)

        # 字幕链接
        assLink = '' 
        # m3u8链接
        m3u8Link = ''

        for entry in browser.get_log('performance'):
            messageObj = json.loads(entry['message'])
            try:
                ajaxUrl = messageObj['message']['params']['request']['url']

                if 'm3u8' in ajaxUrl:
                    m3u8Link = ajaxUrl
                elif 'sub.ykimg.com/' in ajaxUrl and '.ass' in ajaxUrl:
                    assLink = ajaxUrl
            except Exception: #异常不处理
                pass

        assFilePath = self.__getFileAssPath()
        m3u8FilePath = self.__getFileM3u8Path()

        fileDir = os.path.dirname(m3u8FilePath)
        if not os.path.exists(fileDir):
            os.makedirs(fileDir)

        if len(assLink)>0:
            with open(assFilePath, 'wb') as p:
                p.write(requests.get(assLink).content)

        with open(m3u8FilePath, 'wb') as p:
            content = requests.get(m3u8Link).content
            p.write(content)

    @staticmethod
    def close():
        global singleBrower

        if singleBrower!=None:
            singleBrower.close()
            singleBrower = None

    # 获取m3u8视频文件的保存路径
    def __getFileM3u8Path(self):
        '''
            获取m3u8视频文件的保存路径
        '''
        return 'download/{0}/{1}_{2}.m3u8'.format(self.__videoGroupName, self.__videoIndex, self.__videoName)

    # 获取ass字幕的保存路径
    def __getFileAssPath(self):
        '''
            获取ass字幕的保存路径
        '''
        return 'download/{0}/{1}_{2}.ass'.format(self.__videoGroupName, self.__videoIndex, self.__videoName)
