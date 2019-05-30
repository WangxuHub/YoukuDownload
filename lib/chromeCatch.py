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
browser = None # = webdriver.Chrome(options=option, desired_capabilities=d)


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

    # 使用vip账号，免去广告
    @staticmethod
    def login():
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

def videoLoad():
    try:
        browser.get(videoHtmlUrl)

        # 切换为1080P
        browser.execute_script('$(\'.quality-dashboard [data-val="1080p"]\').click()')

        time.sleep(5)

        # playBarDom = browser.find_element_by_id()

        # ActionChains(browser).move_to_element
        # videoDom = browser.find_element_by_tag_name('video')

        # totalSecond = float(videoDom.get_attribute('duration')) - 2
        # currentTime = 0
        # fastScript = '$("video")[0].currentTime={0}'
                
        # while currentTime < 60:
        # while currentTime < totalSecond:
        #     browser.execute_script(fastScript.format(currentTime))
        #     time.sleep(0.4)
        #     currentTime = float(videoDom.get_attribute('currentTime'))+8
        #     print('current:{0}'.format(currentTime))
    except Exception as e:
        print(e)


# 拦截所有视频的ts
def  catchVideoTs():    
    videoTsList = []
    for entry in browser.get_log('performance'):
        messageObj = json.loads(entry['message'])
        try:
            ajaxUrl = messageObj['message']['params']['request']['url']

            if 'cp31.ott.cibntv.net' in ajaxUrl:
                videoTsList.append(ajaxUrl)
        except Exception: 
            pass

    if not os.path.exists('hy/1'):
        os.makedirs('hy/1')

    index = 0
    for item in videoTsList:
        content = requests.get(item).content
        if len(content) < 70000:
            print(item)
            print('===============================')
            print(content)
            continue
        if index == 0:
            with open('hy/1/123.ts', 'wb') as p:
                p.write(content)
                print(str(index) + 'load finish')
        else:
            with open('hy/1/123.ts', 'ab+') as p:
                p.write(content)
                print(str(index) + 'load finish')
        index += 1



    def getVideoInfo(self):
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

        fileDir = 'hy/csy'
        if not os.path.exists(fileDir):
            os.makedirs(fileDir)

        if len(assLink)>0:
            with open(fileDir + '/11.ass', 'wb') as p:
                p.write(requests.get(assLink).content)
                print('ass load finish')

        with open(fileDir + '/11.m3u8', 'wb') as p:
            content = requests.get(m3u8Link).content
            p.write(content)
            print('m3u8 load finish')
       
    # 过期方法
    def m3u8ToMp4():
        # 视频字幕
        # assUrl = 'http://sub.ykimg.com/01006401005CDBC802BB78000000011DAD68EC-6CF6-4700-86FA-66083F96846C.ass'

        # # 视频信息 截取
        # tempUrl = 'https://acs.youku.com/h5/mtop.youku.play.ups.appinfo.get/1.1/?jsv=2.4.16&appKey=24679788&t=1558944641486&sign=24f34bdc898138ef9f5b5005428b5097&api=mtop.youku.play.ups.appinfo.get&v=1.1&timeout=20000&YKPid=20160317PLF000211&YKLoginRequest=true&AntiFlood=true&AntiCreep=true&type=jsonp&dataType=jsonp&callback=mtopjsonp1&data=%7B%22steal_params%22%3A%22%7B%5C%22ccode%5C%22%3A%5C%220502%5C%22%2C%5C%22client_ip%5C%22%3A%5C%22192.168.1.1%5C%22%2C%5C%22utid%5C%22%3A%5C%22t31yFdbKem4CAXPNk4SztuJJ%5C%22%2C%5C%22client_ts%5C%22%3A1558944641%2C%5C%22version%5C%22%3A%5C%221.4.2%5C%22%2C%5C%22ckey%5C%22%3A%5C%22118%23ZVWZzSkURPdYOe43BeJQZYquZYT4zHWzagg4NsTIiIJtbFmhhHRxZZgZZzqhzHRzZgCZXfquze2zZZFhHluhzZ2ZZ0NTzeWzzgFuVfq4zH2ZZZChXHWVZggZZzqhzHRZZXquVfqt7H8wZIs1ZgJwzwFeBgx1xkW%2FnZ7daDTINiAZEggJZxuD2CK9mgSBLSJ%2FtPejFoNlstLTsKYX6eACugZCmrDtKHZzh7RuzlYCRZZTtW%2BWPMAKwaIG4S%2BJjfVmN4HeyZUNtxtKSEbJoey8bpxESe%2B8NknXNbvMyFr0k5zQNK%2FvRUcnAsKq5269OCNC%2Fd1%2FBAZ1idzIKKKiL3p1WJMu8BFJC%2BHeFN%2F93ifUZRVliej%2B%2B6xK2p1CgFSYnlv74ibzDk2GPaH1R1fbuJ%2FmaieejwdlxfPyzgM5TibuFBiW5JsTcPigkodTmpt8VNTrFo9relJth6FKtII0BaPlomNIbSSxdOrNa18ROFThmnpsQVTeSQRnNU7F8HVArObBpVK8geWE21WVgS%2FkndGDZeKM5DDA5DpMmzJQSJ2Ibtfx6ypZXczxbKcJZjYLJc6CvhFqOIt974X0VgLX8O1zSphi%5C%22%7D%22%2C%22biz_params%22%3A%22%7B%5C%22vid%5C%22%3A%5C%22XNDE4MjY1NjEyOA%3D%3D%5C%22%2C%5C%22play_ability%5C%22%3A1024%2C%5C%22current_showid%5C%22%3A%5C%22316449%5C%22%2C%5C%22master_m3u8%5C%22%3A0%2C%5C%22media_type%5C%22%3A%5C%22standard%2Csubtitle%5C%22%2C%5C%22app_ver%5C%22%3A%5C%221.4.2%5C%22%7D%22%2C%22ad_params%22%3A%22%7B%5C%22vs%5C%22%3A%5C%221.0%5C%22%2C%5C%22pver%5C%22%3A%5C%221.4.2%5C%22%2C%5C%22sver%5C%22%3A%5C%221.1%5C%22%2C%5C%22site%5C%22%3A1%2C%5C%22aw%5C%22%3A%5C%22w%5C%22%2C%5C%22fu%5C%22%3A0%2C%5C%22d%5C%22%3A%5C%220%5C%22%2C%5C%22bt%5C%22%3A%5C%22pc%5C%22%2C%5C%22os%5C%22%3A%5C%22win%5C%22%2C%5C%22osv%5C%22%3A%5C%2210%5C%22%2C%5C%22dq%5C%22%3A%5C%22auto%5C%22%2C%5C%22atm%5C%22%3A%5C%22%5C%22%2C%5C%22partnerid%5C%22%3A%5C%22null%5C%22%2C%5C%22wintype%5C%22%3A%5C%22interior%5C%22%2C%5C%22isvert%5C%22%3A0%2C%5C%22vip%5C%22%3A0%2C%5C%22emb%5C%22%3A%5C%22AjEwNDU2NjQwMzICdi55b3VrdS5jb20CL3Zfc2hvdy9pZF9YTkRFNE1qWTFOakV5T0E9PS5odG1s%5C%22%2C%5C%22p%5C%22%3A1%2C%5C%22rst%5C%22%3A%5C%22mp4%5C%22%2C%5C%22needbf%5C%22%3A2%7D%22%7D'
        # cmdStr ='.\ffmpeg.exe -protocol_whitelist "file,http,https,rtp,udp,tcp,tls"  -i .\123.m3u8 123.mp4'

        cmdStr = r'.\tools\ffmpeg.exe -protocol_whitelist "file,http,https,rtp,udp,tcp,tls"  -i .\hy\csy\11.m3u8 .\hy\csy\11.mp4'
        os.system(cmdStr)
        pass

# login()
# videoLoad()
# # catchVideoTs()
# getVideoInfo()

# m3u8ToMp4()
