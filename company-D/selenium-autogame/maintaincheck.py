# -*- coding: utf-8 -*-
from selenium import webdriver
from HTMLTestRunner import HTMLTestRunner
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
from selenium.webdriver.chrome.options import Options
import unittest, time, re, os, sys

pic_path = './result/maintain/'

options = webdriver.ChromeOptions()
# staging測試腳本
# class test_maintaincheck(unittest.TestCase):

prefs = {
    'profile.default_content_setting_values' :
        {
        'notifications' : 2
         }
}
options.add_experimental_option('prefs',prefs)
options.add_argument("--headless")            #不開啟實體瀏覽器背景執行
options.add_argument("--start-maximized")     #最大化視窗
options.add_argument("--incognito")           #開啟無痕模式


urllist = [
('agent-01','http://example.internal/slots/<PRODUCT>'),
('agent-02','https://example.internal/our-games'),
('agent-03','https://example.internal/slots/<PRODUCT>'),
('agent-04','https://example.internal/slots'),
('agent-05','https://example.internal/slots'),
('agent-06','https://example.internal/slots?category=7'),
('agent-07','https://example.internal/id/db/slot/<PRODUCT>-<PRODUCT>'),
('agent-08','https://example.internal/slots/<PRODUCT>'),
('agent-09','https://example.internal/games'),
('agent-10','https://example.internal/our-games/<PRODUCT>'),
('agent-11','https://example.internal/our-games/<PRODUCT>'),
('agent-12','https://example.internal/id/db/slot'),
('agent-13','https://example.internal/id/db/slot/<PRODUCT>-<PRODUCT>'),
('agent-14','https://example.internal/slot/<PRODUCT>-slot'),
('agent-15','https://example.internal/our-games/<PRODUCT>'),
('agent-16','https://example.internal/our-games/<PRODUCT>'),
('agent-17','https://example.internal/our-games/<PRODUCT>'),
('agent-18','https://example.internal/our-games/<PRODUCT>'),
('agent-19','https://example.internal/our-games/<PRODUCT>'),
('agent-20','https://example.internal/our-games/<PRODUCT>'),
('agent-21','https://example.internal/our-games/<PRODUCT>'),
('agent-22','https://example.internal/our-games/<PRODUCT>'),
('agent-23','https://example.internal/our-games/<PRODUCT>'),
('agent-24','https://example.internal/games/slots?category=<PRODUCT>-<PRODUCT>'),
('agent-25','https://example.internal/game/slots'),
('agent-26','https://example.internal/game/slots'),
('agent-27','https://example.internal/game/slots'),
('agent-28','https://example.internal/game/slots'),
('agent-29','http://example.internal/game/slots'),
('agent-30','https://example.internal/game/slots'),
('agent-31','https://example.internal/game/slots?category=<PRODUCT>-<PRODUCT>'),
('agent-32','https://example.internal/game/slots'),
('agent-33','https://example.internal/'),
('agent-34','https://example.internal/'),
('agent-35','https://example.internal/'),
('agent-36','https://example.internal/'),
('agent-37','https://example.internal/'),
('agent-38','https://example.internal/'),
('agent-39','http://example.internal/'),
('agent-40','http://example.internal/slotsrule'),
('agent-41','https://example.internal/'),
('agent-42','https://example.internal/'),
('agent-43','https://example.internal/'),
('agent-44','https://example.internal/'),
('agent-45','https://example.internal/sports/live')
]

urllist.sort(key =lambda s:s[0])

for (agentcode,link) in urllist :
    driver = webdriver.Chrome(chrome_options=options)
    driver.set_window_size(2400, 1350)
    # driver.set_window_size(1920, 1080) 標準尺寸
    driver.maximize_window()
    # driver.fullscreen_window() 無法使用
    driver.get(link)
    print(driver.current_url)
    print(driver.title)
    print(agentcode)
    time.sleep(8)
    driver.save_screenshot('./result/maintain/'+agentcode+'.png')
    driver.quit()  