from selenium import webdriver
import time
import urllib.parse
import json
import requests
import os

from selenium.webdriver.common.desired_capabilities import DesiredCapabilities 

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
   
browser = webdriver.Chrome(options=option, desired_capabilities=d)
loginUrl = 'https://account.youku.com/'
browser.get('https://account.youku.com/')
