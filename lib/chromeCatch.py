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
d['loggingPrefs'] = { 'performance':'ALL' }

option = webdriver.ChromeOptions()
option.add_argument('log-level=3')

# videoHtmlUrl = 'https://v.youku.com/v_show/id_XMjY4NjM5Mzc0MA==.html'
videoHtmlUrl = 'https://v.youku.com/v_show/id_XNDE4MjY1NjEyOA==.html'

# browser.get(videoHtmlUrl)

isLogin = False
class ChromeCatch:
    global isLogin

    def __init__(self, videoIndex, videoName, videoUrl, videoGroupName):
        self.__videoIndex = videoIndex
        self.__videoName = videoName
        self.__videoUrl = videoUrl
        self.__videoGroupName = videoGroupName
        self.__browser = None # = webdriver.Chrome(options=option, desired_capabilities=d)

    # 使用vip账号，免去广告
    def login(self):
        '''
            使用vip账号，免去广告
        '''

        global isLogin
        if isLogin:
            return False
            
        global browser    
        browser = webdriver.Chrome(options=option, desired_capabilities=d)
        # loginUrl = 'https://account.youku.com/?callback={0}'.format(urllib.parse.quote(videoHtmlUrl))
        loginUrl = 'https://account.youku.com/'

        browser = self.__browser
        print('before get')
        browser.get(loginUrl)
        print('after get')

        browser.find_element_by_id('YT-showNormalLogin-text').click()

        user = youkuAccount.account.get('user')
        pwd = youkuAccount.account.get('pwd')

        browser.find_element_by_id('YT-ytaccount').send_keys(user)
        browser.find_element_by_id('YT-ytpassword').send_keys(pwd)
        
        browser.find_element_by_id('YT-nloginSubmit').click()
        
        isLogin = True
        return True

    # 下载视频中间文件 包括m3u8,视频ts文件,字幕ass文件
    def downloadVideoMidFile(self):
        browser = self.__browser
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
