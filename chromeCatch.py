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


videoHtmlUrl = 'https://v.youku.com/v_show/id_XMjY4NjM5Mzc0MA==.html'
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

# 在写入的时候，直接就进行和平了         
# def concatVideo():
#     os.system('cd hy/1 & copy /b *.ts new.ts')
#     pass

login()
videoLoad()
catchVideoTs()
#concatVideo()