# -*- coding: utf-8 -*-
from selenium import webdriver
from HTMLTestRunner import HTMLTestRunner
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
from selenium.webdriver.common.action_chains import ActionChains
import unittest, time, re, os, sys
import pyautogui
#staging測試腳本

playerusername = '<ACCOUNT>'
#輸入帳號，只能大寫

playerpassword = '<REDACTED>'
#輸入密碼

#gamedomain = 'https://example.internal'
gamedomain = 'https://example.internal'
#輸入遊戲網址domain，換環境或測試CDN時會需要

#betrecordurl = 'https://example.internal/'
betrecordurl = 'https://example.internal/'
#輸入投注紀錄網址domain，換環境或測試CDN時會需要

#取得今日日期
def get_day():
    currentday = time.strftime("%Y-%m-%d", time.localtime(time.time()))
    return currentday
#取得今日時間
def get_time():
    currenttime = time.strftime("%Y-%m-%d-%H_%M_%S", time.localtime(time.time()))
    return currenttime
#印出今日日期
def print_day():
    print (get_day())
#印出今日時間
def print_time():
    print (get_time())

#跳轉前網址+遊戲ID
def get_gameoriginalurl(game_id):
    return "http://example.internal/play/is_"+game_id
#跳轉後網址+遊戲ID
def get_slotgameurl(game_id):
    return gamedomain+"/18slot/?gameid="+game_id
def get_scratchgameurl(game_id):
    return gamedomain+"/18scratch/?gameid="+game_id
def get_fruitgameurl(game_id):
    return gamedomain+"/18fruit/?gameid="+game_id




class test_18gamespin(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()
        # driverpath = "C:/selenium/test_case"
        # self.driver = webdriver.Firefox(driverpath)
        self.driver.maximize_window()
        self.driver.implicitly_wait(30)
        self.base_url = "https://www.google.com/"
        self.verificationErrors = []
        self.accept_next_alert = True

    def logininfo(self):
        driver = self.driver
        self.driver.find_element_by_name("username").click()
        self.driver.find_element_by_name("username").clear()
        self.driver.find_element_by_name("username").send_keys(playerusername)
        #帶入帳號
        self.driver.find_element_by_name("password").click()
        self.driver.find_element_by_name("password").clear()
        self.driver.find_element_by_name("password").send_keys(playerpassword)
        #帶入密碼
        self.driver.find_element_by_id("form_login").submit()
        time.sleep(3)

    def test1811(self):
        print_time()
        driver = self.driver
        #打開staging 商戶登陸頁面
        self.driver.get("http://example.internal/")
        time.sleep(3)
        self.logininfo()
        try: 
            self.assertEqual(playerusername, driver.find_element_by_xpath("//li[@id='profile-menu']/a/span[2]").text)
        except AssertionError as e: 
            self.verificationErrors.append(str(e))
            self.print("assertEqual"+playerusername+"passed")
        for i in range(60):
            try:
                if self.is_element_present(example.internal, "balance-total"): 
                    break
            except: 
                pass
            time.sleep(3)
        else: 
            self.fail("time out")
        #打開1811遊戲測試頁面
        self.driver.execute_script("window.open()")
        self.driver.switch_to.window(driver.window_handles[1])
        self.driver.get(get_gameoriginalurl('1811'))
        self.driver.implicitly_wait(30)
        time.sleep(3)
        currentPageUrl = driver.current_url
        print("打開網址是：", currentPageUrl)
        newcurrenturl = currentPageUrl.split('&token=')[0]
        tokenpara = currentPageUrl.split('&token=')[1]
        urltoken = tokenpara.split('&betrecordurl')[0]
        print("跳轉網址前半段是：", newcurrenturl)
        assert newcurrenturl == get_scratchgameurl('1811'), "当前遊戲网址非预期！"
        pic_path = './result/'+get_day()+'\\'
        self.driver.save_screenshot('./result/'+get_day()+'\\'+get_time()+'1811-loading.png')
        time.sleep(5)
        self.driver.save_screenshot('./result/'+get_day()+'\\'+get_time()+'1811-gamepage.png')
        time.sleep(5)
        #x=870  #840+30
        #y=605  #640-35
        canvas = driver.find_element_by_xpath("//canvas")       
        # ActionChains(driver).move_by_offset(1075, 900).click()
        pyautogui.click(x=1420, y=1000)
        #刮刮卡坐標
        # can work on chrome
        time.sleep(5)
        pyautogui.click(x=1420, y=1000)
        # ActionChains(driver).move_to_element_with_offset(canvas, 1075, 900).click().perform()
        # work on firefox
        #ActionChains(driver).move_by_offset(-1075, -900).perform() # 将鼠标位置恢复到移动前 
        self.driver.save_screenshot('./result/'+get_day()+'\\'+get_time()+'1811-spin.png')
        time.sleep(3)
        #打開投注記錄頁面
        self.driver.execute_script("window.open()")
        self.driver.switch_to.window(driver.window_handles[2])
        recordurl = betrecordurl+"?token="+ urltoken +"&lang=id&serverurl=https%3A%2F%2Fexample.internal"
        print(recordurl)
        self.driver.get(recordurl)
        self.driver.implicitly_wait(30)
        print("進入bet record page")
        for i in range(60):
            try:
                if self.is_element_present(By.XPATH, "//table[@id='__BVID__11']/tbody/tr/td[3]"): 
                    break
            except: 
                pass
                self.driver.implicitly_wait(30)
            else: 
                self.fail("time out")
        try: 
            self.assertEqual("Legenda Hanoman", driver.find_element_by_xpath("//table[@id='__BVID__11']/tbody/tr/td[3]").text)
        except AssertionError as e: 
            self.verificationErrors.append(str(e))
    
    def test1812(self):
        print_time()
        driver = self.driver
        #打開staging 商戶登陸頁面
        self.driver.get("http://example.internal/")
        time.sleep(3)
        self.logininfo()
        try: 
            self.assertEqual(playerusername, driver.find_element_by_xpath("//li[@id='profile-menu']/a/span[2]").text)
        except AssertionError as e: 
            self.verificationErrors.append(str(e))
            self.print("assertEqual"+playerusername+"passed")
        for i in range(60):
            try:
                if self.is_element_present(example.internal, "balance-total"): 
                    break
            except: 
                pass
            time.sleep(3)
        else: 
            self.fail("time out")
        #打開1812遊戲測試頁面
        self.driver.execute_script("window.open()")
        self.driver.switch_to.window(driver.window_handles[1])
        self.driver.get(get_gameoriginalurl('1812'))
        self.driver.implicitly_wait(30)
        time.sleep(3)
        currentPageUrl = driver.current_url
        print("打開網址是：", currentPageUrl)
        newcurrenturl = currentPageUrl.split('&token=')[0]
        tokenpara = currentPageUrl.split('&token=')[1]
        urltoken = tokenpara.split('&betrecordurl')[0]
        print("跳轉網址前半段是：", newcurrenturl)
        assert newcurrenturl == get_scratchgameurl('1812'), "当前遊戲网址非预期！"
        pic_path = './result/'+get_day()+'\\'
        self.driver.save_screenshot('./result/'+get_day()+'\\'+get_time()+'1812-loading.png')
        time.sleep(5)
        self.driver.save_screenshot('./result/'+get_day()+'\\'+get_time()+'1812-gamepage.png')
        time.sleep(5)
        #x=870  #840+30
        #y=605  #640-35
        canvas = driver.find_element_by_xpath("//canvas")       
        # ActionChains(driver).move_by_offset(1075, 900).click()
        pyautogui.click(x=1420, y=1000)
        # 刮刮卡坐標
        time.sleep(5)
        pyautogui.click(x=1420, y=1000)
        # can work on chrome
        time.sleep(3)
        # ActionChains(driver).move_to_element_with_offset(canvas, 1075, 900).click().perform()
        # work on firefox
        #ActionChains(driver).move_by_offset(-1075, -900).perform() # 将鼠标位置恢复到移动前 
        self.driver.save_screenshot('./result/'+get_day()+'\\'+get_time()+'1812-spin.png')
        time.sleep(3)
        #打開投注記錄頁面
        self.driver.execute_script("window.open()")
        self.driver.switch_to.window(driver.window_handles[2])
        recordurl = betrecordurl+"?token="+ urltoken +"&lang=id&serverurl=https%3A%2F%2Fexample.internal"
        print(recordurl)
        self.driver.get(recordurl)
        self.driver.implicitly_wait(30)
        print("進入bet record page")
        for i in range(60):
            try:
                if self.is_element_present(By.XPATH, "//table[@id='__BVID__11']/tbody/tr/td[3]"): 
                    break
            except: 
                pass
                self.driver.implicitly_wait(30)
            else: 
                self.fail("time out")
        try: 
            self.assertEqual("Buah Tropis", driver.find_element_by_xpath("//table[@id='__BVID__11']/tbody/tr/td[3]").text)
        except AssertionError as e: 
            self.verificationErrors.append(str(e))

    def test1813(self):
        print_time()
        driver = self.driver
        #打開staging 商戶登陸頁面
        self.driver.get("http://example.internal/")
        time.sleep(3)
        self.logininfo()
        try: 
            self.assertEqual(playerusername, driver.find_element_by_xpath("//li[@id='profile-menu']/a/span[2]").text)
        except AssertionError as e: 
            self.verificationErrors.append(str(e))
            self.print("assertEqual"+playerusername+"passed")
        for i in range(60):
            try:
                if self.is_element_present(example.internal, "balance-total"): 
                    break
            except: 
                pass
            time.sleep(3)
        else: 
            self.fail("time out")
        #打開1813遊戲測試頁面
        self.driver.execute_script("window.open()")
        self.driver.switch_to.window(driver.window_handles[1])
        self.driver.get(get_gameoriginalurl('1813'))
        self.driver.implicitly_wait(30)
        time.sleep(3)
        currentPageUrl = driver.current_url
        print("打開網址是：", currentPageUrl)
        newcurrenturl = currentPageUrl.split('&token=')[0]
        tokenpara = currentPageUrl.split('&token=')[1]
        urltoken = tokenpara.split('&betrecordurl')[0]
        print("跳轉網址前半段是：", newcurrenturl)
        assert newcurrenturl == get_slotgameurl('1813'), "当前遊戲网址非预期！"
        pic_path = './result/'+get_day()+'\\'
        self.driver.save_screenshot('./result/'+get_day()+'\\'+get_time()+'1813-loading.png')
        time.sleep(5)
        self.driver.save_screenshot('./result/'+get_day()+'\\'+get_time()+'1813-gamepage.png')
        time.sleep(5)
        #x=870  #840+30
        #y=605  #640-35
        canvas = driver.find_element_by_xpath("//canvas")       
        # ActionChains(driver).move_by_offset(1075, 900).click()
        # pyautogui.click(x=920, y=1000)
        # can work on chrome / 舊UI座標
        pyautogui.click(x=1680, y=880)
        time.sleep(5)
        # ActionChains(driver).move_to_element_with_offset(canvas, 1075, 900).click().perform()
        # work on firefox
        #ActionChains(driver).move_by_offset(-1075, -900).perform() # 将鼠标位置恢复到移动前 
        self.driver.save_screenshot('./result/'+get_day()+'\\'+get_time()+'1813-spin.png')
        time.sleep(3)
        #打開投注記錄頁面
        self.driver.execute_script("window.open()")
        self.driver.switch_to.window(driver.window_handles[2])
        recordurl = betrecordurl+"?token="+ urltoken +"&lang=id&serverurl=https%3A%2F%2Fexample.internal"
        print(recordurl)
        self.driver.get(recordurl)
        self.driver.implicitly_wait(30)
        print("進入bet record page")
        for i in range(60):
            try:
                if self.is_element_present(By.XPATH, "//table[@id='__BVID__11']/tbody/tr/td[3]"): 
                    break
            except: 
                pass
                self.driver.implicitly_wait(30)
            else: 
                self.fail("time out")
        try: 
            self.assertEqual("Legenda Gatotkaca", driver.find_element_by_xpath("//table[@id='__BVID__11']/tbody/tr/td[3]").text)
        except AssertionError as e: 
            self.verificationErrors.append(str(e))

    def test1815(self):
        print_time()
        driver = self.driver
        #打開staging 商戶登陸頁面
        self.driver.get("http://example.internal/")
        time.sleep(3)
        self.logininfo()
        try: 
            self.assertEqual(playerusername, driver.find_element_by_xpath("//li[@id='profile-menu']/a/span[2]").text)
        except AssertionError as e: 
            self.verificationErrors.append(str(e))
            self.print("assertEqual"+playerusername+"passed")
        for i in range(60):
            try:
                if self.is_element_present(example.internal, "balance-total"): 
                    break
            except: 
                pass
            time.sleep(3)
        else: 
            self.fail("time out")
        #打開1815遊戲測試頁面
        self.driver.execute_script("window.open()")
        self.driver.switch_to.window(driver.window_handles[1])
        self.driver.get(get_gameoriginalurl('1815'))
        self.driver.implicitly_wait(30)
        time.sleep(3)
        currentPageUrl = driver.current_url
        print("打開網址是：", currentPageUrl)
        newcurrenturl = currentPageUrl.split('&token=')[0]
        tokenpara = currentPageUrl.split('&token=')[1]
        urltoken = tokenpara.split('&betrecordurl')[0]
        print("跳轉網址前半段是：", newcurrenturl)
        assert newcurrenturl == get_slotgameurl('1815'), "当前遊戲网址非预期！"
        pic_path = './result/'+get_day()+'\\'
        self.driver.save_screenshot('./result/'+get_day()+'\\'+get_time()+'1815-loading.png')
        time.sleep(5)
        self.driver.save_screenshot('./result/'+get_day()+'\\'+get_time()+'1815-gamepage.png')
        time.sleep(5)
        #x=870  #840+30
        #y=605  #640-35
        canvas = driver.find_element_by_xpath("//canvas")       
        # ActionChains(driver).move_by_offset(1075, 900).click()
        # pyautogui.click(x=920, y=1000)
        # can work on chrome / 舊UI座標
        pyautogui.click(x=1680, y=880)
        time.sleep(5)
        # ActionChains(driver).move_to_element_with_offset(canvas, 1075, 900).click().perform()
        # work on firefox
        #ActionChains(driver).move_by_offset(-1075, -900).perform() # 将鼠标位置恢复到移动前 
        self.driver.save_screenshot('./result/'+get_day()+'\\'+get_time()+'1815-spin.png')
        time.sleep(3)
        #打開投注記錄頁面
        self.driver.execute_script("window.open()")
        self.driver.switch_to.window(driver.window_handles[2])
        recordurl = betrecordurl+"?token="+ urltoken +"&lang=id&serverurl=https%3A%2F%2Fexample.internal"
        print(recordurl)
        self.driver.get(recordurl)
        self.driver.implicitly_wait(30)
        print("進入bet record page")
        for i in range(60):
            try:
                if self.is_element_present(By.XPATH, "//table[@id='__BVID__11']/tbody/tr/td[3]"): 
                    break
            except: 
                pass
                self.driver.implicitly_wait(30)
            else: 
                self.fail("time out")
        try: 
            self.assertEqual("Djakarta", driver.find_element_by_xpath("//table[@id='__BVID__11']/tbody/tr/td[3]").text)
        except AssertionError as e: 
            self.verificationErrors.append(str(e))

    def test1816(self):
        print_time()
        driver = self.driver
        #打開staging 商戶登陸頁面
        self.driver.get("http://example.internal/")
        time.sleep(3)
        self.logininfo()
        try: 
            self.assertEqual(playerusername, driver.find_element_by_xpath("//li[@id='profile-menu']/a/span[2]").text)
        except AssertionError as e: 
            self.verificationErrors.append(str(e))
            self.print("assertEqual"+playerusername+"passed")
        for i in range(60):
            try:
                if self.is_element_present(example.internal, "balance-total"): 
                    break
            except: 
                pass
            time.sleep(3)
        else: 
            self.fail("time out")
        #打開1816遊戲測試頁面
        self.driver.execute_script("window.open()")
        self.driver.switch_to.window(driver.window_handles[1])
        self.driver.get(get_gameoriginalurl('1816'))
        self.driver.implicitly_wait(30)
        time.sleep(3)
        currentPageUrl = driver.current_url
        print("打開網址是：", currentPageUrl)
        newcurrenturl = currentPageUrl.split('&token=')[0]
        tokenpara = currentPageUrl.split('&token=')[1]
        urltoken = tokenpara.split('&betrecordurl')[0]
        print("跳轉網址前半段是：", newcurrenturl)
        assert newcurrenturl == get_slotgameurl('1816'), "当前遊戲网址非预期！"
        pic_path = './result/'+get_day()+'\\'
        self.driver.save_screenshot('./result/'+get_day()+'\\'+get_time()+'1816-loading.png')
        time.sleep(5)
        self.driver.save_screenshot('./result/'+get_day()+'\\'+get_time()+'1816-gamepage.png')
        time.sleep(5)
        #x=870  #840+30
        #y=605  #640-35
        canvas = driver.find_element_by_xpath("//canvas")       
        # ActionChains(driver).move_by_offset(1075, 900).click()
        # pyautogui.click(x=920, y=1000)
        # can work on chrome / 舊UI座標
        pyautogui.click(x=1680, y=880)
        time.sleep(5)
        # ActionChains(driver).move_to_element_with_offset(canvas, 1075, 900).click().perform()
        # work on firefox
        #ActionChains(driver).move_by_offset(-1075, -900).perform() # 将鼠标位置恢复到移动前 
        self.driver.save_screenshot('./result/'+get_day()+'\\'+get_time()+'1816-spin.png')
        time.sleep(3)
        #打開投注記錄頁面
        self.driver.execute_script("window.open()")
        self.driver.switch_to.window(driver.window_handles[2])
        recordurl = betrecordurl+"?token="+ urltoken +"&lang=id&serverurl=https%3A%2F%2Fexample.internal"
        print(recordurl)
        self.driver.get(recordurl)
        self.driver.implicitly_wait(30)
        print("進入bet record page")
        for i in range(60):
            try:
                if self.is_element_present(By.XPATH, "//table[@id='__BVID__11']/tbody/tr/td[3]"): 
                    break
            except: 
                pass
                self.driver.implicitly_wait(30)
            else: 
                self.fail("time out")
        try: 
            self.assertEqual("BALI", driver.find_element_by_xpath("//table[@id='__BVID__11']/tbody/tr/td[3]").text)
        except AssertionError as e: 
            self.verificationErrors.append(str(e))

    def test1817(self):
        print_time()
        driver = self.driver
        #打開staging 商戶登陸頁面
        self.driver.get("http://example.internal/")
        time.sleep(3)
        self.logininfo()
        try: 
            self.assertEqual(playerusername, driver.find_element_by_xpath("//li[@id='profile-menu']/a/span[2]").text)
        except AssertionError as e: 
            self.verificationErrors.append(str(e))
            self.print("assertEqual"+playerusername+"passed")
        for i in range(60):
            try:
                if self.is_element_present(example.internal, "balance-total"): 
                    break
            except: 
                pass
            time.sleep(3)
        else: 
            self.fail("time out")
        #打開1817遊戲測試頁面
        self.driver.execute_script("window.open()")
        self.driver.switch_to.window(driver.window_handles[1])
        self.driver.get(get_gameoriginalurl('1817'))
        self.driver.implicitly_wait(30)
        time.sleep(3)
        currentPageUrl = driver.current_url
        print("打開網址是：", currentPageUrl)
        newcurrenturl = currentPageUrl.split('&token=')[0]
        tokenpara = currentPageUrl.split('&token=')[1]
        urltoken = tokenpara.split('&betrecordurl')[0]
        print("跳轉網址前半段是：", newcurrenturl)
        assert newcurrenturl == get_fruitgameurl('1817'), "当前遊戲网址非预期！"
        pic_path = './result/'+get_day()+'\\'
        self.driver.save_screenshot('./result/'+get_day()+'\\'+get_time()+'1817-loading.png')
        time.sleep(5)
        self.driver.save_screenshot('./result/'+get_day()+'\\'+get_time()+'1817-gamepage.png')
        time.sleep(5)
        #x=870  #840+30
        #y=605  #640-35
        canvas = driver.find_element_by_xpath("//canvas")       
        # ActionChains(driver).move_by_offset(1075, 900).click()
        # pyautogui.click(x=920, y=1000)
        # can work on chrome / 舊UI座標
        pyautogui.click(x=1680, y=880)
        # can work on chrome / 新UI座標
        time.sleep(5)
        # ActionChains(driver).move_to_element_with_offset(canvas, 1075, 900).click().perform()
        # work on firefox
        #ActionChains(driver).move_by_offset(-1075, -900).perform() # 将鼠标位置恢复到移动前 
        self.driver.save_screenshot('./result/'+get_day()+'\\'+get_time()+'1817-spin.png')
        time.sleep(3)
        #打開投注記錄頁面
        self.driver.execute_script("window.open()")
        self.driver.switch_to.window(driver.window_handles[2])
        recordurl = betrecordurl+"?token="+ urltoken +"&lang=id&serverurl=https%3A%2F%2Fexample.internal"
        print(recordurl)
        self.driver.get(recordurl)
        self.driver.implicitly_wait(30)
        print("進入bet record page")
        for i in range(60):
            try:
                if self.is_element_present(By.XPATH, "//table[@id='__BVID__11']/tbody/tr/td[3]"): 
                    break
            except: 
                pass
                self.driver.implicitly_wait(30)
            else: 
                self.fail("time out")
        try: 
            self.assertEqual("Punakawan 777", driver.find_element_by_xpath("//table[@id='__BVID__11']/tbody/tr/td[3]").text)
        except AssertionError as e: 
            self.verificationErrors.append(str(e))

    def test1818(self):
        print_time()
        driver = self.driver
        #打開staging 商戶登陸頁面
        self.driver.get("http://example.internal/")
        time.sleep(3)
        self.logininfo()
        try: 
            self.assertEqual(playerusername, driver.find_element_by_xpath("//li[@id='profile-menu']/a/span[2]").text)
        except AssertionError as e: 
            self.verificationErrors.append(str(e))
            self.print("assertEqual"+playerusername+"passed")
        for i in range(60):
            try:
                if self.is_element_present(example.internal, "balance-total"): 
                    break
            except: 
                pass
            time.sleep(3)
        else: 
            self.fail("time out")
        #打開1818遊戲測試頁面
        self.driver.execute_script("window.open()")
        self.driver.switch_to.window(driver.window_handles[1])
        self.driver.get(get_gameoriginalurl('1818'))
        self.driver.implicitly_wait(30)
        time.sleep(3)
        currentPageUrl = driver.current_url
        print("打開網址是：", currentPageUrl)
        newcurrenturl = currentPageUrl.split('&token=')[0]
        tokenpara = currentPageUrl.split('&token=')[1]
        urltoken = tokenpara.split('&betrecordurl')[0]
        print("跳轉網址前半段是：", newcurrenturl)
        assert newcurrenturl == get_slotgameurl('1818'), "当前遊戲网址非预期！"
        pic_path = './result/'+get_day()+'\\'
        self.driver.save_screenshot('./result/'+get_day()+'\\'+get_time()+'1818-loading.png')
        time.sleep(5)
        self.driver.save_screenshot('./result/'+get_day()+'\\'+get_time()+'1818-gamepage.png')
        time.sleep(5)
        #x=870  #840+30
        #y=605  #640-35
        canvas = driver.find_element_by_xpath("//canvas")       
        # ActionChains(driver).move_by_offset(1075, 900).click()
        # pyautogui.click(x=920, y=1000)
        # can work on chrome / 舊UI座標
        pyautogui.click(x=1680, y=880)
        # can work on chrome / 新UI座標
        time.sleep(5)
        # ActionChains(driver).move_to_element_with_offset(canvas, 1075, 900).click().perform()
        # work on firefox
        #ActionChains(driver).move_by_offset(-1075, -900).perform() # 将鼠标位置恢复到移动前 
        self.driver.save_screenshot('./result/'+get_day()+'\\'+get_time()+'1818-spin.png')
        time.sleep(3)
        #打開投注記錄頁面
        self.driver.execute_script("window.open()")
        self.driver.switch_to.window(driver.window_handles[2])
        recordurl = betrecordurl+"?token="+ urltoken +"&lang=id&serverurl=https%3A%2F%2Fexample.internal"
        print(recordurl)
        self.driver.get(recordurl)
        self.driver.implicitly_wait(30)
        print("進入bet record page")
        for i in range(60):
            try:
                if self.is_element_present(By.XPATH, "//table[@id='__BVID__11']/tbody/tr/td[3]"): 
                    break
            except: 
                pass
                self.driver.implicitly_wait(30)
            else: 
                self.fail("time out")
        try: 
            self.assertEqual("Jumat Kliwon", driver.find_element_by_xpath("//table[@id='__BVID__11']/tbody/tr/td[3]").text)
        except AssertionError as e: 
            self.verificationErrors.append(str(e))

    def test1819(self):
        print_time()
        driver = self.driver
        #打開staging 商戶登陸頁面
        self.driver.get("http://example.internal/")
        time.sleep(3)
        self.logininfo()
        try: 
            self.assertEqual(playerusername, driver.find_element_by_xpath("//li[@id='profile-menu']/a/span[2]").text)
        except AssertionError as e: 
            self.verificationErrors.append(str(e))
            self.print("assertEqual"+playerusername+"passed")
        for i in range(60):
            try:
                if self.is_element_present(example.internal, "balance-total"): 
                    break
            except: 
                pass
            time.sleep(3)
        else: 
            self.fail("time out")
        #打開1819遊戲測試頁面
        self.driver.execute_script("window.open()")
        self.driver.switch_to.window(driver.window_handles[1])
        self.driver.get(get_gameoriginalurl('1819'))
        self.driver.implicitly_wait(30)
        time.sleep(3)
        currentPageUrl = driver.current_url
        print("打開網址是：", currentPageUrl)
        newcurrenturl = currentPageUrl.split('&token=')[0]
        tokenpara = currentPageUrl.split('&token=')[1]
        urltoken = tokenpara.split('&betrecordurl')[0]
        print("跳轉網址前半段是：", newcurrenturl)
        assert newcurrenturl == get_slotgameurl('1819'), "当前遊戲网址非预期！"
        pic_path = './result/'+get_day()+'\\'
        self.driver.save_screenshot('./result/'+get_day()+'\\'+get_time()+'1819-loading.png')
        time.sleep(5)
        self.driver.save_screenshot('./result/'+get_day()+'\\'+get_time()+'1819-gamepage.png')
        time.sleep(5)
        #x=870  #840+30
        #y=605  #640-35
        canvas = driver.find_element_by_xpath("//canvas")       
        # ActionChains(driver).move_by_offset(1075, 900).click()
        # pyautogui.click(x=920, y=1000)
        # can work on chrome / 舊UI座標
        pyautogui.click(x=1680, y=880)
        # can work on chrome / 新UI座標
        time.sleep(5)
        # ActionChains(driver).move_to_element_with_offset(canvas, 1075, 900).click().perform()
        # work on firefox
        #ActionChains(driver).move_by_offset(-1075, -900).perform() # 将鼠标位置恢复到移动前 
        self.driver.save_screenshot('./result/'+get_day()+'\\'+get_time()+'1819-spin.png')
        time.sleep(3)
        #打開投注記錄頁面
        self.driver.execute_script("window.open()")
        self.driver.switch_to.window(driver.window_handles[2])
        recordurl = betrecordurl+"?token="+ urltoken +"&lang=id&serverurl=https%3A%2F%2Fexample.internal"
        print(recordurl)
        self.driver.get(recordurl)
        self.driver.implicitly_wait(30)
        print("進入bet record page")
        for i in range(60):
            try:
                if self.is_element_present(By.XPATH, "//table[@id='__BVID__11']/tbody/tr/td[3]"): 
                    break
            except: 
                pass
                self.driver.implicitly_wait(30)
            else: 
                self.fail("time out")
        try: 
            self.assertEqual("Jagawana 777", driver.find_element_by_xpath("//table[@id='__BVID__11']/tbody/tr/td[3]").text)
        except AssertionError as e: 
            self.verificationErrors.append(str(e))

    def test1820(self):
        print_time()
        driver = self.driver
        #打開staging 商戶登陸頁面
        self.driver.get("http://example.internal/")
        time.sleep(3)
        self.logininfo()
        try: 
            self.assertEqual(playerusername, driver.find_element_by_xpath("//li[@id='profile-menu']/a/span[2]").text)
        except AssertionError as e: 
            self.verificationErrors.append(str(e))
            self.print("assertEqual"+playerusername+"passed")
        for i in range(60):
            try:
                if self.is_element_present(example.internal, "balance-total"): 
                    break
            except: 
                pass
            time.sleep(3)
        else: 
            self.fail("time out")
        #打開1820遊戲測試頁面
        self.driver.execute_script("window.open()")
        self.driver.switch_to.window(driver.window_handles[1])
        self.driver.get(get_gameoriginalurl('1820'))
        self.driver.implicitly_wait(30)
        time.sleep(3)
        currentPageUrl = driver.current_url
        print("打開網址是：", currentPageUrl)
        newcurrenturl = currentPageUrl.split('&token=')[0]
        tokenpara = currentPageUrl.split('&token=')[1]
        urltoken = tokenpara.split('&betrecordurl')[0]
        print("跳轉網址前半段是：", newcurrenturl)
        assert newcurrenturl == get_fruitgameurl('1820'), "当前遊戲网址非预期！"
        pic_path = './result/'+get_day()+'\\'
        self.driver.save_screenshot('./result/'+get_day()+'\\'+get_time()+'1820-loading.png')
        time.sleep(5)
        self.driver.save_screenshot('./result/'+get_day()+'\\'+get_time()+'1820-gamepage.png')
        time.sleep(5)
        #x=870  #840+30
        #y=605  #640-35
        canvas = driver.find_element_by_xpath("//canvas")       
        # ActionChains(driver).move_by_offset(1075, 900).click()
        # pyautogui.click(x=920, y=1000)
        # can work on chrome / 舊UI座標
        pyautogui.click(x=1680, y=880)
        # can work on chrome / 新UI座標
        time.sleep(5)
        # ActionChains(driver).move_to_element_with_offset(canvas, 1075, 900).click().perform()
        # work on firefox
        #ActionChains(driver).move_by_offset(-1075, -900).perform() # 将鼠标位置恢复到移动前 
        self.driver.save_screenshot('./result/'+get_day()+'\\'+get_time()+'1820-spin.png')
        time.sleep(3)
        #打開投注記錄頁面
        self.driver.execute_script("window.open()")
        self.driver.switch_to.window(driver.window_handles[2])
        recordurl = betrecordurl+"?token="+ urltoken +"&lang=id&serverurl=https%3A%2F%2Fexample.internal"
        print(recordurl)
        self.driver.get(recordurl)
        self.driver.implicitly_wait(30)
        print("進入bet record page")
        for i in range(60):
            try:
                if self.is_element_present(By.XPATH, "//table[@id='__BVID__11']/tbody/tr/td[3]"): 
                    break
            except: 
                pass
                self.driver.implicitly_wait(30)
            else: 
                self.fail("time out")
        try: 
            self.assertEqual("Pujasera", driver.find_element_by_xpath("//table[@id='__BVID__11']/tbody/tr/td[3]").text)
        except AssertionError as e: 
            self.verificationErrors.append(str(e))

    def test1822(self):
        print_time()
        driver = self.driver
        #打開staging 商戶登陸頁面
        self.driver.get("http://example.internal/")
        time.sleep(3)
        self.logininfo()
        try: 
            self.assertEqual(playerusername, driver.find_element_by_xpath("//li[@id='profile-menu']/a/span[2]").text)
        except AssertionError as e: 
            self.verificationErrors.append(str(e))
            self.print("assertEqual"+playerusername+"passed")
        for i in range(60):
            try:
                if self.is_element_present(example.internal, "balance-total"): 
                    break
            except: 
                pass
            time.sleep(3)
        else: 
            self.fail("time out")
        #打開1822遊戲測試頁面
        self.driver.execute_script("window.open()")
        self.driver.switch_to.window(driver.window_handles[1])
        self.driver.get(get_gameoriginalurl('1822'))
        self.driver.implicitly_wait(30)
        time.sleep(3)
        currentPageUrl = driver.current_url
        print("打開網址是：", currentPageUrl)
        newcurrenturl = currentPageUrl.split('&token=')[0]
        tokenpara = currentPageUrl.split('&token=')[1]
        urltoken = tokenpara.split('&betrecordurl')[0]
        print("跳轉網址前半段是：", newcurrenturl)
        assert newcurrenturl == get_slotgameurl('1822'), "当前遊戲网址非预期！"
        pic_path = './result/'+get_day()+'\\'
        self.driver.save_screenshot('./result/'+get_day()+'\\'+get_time()+'1822-loading.png')
        time.sleep(5)
        self.driver.save_screenshot('./result/'+get_day()+'\\'+get_time()+'1822-gamepage.png')
        time.sleep(5)
        #x=870  #840+30
        #y=605  #640-35
        canvas = driver.find_element_by_xpath("//canvas")       
        # ActionChains(driver).move_by_offset(1075, 900).click()
        # pyautogui.click(x=920, y=1000)
        # can work on chrome / 舊UI座標
        pyautogui.click(x=1680, y=880)
        # can work on chrome / 新UI座標
        time.sleep(5)
        # ActionChains(driver).move_to_element_with_offset(canvas, 1075, 900).click().perform()
        # work on firefox
        #ActionChains(driver).move_by_offset(-1075, -900).perform() # 将鼠标位置恢复到移动前 
        self.driver.save_screenshot('./result/'+get_day()+'\\'+get_time()+'1822-spin.png')
        time.sleep(3)
        #打開投注記錄頁面
        self.driver.execute_script("window.open()")
        self.driver.switch_to.window(driver.window_handles[2])
        recordurl = betrecordurl+"?token="+ urltoken +"&lang=id&serverurl=https%3A%2F%2Fexample.internal"
        print(recordurl)
        self.driver.get(recordurl)
        self.driver.implicitly_wait(30)
        print("進入bet record page")
        for i in range(60):
            try:
                if self.is_element_present(By.XPATH, "//table[@id='__BVID__11']/tbody/tr/td[3]"): 
                    break
            except: 
                pass
                self.driver.implicitly_wait(30)
            else: 
                self.fail("time out")
        try: 
            self.assertEqual("Komodo Romantis", driver.find_element_by_xpath("//table[@id='__BVID__11']/tbody/tr/td[3]").text)
        except AssertionError as e: 
            self.verificationErrors.append(str(e))

    def is_element_present(self, how, what):
        try: self.driver.find_element(by=how, value=what)
        except NoSuchElementException as e: return False
        return True
    
    def is_alert_present(self):
        try: self.driver.switch_to_alert()
        except NoAlertPresentException as e: return False
        return True
    
    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally: self.accept_next_alert = True

    def tearDown(self):
        print('Test finished')
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)


if __name__ == "__main__":
    #unittest.main()
    file_path = './result/'+get_day()
    if os.path.exists(file_path):
        print("路徑存在。")
    else:
        print("路徑不存在。")
        os.mkdir(file_path)
        print("create successfully")
    unittest=unittest.TestSuite() #將測試用例加入到測試容器中
    unittest.addTest(test_18gamespin("test1811")) 
    unittest.addTest(test_18gamespin("test1812"))
    unittest.addTest(test_18gamespin("test1813"))
    unittest.addTest(test_18gamespin("test1815"))
    unittest.addTest(test_18gamespin("test1816"))
    unittest.addTest(test_18gamespin("test1817"))
    unittest.addTest(test_18gamespin("test1818"))
    unittest.addTest(test_18gamespin("test1819"))
    unittest.addTest(test_18gamespin("test1820"))
    unittest.addTest(test_18gamespin("test1822"))
    # unittest.addTest(LoginTest("test_gotogame"))
    # unittest.addTest(LoginTest("is_element_present"))
    # unittest.addTest(LoginTest("is_alert_present"))
    # unittest.addTest(LoginTest("close_alert_and_get_its_text"))

    #将测试结果写入到result.html中
    fp=open(get_time()+"-18 result.html",'wb')
    runner=HTMLTestRunner(stream=fp,title='18 Test Report',description='Result:',tester='jay')
    runner.run(unittest)
    fp.close()