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
browser = webdriver.Chrome(options=option, desired_capabilities=d)


# videoHtmlUrl = 'https://v.youku.com/v_show/id_XMjY4NjM5Mzc0MA==.html'
videoHtmlUrl = 'https://v.youku.com/v_show/id_XNDE4MjY1NjEyOA==.html'

# browser.get(videoHtmlUrl)

# 使用vip账号，免去广告
def login():
    loginUrl = 'https://account.youku.com/?callback={0}'.format(urllib.parse.quote(videoHtmlUrl))

    browser.get(loginUrl)

    browser.find_element_by_id('YT-showNormalLogin-text').click()

    user = youkuAccount.account.get('user')
    pwd = youkuAccount.account.get('pwd')

    browser.find_element_by_id('YT-ytaccount').send_keys(user)
    browser.find_element_by_id('YT-ytpassword').send_keys(pwd)
    
    browser.find_element_by_id('YT-nloginSubmit').click()


def videoLoad():
    try:
        browser.get(videoHtmlUrl)
        # playBarDom = browser.find_element_by_id()

        # ActionChains(browser).move_to_element
        videoDom = browser.find_element_by_tag_name('video')

        totalSecond = float(videoDom.get_attribute('duration')) - 2
        currentTime = 0
        fastScript = '$("video")[0].currentTime={0}'
        
        # while currentTime < 60:
        while currentTime < totalSecond:
            browser.execute_script(fastScript.format(currentTime))
            time.sleep(0.4)
            currentTime = float(videoDom.get_attribute('currentTime'))+8
            print('current:{0}'.format(currentTime))
    except Exception as e:
        print(e)


# 拦截所有视频的ts
def  catchVideoTs():
    # script = 'return performance.getEntries()'
    # list = browser.execute_script(script)
    # print(list)
    # browser.get_network_conditions
    
    videoTsList = []
    for entry in browser.get_log('performance'):
        messageObj = json.loads(entry['message'])
        try:
            ajaxUrl = messageObj['message']['params']['request']['url']
            if 'cp31.ott.cibntv.net' in ajaxUrl:
                # print('videoDataUrl:'+ajaxUrl)
                videoTsList.append(ajaxUrl)
        except Exception: #异常不处理
            pass
        #print(entry['url'])
    #print "Register: 

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

# 在写入的时候，直接就进行合并了         
# def concatVideo():
#     os.system('cd hy/1 & copy /b *.ts new.ts')
#     pass

def m3u8ToMp4():
    # 视频字幕
    assUrl = 'http://sub.ykimg.com/01006401005CDBC802BB78000000011DAD68EC-6CF6-4700-86FA-66083F96846C.ass'

    # 视频信息 截取
    tempUrl = 'https://acs.youku.com/h5/mtop.youku.play.ups.appinfo.get/1.1/?jsv=2.4.16&appKey=24679788&t=1558944641486&sign=24f34bdc898138ef9f5b5005428b5097&api=mtop.youku.play.ups.appinfo.get&v=1.1&timeout=20000&YKPid=20160317PLF000211&YKLoginRequest=true&AntiFlood=true&AntiCreep=true&type=jsonp&dataType=jsonp&callback=mtopjsonp1&data=%7B%22steal_params%22%3A%22%7B%5C%22ccode%5C%22%3A%5C%220502%5C%22%2C%5C%22client_ip%5C%22%3A%5C%22192.168.1.1%5C%22%2C%5C%22utid%5C%22%3A%5C%22t31yFdbKem4CAXPNk4SztuJJ%5C%22%2C%5C%22client_ts%5C%22%3A1558944641%2C%5C%22version%5C%22%3A%5C%221.4.2%5C%22%2C%5C%22ckey%5C%22%3A%5C%22118%23ZVWZzSkURPdYOe43BeJQZYquZYT4zHWzagg4NsTIiIJtbFmhhHRxZZgZZzqhzHRzZgCZXfquze2zZZFhHluhzZ2ZZ0NTzeWzzgFuVfq4zH2ZZZChXHWVZggZZzqhzHRZZXquVfqt7H8wZIs1ZgJwzwFeBgx1xkW%2FnZ7daDTINiAZEggJZxuD2CK9mgSBLSJ%2FtPejFoNlstLTsKYX6eACugZCmrDtKHZzh7RuzlYCRZZTtW%2BWPMAKwaIG4S%2BJjfVmN4HeyZUNtxtKSEbJoey8bpxESe%2B8NknXNbvMyFr0k5zQNK%2FvRUcnAsKq5269OCNC%2Fd1%2FBAZ1idzIKKKiL3p1WJMu8BFJC%2BHeFN%2F93ifUZRVliej%2B%2B6xK2p1CgFSYnlv74ibzDk2GPaH1R1fbuJ%2FmaieejwdlxfPyzgM5TibuFBiW5JsTcPigkodTmpt8VNTrFo9relJth6FKtII0BaPlomNIbSSxdOrNa18ROFThmnpsQVTeSQRnNU7F8HVArObBpVK8geWE21WVgS%2FkndGDZeKM5DDA5DpMmzJQSJ2Ibtfx6ypZXczxbKcJZjYLJc6CvhFqOIt974X0VgLX8O1zSphi%5C%22%7D%22%2C%22biz_params%22%3A%22%7B%5C%22vid%5C%22%3A%5C%22XNDE4MjY1NjEyOA%3D%3D%5C%22%2C%5C%22play_ability%5C%22%3A1024%2C%5C%22current_showid%5C%22%3A%5C%22316449%5C%22%2C%5C%22master_m3u8%5C%22%3A0%2C%5C%22media_type%5C%22%3A%5C%22standard%2Csubtitle%5C%22%2C%5C%22app_ver%5C%22%3A%5C%221.4.2%5C%22%7D%22%2C%22ad_params%22%3A%22%7B%5C%22vs%5C%22%3A%5C%221.0%5C%22%2C%5C%22pver%5C%22%3A%5C%221.4.2%5C%22%2C%5C%22sver%5C%22%3A%5C%221.1%5C%22%2C%5C%22site%5C%22%3A1%2C%5C%22aw%5C%22%3A%5C%22w%5C%22%2C%5C%22fu%5C%22%3A0%2C%5C%22d%5C%22%3A%5C%220%5C%22%2C%5C%22bt%5C%22%3A%5C%22pc%5C%22%2C%5C%22os%5C%22%3A%5C%22win%5C%22%2C%5C%22osv%5C%22%3A%5C%2210%5C%22%2C%5C%22dq%5C%22%3A%5C%22auto%5C%22%2C%5C%22atm%5C%22%3A%5C%22%5C%22%2C%5C%22partnerid%5C%22%3A%5C%22null%5C%22%2C%5C%22wintype%5C%22%3A%5C%22interior%5C%22%2C%5C%22isvert%5C%22%3A0%2C%5C%22vip%5C%22%3A0%2C%5C%22emb%5C%22%3A%5C%22AjEwNDU2NjQwMzICdi55b3VrdS5jb20CL3Zfc2hvdy9pZF9YTkRFNE1qWTFOakV5T0E9PS5odG1s%5C%22%2C%5C%22p%5C%22%3A1%2C%5C%22rst%5C%22%3A%5C%22mp4%5C%22%2C%5C%22needbf%5C%22%3A2%7D%22%7D'
    cmdStr ='.\ffmpeg.exe -protocol_whitelist "file,http,https,rtp,udp,tcp,tls"  -i .\123.m3u8 123.mp4'
    pass

login()
videoLoad()
catchVideoTs()
#concatVideo()