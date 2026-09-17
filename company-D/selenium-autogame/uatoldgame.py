# -*- coding: utf-8 -*-
from selenium import webdriver
from HTMLTestRunner import HTMLTestRunner
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from datetime import datetime, timedelta
import unittest, time, re, os, sys
import pyautogui
import gamevariable
#staging測試腳本

homeurl = 'http://example.internal/'
#staging網址

playerusername = '<ACCOUNT>'
#輸入帳號，只能大寫
playerpassword = '<REDACTED>'
#輸入密碼

#gamedomain = 'https://example.internal'
gamedomain = 'https://example.internal'
#輸入遊戲網址domain，換環境或測試CDN時會需要

#betrecordurl = 'https://example.internal'
betrecordurl = 'https://example.internal'
#輸入投注紀錄網址domain，換環境或測試CDN時會需要

brgametime = "//table[@id='__BVID__11']/tbody/tr/td[1]"
# betrecord game time 位置

brgamename = "//table[@id='__BVID__11']/tbody/tr/td[3]"
#betrecord game name 位置

brgametotalbet = "//table[@id='__BVID__11']/tbody/tr/td[4]/div"
#betrecord total bet 位置

brgamebuyfree = "//table[@id='__BVID__11']/tbody/tr/td[5]/div"
#betrecord buy free game 位置

#https://example.internal/api/<PRODUCT>/launch/2001/?data=<REDACTED>&urlToken=<REDACTED>
#開遊戲報API錯誤

def get_documenttime():
    documenttime = time.strftime("%Y-%m-%d-%H_%M_%S", time.localtime(time.time()))
    return documenttime
# 取得文件用的日期與時間，中間不能有空白，因為是檔名

def get_day():
    currentday = time.strftime("%Y-%m-%d", time.localtime(time.time()))
    return currentday
#取得今日日期

def get_time():
    currenttime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
    return currenttime
#取得今日時間

def print_day():
    print (get_day())
#印出今日日期

def print_time():
    print (get_time())
#印出今日時間

def get_gameoriginalurl(game_id):
    return "http://example.internal/id/<PRODUCT>/lobby/is_"+game_id
#跳轉前網址+遊戲ID


class test_newuat_old_test(unittest.TestCase):

    def setUp(self):
        # self.driver = webdriver.Chrome()
        options = webdriver.ChromeOptions()
        # options.add_argument('blink-settings=imagesEnabled=false') 
        options.add_argument("--incognito")
        options.add_argument('--no-sandbox')
        options.add_argument("--window-position=0,0")
        options.add_argument('--window-size=1024,768')
        # options.add_argument("--start-maximized")
        # options.add_argument('--disable-dev-shm-usage')
        # options.headless = True 

        # driverpath = "C:/selenium/test_case"
        # self.driver = webdriver.Firefox(driverpath)
        self.driver = webdriver.Chrome(options=options)
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
        self.driver.find_element_by_id("btnLogin").submit()
        time.sleep(3)

    def confirmloginfo(self):
        driver = self.driver
        try: 
            self.assertEqual(playerusername, driver.find_element_by_xpath("//li[@id='profile-menu']/a/span").text)
        except AssertionError as e: 
            self.verificationErrors.append(str(e))
        for i in range(60):
            try:
                if self.is_element_present(example.internal, "balance-holder"): 
                    print (playerusername + "登入成功")
                    break
            except: 
                pass
            time.sleep(3)
        else: 
            self.fail("time out")
            print ("驗證登錄資訊逾時")
    

    def get_gameurl(self,game_id):
        intgameid = int(game_id)
        
        e8slot = {1813,1815,1816,1818,1819,1822}
        
        if 1601 <= intgameid and 1607 >= intgameid :
            return gamedomain+"/16slot/?gameid="+game_id
        elif ( intgameid == 1700 ) or ( intgameid == 1701 ) :
            return gamedomain+"/17scratch/?gameid="+game_id
        elif ( intgameid == 1811 ) or ( intgameid == 1812 ) :
            return gamedomain+"/18scratch/?gameid="+game_id
        elif intgameid in e8slot :
            return gamedomain+"/18slot/?gameid="+game_id
        elif ( intgameid == 1817 ) or ( intgameid == 1820 ) :
            return gamedomain+"/18fruit/?gameid="+game_id
        elif 2000 <= intgameid and 2001 >= intgameid :
            return gamedomain+"/20fruit/?gameid="+game_id
        elif 1900 <= intgameid and 1908 >= intgameid :
            return gamedomain+"/19slot/?gameid="+game_id
        elif 2100 <= intgameid and 2103 >= intgameid :
            return gamedomain+"/21fruit/?gameid="+game_id
        elif 2200 <= intgameid and 2203 >= intgameid :
            return gamedomain+"/22slot/?gameid="+game_id
        elif 2300 <= intgameid and 2302 >= intgameid :
            return gamedomain+"/23slot/?gameid="+game_id
        elif 2400 <= intgameid and 2403 >= intgameid :
            return gamedomain+"/24slot/?gameid="+game_id
        elif 2500 <= intgameid and 2504 >= intgameid :
            return gamedomain+"/25grid/?gameid="+game_id
        elif 2600 <= intgameid and 2603 >= intgameid :
            return gamedomain+"/26slot/?gameid="+game_id
        elif 2700 <= intgameid and 2703 >= intgameid :
            return gamedomain+"/27slot/?gameid="+game_id
        elif 2800 <= intgameid and 2803 >= intgameid :
            return gamedomain+"/28fruit/?gameid="+game_id
        elif 2900 <= intgameid and 2902 >= intgameid :
            return gamedomain+"/29grid/?gameid="+game_id
        elif ( intgameid == 3000 ) or ( intgameid == 3001 ) :
            return gamedomain+"/30slot/?gameid="+game_id
        elif 3100 <= intgameid and 3102 >= intgameid :
            return gamedomain+"/31slot/?gameid="+game_id
        elif 3200 <= intgameid and 3202 >= intgameid :
            return gamedomain+"/32slot/?gameid="+game_id
        else :
            return None

    def calculatetimeerror(self):    
        driver = self.driver
        gametime = driver.find_element_by_xpath(brgametime).text
        print("當前時間為:"+ get_time())
        print("遊戲時間為:"+ gametime)
        nowgametime = datetime.strptime(str(gametime),"%Y-%m-%d %H:%M:%S")
        nowgettime = datetime.strptime(str(get_time()),"%Y-%m-%d %H:%M:%S")
        secondserror = (nowgettime - nowgametime).seconds
        if secondserror  < 15 :
            print("驗證遊戲時間小於15秒，通過")
        else :
            print("超出時間允許誤差值")

    def verified_gamelink(self,game_id):

        driver = self.driver
        currentPageUrl = driver.current_url
        #現在的網址命名變數

        gamelink = currentPageUrl.split('&token=')[0]
        #取token之前的網址

        gameexpecturl = self.get_gameurl(game_id)
        
        assert gamelink == gameexpecturl, "当前遊戲网址非预期！"
        #驗證網址是否正確

        return gamelink
    
    def get_token(self,game_id):
        
        driver = self.driver
        currentPageUrl = driver.current_url
        #現在的網址命名變數

        urltoken = currentPageUrl.split("&")[1]
        #取&token整串

        return urltoken
    
    def verified_br_gametime(self):
        driver = self.driver

        # 驗證betrecord game time
        for i in range(60):
            try:
                if self.is_element_present(By.XPATH, brgametime):
                    break
            except:
                pass
                self.driver.implicitly_wait(30)
            else:
                print ("等待驗證遊戲時間超時!!!!")
                self.fail("time out")
        try:
             # 驗證當前與投注時間誤差是否小餘 15 秒
             self.calculatetimeerror()  
        except AssertionError as e:
            self.verificationErrors.append(str(e))
            print ("錯誤 : 遊戲投注時間超時") 

    #betrecord gamename verified
    def verified_br_gamename(self,game_id,language):
        driver = self.driver
        get_brgamename = gamevariable.getgameinfo.get_gamename(game_id,language)

        #驗證betrecord game name
        for i in range(60):
            try:
                if self.is_element_present(By.XPATH, brgamename): 
                    break
            except: 
                pass
                self.driver.implicitly_wait(30)
            else: 
                self.fail("time out")
        try:
            gamename = driver.find_element_by_xpath(brgamename).text
            self.assertEqual(get_brgamename, gamename)
            print ("遊戲名稱驗證結束")
        except AssertionError as e: 
            self.verificationErrors.append(str(e))
    
    #betrecord totalbet verified
    def verified_br_totalbet(self,game_id):
        driver = self.driver
        get_brgametotalbet = gamevariable.getgameinfo.get_gametotalbet(game_id)

        for i in range(60):
            try:
                if self.is_element_present(By.XPATH, brgametotalbet): 
                    break
            except: 
                pass
                self.driver.implicitly_wait(30)
            else: 
                self.fail("time out")
        try: 
            self.assertEqual(get_brgametotalbet, driver.find_element_by_xpath(brgametotalbet).text)
            print ("投注金額驗證結束")
        except AssertionError as e: 
            self.verificationErrors.append(str(e))
    
    
    #betrecord language verfied

    def verified_br(self,token,game_id):

        driver = self.driver

        recordurl_id = betrecordurl+"/?"+ token +"&lang=id&serverurl=https%3A%2F%2Fexample.internal"
        recordurl_en = betrecordurl+"/?"+ token +"&lang=en&serverurl=https%3A%2F%2Fexample.internal"
        recordurl_ko = betrecordurl+"/?"+ token +"&lang=ko&serverurl=https%3A%2F%2Fexample.internal"
        recordurl_cn = betrecordurl+"/?"+ token +"&lang=zh-cn&serverurl=https%3A%2F%2Fexample.internal"
    
        driver.get(recordurl_id)
        print("前往印尼文投注記錄")
        driver.implicitly_wait(30)
        self.verified_br_gametime()
        self.verified_br_gamename(game_id,"id")
        self.verified_br_totalbet(game_id)
        print("印尼文驗證結束")
        driver.get(recordurl_en)
        print("前往英文投注記錄")
        driver.implicitly_wait(30)
        self.verified_br_gametime()
        self.verified_br_gamename(game_id,"en")
        self.verified_br_totalbet(game_id)
        print("英文驗證結束")
        driver.get(recordurl_ko)
        print("前往韓文投注記錄")
        driver.implicitly_wait(30)
        self.verified_br_gametime()
        self.verified_br_gamename(game_id,"ko")
        self.verified_br_totalbet(game_id)
        print("韓文驗證結束")
        driver.get(recordurl_cn)
        print("前往簡體中文投注記錄")
        driver.implicitly_wait(30)
        self.verified_br_gametime()
        self.verified_br_gamename(game_id,"cn")
        self.verified_br_totalbet(game_id)
        print("簡體中文驗證結束")

        #驗證投注記錄4個語系

    def test16slot(self):
        print_time()
        driver = self.driver
        #打開staging 商戶登陸頁面
        self.driver.get(homeurl)
        time.sleep(3)
        self.logininfo()
        self.confirmloginfo()

        #打開1601遊戲測試頁面
        self.driver.execute_script("window.open()")
        self.driver.switch_to.window(driver.window_handles[1])
        self.driver.get(get_gameoriginalurl('1601'))
        self.driver.implicitly_wait(30)
        time.sleep(3)
        
        #驗證遊戲網址
        self.verified_gamelink('1601')
        result = self.verified_gamelink('1601')
        print("打開網址是："+ result)    

        #取得token
        self.get_token('1601')
        tokena = self.get_token('1601')
        print(tokena)

        #self.driver.save_screenshot('./result/'+get_day()+'\\'+get_time()+'-1601-loading.png')
        time.sleep(5)
        #self.driver.save_screenshot('./result/'+get_day()+'\\'+get_time()+'-1601-gamepage.png')
        time.sleep(5)
        
        #進入畫布(遊戲頁面)
        canvas = driver.find_element_by_xpath("//canvas")       
        
        #spin
        gamevariable.getgameinfo.click_spin('spin21')

        #另開新視窗
        self.driver.execute_script("window.open()")
        self.driver.switch_to.window(driver.window_handles[2])

        #驗證1601是否投注成功
        self.verified_br(tokena,'1601')

        #打開1602遊戲測試頁面
        self.driver.switch_to.window(driver.window_handles[1])
        self.driver.get(get_gameoriginalurl('1602'))
        self.driver.implicitly_wait(30)
        time.sleep(3)
        
        #驗證遊戲網址
        self.verified_gamelink('1602')
        result = self.verified_gamelink('1602')
        print("打開網址是："+ result)

        #取得token
        self.get_token('1602')
        tokena = self.get_token('1602')
        print(tokena)

        #self.driver.save_screenshot('./result/'+get_day()+'\\'+get_time()+'-1602-loading.png')
        time.sleep(5)
        #self.driver.save_screenshot('./result/'+get_day()+'\\'+get_time()+'-1602-gamepage.png')
        time.sleep(5)
        
        #進入畫布(遊戲頁面)
        canvas = driver.find_element_by_xpath("//canvas")       
        
        #spin
        gamevariable.getgameinfo.click_spin('spin21')

        #切換到投注記錄
        self.driver.switch_to.window(driver.window_handles[2])

        #驗證1602是否投注成功
        self.verified_br(tokena,'1602')

        #打開1603遊戲測試頁面
        self.driver.switch_to.window(driver.window_handles[1])
        self.driver.get(get_gameoriginalurl('1603'))
        self.driver.implicitly_wait(30)
        time.sleep(3)
        
        #驗證遊戲網址
        self.verified_gamelink('1603')
        result = self.verified_gamelink('1603')
        print("打開網址是："+ result)

        #取得token
        self.get_token('1603')
        tokena = self.get_token('1603')
        print(tokena)

        #self.driver.save_screenshot('./result/'+get_day()+'\\'+get_time()+'-1603-loading.png')
        time.sleep(5)
        #self.driver.save_screenshot('./result/'+get_day()+'\\'+get_time()+'-1603-gamepage.png')
        time.sleep(5)
        
        #進入畫布(遊戲頁面)
        canvas = driver.find_element_by_xpath("//canvas")       
        
        #spin
        gamevariable.getgameinfo.click_spin('spin21')

        #切換到投注記錄
        self.driver.switch_to.window(driver.window_handles[2])

        #驗證1603是否投注成功
        self.verified_br(tokena,'1603')

        #打開1604遊戲測試頁面
        self.driver.switch_to.window(driver.window_handles[1])
        self.driver.get(get_gameoriginalurl('1604'))
        self.driver.implicitly_wait(30)
        time.sleep(3)
        
        #驗證遊戲網址
        self.verified_gamelink('1604')
        result = self.verified_gamelink('1604')
        print("打開網址是："+ result)

        #取得token
        self.get_token('1604')
        tokena = self.get_token('1604')
        print(tokena)

        #self.driver.save_screenshot('./result/'+get_day()+'\\'+get_time()+'-1604-loading.png')
        time.sleep(5)
        #self.driver.save_screenshot('./result/'+get_day()+'\\'+get_time()+'-1604-gamepage.png')
        time.sleep(5)
        
        #進入畫布(遊戲頁面)
        canvas = driver.find_element_by_xpath("//canvas")       
        
        #spin
        gamevariable.getgameinfo.click_spin('spin21')

        #切換到投注記錄
        self.driver.switch_to.window(driver.window_handles[2])

        #驗證1604是否投注成功
        self.verified_br(tokena,'1604')

        #打開1605遊戲測試頁面
        self.driver.switch_to.window(driver.window_handles[1])
        self.driver.get(get_gameoriginalurl('1605'))
        self.driver.implicitly_wait(30)
        time.sleep(3)
        
        #驗證遊戲網址
        self.verified_gamelink('1605')
        result = self.verified_gamelink('1605')
        print("打開網址是："+ result)

        #取得token
        self.get_token('1605')
        tokena = self.get_token('1605')
        print(tokena)

        #self.driver.save_screenshot('./result/'+get_day()+'\\'+get_time()+'-1605-loading.png')
        time.sleep(5)
        #self.driver.save_screenshot('./result/'+get_day()+'\\'+get_time()+'-1605-gamepage.png')
        time.sleep(5)
        
        #進入畫布(遊戲頁面)
        canvas = driver.find_element_by_xpath("//canvas")       
        
        #spin
        gamevariable.getgameinfo.click_spin('spin21')

        #切換到投注記錄
        self.driver.switch_to.window(driver.window_handles[2])

        #驗證1605是否投注成功
        self.verified_br(tokena,'1605')

        #打開1606遊戲測試頁面
        self.driver.switch_to.window(driver.window_handles[1])
        self.driver.get(get_gameoriginalurl('1606'))
        self.driver.implicitly_wait(30)
        time.sleep(3)
        
        #驗證遊戲網址
        self.verified_gamelink('1606')
        result = self.verified_gamelink('1606')
        print("打開網址是："+ result)

        #取得token
        self.get_token('1606')
        tokena = self.get_token('1606')
        print(tokena)

        #self.driver.save_screenshot('./result/'+get_day()+'\\'+get_time()+'-1606-loading.png')
        time.sleep(5)
        #self.driver.save_screenshot('./result/'+get_day()+'\\'+get_time()+'-1606-gamepage.png')
        time.sleep(5)
        
        #進入畫布(遊戲頁面)
        canvas = driver.find_element_by_xpath("//canvas")       
        
        #spin
        gamevariable.getgameinfo.click_spin('spin21')

        #切換到投注記錄
        self.driver.switch_to.window(driver.window_handles[2])

        #驗證1606是否投注成功
        self.verified_br(tokena,'1606')

        #打開1607遊戲測試頁面
        self.driver.switch_to.window(driver.window_handles[1])
        self.driver.get(get_gameoriginalurl('1607'))
        self.driver.implicitly_wait(30)
        time.sleep(3)
        
        #驗證遊戲網址
        self.verified_gamelink('1607')
        result = self.verified_gamelink('1607')
        print("打開網址是："+ result)

        #取得token
        self.get_token('1607')
        tokena = self.get_token('1607')
        print(tokena)

        #self.driver.save_screenshot('./result/'+get_day()+'\\'+get_time()+'-1607-loading.png')
        time.sleep(5)
        #self.driver.save_screenshot('./result/'+get_day()+'\\'+get_time()+'-1607-gamepage.png')
        time.sleep(5)
        
        #進入畫布(遊戲頁面)
        canvas = driver.find_element_by_xpath("//canvas")       
        
        #spin
        gamevariable.getgameinfo.click_spin('spin21')

        #切換到投注記錄
        self.driver.switch_to.window(driver.window_handles[2])

        #驗證1607是否投注成功
        self.verified_br(tokena,'1607')
    
    def testscratch(self):
        print_time()
        driver = self.driver
        #打開staging 商戶登陸頁面
        self.driver.get(homeurl)
        time.sleep(3)
        self.logininfo()
        self.confirmloginfo()

        #打開1700遊戲測試頁面
        self.driver.execute_script("window.open()")
        self.driver.switch_to.window(driver.window_handles[1])
        self.driver.get(get_gameoriginalurl('1700'))
        self.driver.implicitly_wait(30)
        time.sleep(3)
        
        #驗證遊戲網址
        self.verified_gamelink('1700')
        result = self.verified_gamelink('1700')
        print("打開網址是："+ result)

        #取得token
        self.get_token('1700')
        tokena = self.get_token('1700')
        print(tokena)

        #self.driver.save_screenshot('./result/'+get_day()+'\\'+get_time()+'-1700-loading.png')
        time.sleep(5)
        #self.driver.save_screenshot('./result/'+get_day()+'\\'+get_time()+'-1700-gamepage.png')
        time.sleep(5)
        
        #進入畫布(遊戲頁面)
        canvas = driver.find_element_by_xpath("//canvas")
        
        #開始遊戲
        gamevariable.getgameinfo.click_spin('spinlottery')

        #另開新視窗
        self.driver.execute_script("window.open()")
        self.driver.switch_to.window(driver.window_handles[2])

        #驗證1700是否投注成功
        self.verified_br(tokena,'1700')
    
        #打開1701遊戲測試頁面
        self.driver.switch_to.window(driver.window_handles[1])
        self.driver.get(get_gameoriginalurl('1701'))
        self.driver.implicitly_wait(30)
        time.sleep(3)
        
        #驗證遊戲網址
        self.verified_gamelink('1701')
        result = self.verified_gamelink('1701')
        print("打開網址是："+ result)

        #取得token
        self.get_token('1701')
        tokena = self.get_token('1701')
        print(tokena)

        #self.driver.save_screenshot('./result/'+get_day()+'\\'+get_time()+'-1701-loading.png')
        time.sleep(5)
        #self.driver.save_screenshot('./result/'+get_day()+'\\'+get_time()+'-1701-gamepage.png')
        time.sleep(5)
        
        #進入畫布(遊戲頁面)
        canvas = driver.find_element_by_xpath("//canvas")
        
        #開始遊戲
        gamevariable.getgameinfo.click_spin('spinlottery')

        #切換至投注記錄視窗
        self.driver.switch_to.window(driver.window_handles[2])

        #驗證1701是否投注成功
        self.verified_br(tokena,'1701')
    
        #打開1811遊戲測試頁面
        self.driver.switch_to.window(driver.window_handles[1])
        self.driver.get(get_gameoriginalurl('1811'))
        self.driver.implicitly_wait(30)
        time.sleep(3)
        
        #驗證遊戲網址
        self.verified_gamelink('1811')
        result = self.verified_gamelink('1811')
        print("打開網址是："+ result)

        #取得token
        self.get_token('1811')
        tokena = self.get_token('1811')
        print(tokena)

        #self.driver.save_screenshot('./result/'+get_day()+'\\'+get_time()+'-1811-loading.png')
        time.sleep(5)
        #self.driver.save_screenshot('./result/'+get_day()+'\\'+get_time()+'-1811-gamepage.png')
        time.sleep(5)
        
        #進入畫布(遊戲頁面)
        canvas = driver.find_element_by_xpath("//canvas")
        
        #開始遊戲
        gamevariable.getgameinfo.click_spin('spinlottery')

        #切換至投注記錄視窗
        self.driver.switch_to.window(driver.window_handles[2])

        #驗證1811是否投注成功
        self.verified_br(tokena,'1811')
    
    
        #打開1812遊戲測試頁面
        self.driver.switch_to.window(driver.window_handles[1])
        self.driver.get(get_gameoriginalurl('1812'))
        self.driver.implicitly_wait(30)
        time.sleep(3)
        
        #驗證遊戲網址
        self.verified_gamelink('1812')
        result = self.verified_gamelink('1812')
        print("打開網址是："+ result)

        #取得token
        self.get_token('1812')
        tokena = self.get_token('1812')
        print(tokena)

        #self.driver.save_screenshot('./result/'+get_day()+'\\'+get_time()+'-1812-loading.png')
        time.sleep(5)
        #self.driver.save_screenshot('./result/'+get_day()+'\\'+get_time()+'-1812-gamepage.png')
        time.sleep(5)
        
        #進入畫布(遊戲頁面)
        canvas = driver.find_element_by_xpath("//canvas")
        
        #開始遊戲
        gamevariable.getgameinfo.click_spin('spinlottery')

        #切換至投注記錄視窗
        self.driver.switch_to.window(driver.window_handles[2])

        #驗證1812是否投注成功
        self.verified_br(tokena,'1812')
    
    def testfruit(self):
        print_time()
        driver = self.driver
        #打開staging 商戶登陸頁面
        self.driver.get(homeurl)
        time.sleep(3)
        self.logininfo()
        self.confirmloginfo()

        #打開1817遊戲測試頁面
        self.driver.execute_script("window.open()")
        self.driver.switch_to.window(driver.window_handles[1])
        self.driver.get(get_gameoriginalurl('1817'))
        self.driver.implicitly_wait(30)
        time.sleep(3)
        
        #驗證遊戲網址
        self.verified_gamelink('1817')
        result = self.verified_gamelink('1817')
        print("打開網址是："+ result)    

        #取得token
        self.get_token('1817')
        tokena = self.get_token('1817')
        print(tokena)

        #self.driver.save_screenshot('./result/'+get_day()+'\\'+get_time()+'-1817-loading.png')
        time.sleep(5)
        #self.driver.save_screenshot('./result/'+get_day()+'\\'+get_time()+'-1817-gamepage.png')
        time.sleep(5)
        
        #進入畫布(遊戲頁面)
        canvas = driver.find_element_by_xpath("//canvas")    

        #spin
        gamevariable.getgameinfo.click_spin('spin21')

        #另開新視窗
        self.driver.execute_script("window.open()")
        self.driver.switch_to.window(driver.window_handles[2])

        #驗證1817是否投注成功
        self.verified_br(tokena,'1817')
    
        #打開1820遊戲測試頁面
        self.driver.switch_to.window(driver.window_handles[1])
        self.driver.get(get_gameoriginalurl('1820'))
        self.driver.implicitly_wait(30)
        time.sleep(3)
        
        #驗證遊戲網址
        self.verified_gamelink('1820')
        result = self.verified_gamelink('1820')
        print("打開網址是："+ result)

        #取得token
        self.get_token('1820')
        tokena = self.get_token('1820')
        print(tokena)

        #self.driver.save_screenshot('./result/'+get_day()+'\\'+get_time()+'-1820-loading.png')
        time.sleep(5)
        #self.driver.save_screenshot('./result/'+get_day()+'\\'+get_time()+'-1820-gamepage.png')
        time.sleep(5)
        
        #進入畫布(遊戲頁面)
        canvas = driver.find_element_by_xpath("//canvas")       
        
        #spin
        gamevariable.getgameinfo.click_spin('spin21')

        #切換至投注記錄視窗
        self.driver.switch_to.window(driver.window_handles[2])

        #驗證1820是否投注成功
        self.verified_br(tokena,'1820')
    
        #打開2000遊戲測試頁面
        self.driver.switch_to.window(driver.window_handles[1])
        self.driver.get(get_gameoriginalurl('2000'))
        self.driver.implicitly_wait(30)
        time.sleep(3)
        
        #驗證遊戲網址
        self.verified_gamelink('2000')
        result = self.verified_gamelink('2000')
        print("打開網址是："+ result)

        #取得token
        self.get_token('2000')
        tokena = self.get_token('2000')
        print(tokena)

        #self.driver.save_screenshot('./result/'+get_day()+'\\'+get_time()+'-2000-loading.png')
        time.sleep(5)
        #self.driver.save_screenshot('./result/'+get_day()+'\\'+get_time()+'-2000-gamepage.png')
        time.sleep(5)
        
        #進入畫布(遊戲頁面)
        canvas = driver.find_element_by_xpath("//canvas")       
        
        #spin
        gamevariable.getgameinfo.click_spin('spin21')

        #切換至投注記錄視窗
        self.driver.switch_to.window(driver.window_handles[2])

        #驗證2000是否投注成功
        self.verified_br(tokena,'2000')
    
        #打開2001遊戲測試頁面
        self.driver.switch_to.window(driver.window_handles[1])
        self.driver.get(get_gameoriginalurl('2001'))
        self.driver.implicitly_wait(30)
        time.sleep(3)
        
        #驗證遊戲網址
        self.verified_gamelink('2001')
        result = self.verified_gamelink('2001')
        print("打開網址是："+ result)

        #取得token
        self.get_token('2001')
        tokena = self.get_token('2001')
        print(tokena)

        #self.driver.save_screenshot('./result/'+get_day()+'\\'+get_time()+'-2001-loading.png')
        time.sleep(5)
        #self.driver.save_screenshot('./result/'+get_day()+'\\'+get_time()+'-2001-gamepage.png')
        time.sleep(5)
        
        #進入畫布(遊戲頁面)
        canvas = driver.find_element_by_xpath("//canvas")       
        
        #spin
        gamevariable.getgameinfo.click_spin('spin21')

        #切換至投注記錄視窗
        self.driver.switch_to.window(driver.window_handles[2])

        #驗證2001是否投注成功
        self.verified_br(tokena,'2001')
        
    def test18slot(self):
        print_time()
        driver = self.driver
        #打開staging 商戶登陸頁面
        self.driver.get(homeurl)
        time.sleep(3)
        self.logininfo()
        self.confirmloginfo()

        #打開1813遊戲測試頁面
        self.driver.execute_script("window.open()")
        self.driver.switch_to.window(driver.window_handles[1])
        self.driver.get(get_gameoriginalurl('1813'))
        self.driver.implicitly_wait(30)
        time.sleep(3)
        
        #驗證遊戲網址
        self.verified_gamelink('1813')
        result = self.verified_gamelink('1813')
        print("打開網址是："+ result)    

        #取得token
        self.get_token('1813')
        tokena = self.get_token('1813')
        print(tokena)

        #self.driver.save_screenshot('./result/'+get_day()+'\\'+get_time()+'-1813-loading.png')
        time.sleep(5)
        #self.driver.save_screenshot('./result/'+get_day()+'\\'+get_time()+'-1813-gamepage.png')
        time.sleep(5)
        
        #進入畫布(遊戲頁面)
        canvas = driver.find_element_by_xpath("//canvas")       
        
        #spin
        gamevariable.getgameinfo.click_spin('spin21')

        #另開新視窗
        self.driver.execute_script("window.open()")
        self.driver.switch_to.window(driver.window_handles[2])

        #驗證1813是否投注成功
        self.verified_br(tokena,'1813')

        #打開1815遊戲測試頁面
        self.driver.switch_to.window(driver.window_handles[1])
        self.driver.get(get_gameoriginalurl('1815'))
        self.driver.implicitly_wait(30)
        time.sleep(3)
        
        #驗證遊戲網址
        self.verified_gamelink('1815')
        result = self.verified_gamelink('1815')
        print("打開網址是："+ result)

        #取得token
        self.get_token('1815')
        tokena = self.get_token('1815')
        print(tokena)

        #self.driver.save_screenshot('./result/'+get_day()+'\\'+get_time()+'-1815-loading.png')
        time.sleep(5)
        #self.driver.save_screenshot('./result/'+get_day()+'\\'+get_time()+'-1815-gamepage.png')
        time.sleep(5)
        
        #進入畫布(遊戲頁面)
        canvas = driver.find_element_by_xpath("//canvas")       
        
        #spin
        gamevariable.getgameinfo.click_spin('spin21')

        #切換到投注記錄
        self.driver.switch_to.window(driver.window_handles[2])

        #驗證1815是否投注成功
        self.verified_br(tokena,'1815')

   
        #打開1816遊戲測試頁面
        self.driver.switch_to.window(driver.window_handles[1])
        self.driver.get(get_gameoriginalurl('1816'))
        self.driver.implicitly_wait(30)
        time.sleep(3)
        
        #驗證遊戲網址
        self.verified_gamelink('1816')
        result = self.verified_gamelink('1816')
        print("打開網址是："+ result)

        #取得token
        self.get_token('1816')
        tokena = self.get_token('1816')
        print(tokena)

        #self.driver.save_screenshot('./result/'+get_day()+'\\'+get_time()+'-1816-loading.png')
        time.sleep(5)
        #self.driver.save_screenshot('./result/'+get_day()+'\\'+get_time()+'-1816-gamepage.png')
        time.sleep(5)
        
        #進入畫布(遊戲頁面)
        canvas = driver.find_element_by_xpath("//canvas")       
        
        #spin
        gamevariable.getgameinfo.click_spin('spin21')

        #切換到投注記錄
        self.driver.switch_to.window(driver.window_handles[2])

        #驗證1816是否投注成功
        self.verified_br(tokena,'1816')

    
        #打開1818遊戲測試頁面
        self.driver.switch_to.window(driver.window_handles[1])
        self.driver.get(get_gameoriginalurl('1818'))
        self.driver.implicitly_wait(30)
        time.sleep(3)
        
        #驗證遊戲網址
        self.verified_gamelink('1818')
        result = self.verified_gamelink('1818')
        print("打開網址是："+ result)

        #取得token
        self.get_token('1818')
        tokena = self.get_token('1818')
        print(tokena)

        #self.driver.save_screenshot('./result/'+get_day()+'\\'+get_time()+'-1818-loading.png')
        time.sleep(5)
        #self.driver.save_screenshot('./result/'+get_day()+'\\'+get_time()+'-1818-gamepage.png')
        time.sleep(5)
        
        #進入畫布(遊戲頁面)
        canvas = driver.find_element_by_xpath("//canvas")       
        
        #spin
        gamevariable.getgameinfo.click_spin('spin21')

        #切換到投注記錄
        self.driver.switch_to.window(driver.window_handles[2])

        #驗證1818是否投注成功
        self.verified_br(tokena,'1818')

        #打開1819遊戲測試頁面
        self.driver.switch_to.window(driver.window_handles[1])
        self.driver.get(get_gameoriginalurl('1819'))
        self.driver.implicitly_wait(30)
        time.sleep(3)
        
        #驗證遊戲網址
        self.verified_gamelink('1819')
        result = self.verified_gamelink('1819')
        print("打開網址是："+ result)

        #取得token
        self.get_token('1819')
        tokena = self.get_token('1819')
        print(tokena)

        #self.driver.save_screenshot('./result/'+get_day()+'\\'+get_time()+'-1819-loading.png')
        time.sleep(5)
        #self.driver.save_screenshot('./result/'+get_day()+'\\'+get_time()+'-1819-gamepage.png')
        time.sleep(5)
        
        #進入畫布(遊戲頁面)
        canvas = driver.find_element_by_xpath("//canvas")       
        
        #spin
        gamevariable.getgameinfo.click_spin('spin21')

        #切換到投注記錄
        self.driver.switch_to.window(driver.window_handles[2])

        #驗證1819是否投注成功
        self.verified_br(tokena,'1819')

        #打開1822遊戲測試頁面
        self.driver.switch_to.window(driver.window_handles[1])
        self.driver.get(get_gameoriginalurl('1822'))
        self.driver.implicitly_wait(30)
        time.sleep(3)
        
        #驗證遊戲網址
        self.verified_gamelink('1822')
        result = self.verified_gamelink('1822')
        print("打開網址是："+ result)

        #取得token
        self.get_token('1822')
        tokena = self.get_token('1822')
        print(tokena)

        #self.driver.save_screenshot('./result/'+get_day()+'\\'+get_time()+'-1822-loading.png')
        time.sleep(5)
        #self.driver.save_screenshot('./result/'+get_day()+'\\'+get_time()+'-1822-gamepage.png')
        time.sleep(5)
        
        #進入畫布(遊戲頁面)
        canvas = driver.find_element_by_xpath("//canvas")       
        
        #spin
        gamevariable.getgameinfo.click_spin('spin21')

        #切換到投注記錄
        self.driver.switch_to.window(driver.window_handles[2])

        #驗證1822是否投注成功
        self.verified_br(tokena,'1822')
    
    def test19slot(self):
        print_time()
        driver = self.driver
        #打開staging 商戶登陸頁面
        self.driver.get(homeurl)
        time.sleep(3)
        self.logininfo()
        self.confirmloginfo()

        #打開1900遊戲測試頁面
        self.driver.execute_script("window.open()")
        self.driver.switch_to.window(driver.window_handles[1])
        self.driver.get(get_gameoriginalurl('1900'))
        self.driver.implicitly_wait(30)
        time.sleep(3)
        
        #驗證遊戲網址
        self.verified_gamelink('1900')
        result = self.verified_gamelink('1900')
        print("打開網址是："+ result)    

        #取得token
        self.get_token('1900')
        tokena = self.get_token('1900')
        print(tokena)

        #self.driver.save_screenshot('./result/'+get_day()+'\\'+get_time()+'-1900-loading.png')
        time.sleep(5)
        #self.driver.save_screenshot('./result/'+get_day()+'\\'+get_time()+'-1900-gamepage.png')
        time.sleep(5)
        
        #進入畫布(遊戲頁面)
        canvas = driver.find_element_by_xpath("//canvas")       
        
        #spin
        gamevariable.getgameinfo.click_spin('spin21')

        #另開新視窗
        self.driver.execute_script("window.open()")
        self.driver.switch_to.window(driver.window_handles[2])

        #驗證1900是否投注成功
        self.verified_br(tokena,'1900')
    
 
        #打開1901遊戲測試頁面
        self.driver.switch_to.window(driver.window_handles[1])
        self.driver.get(get_gameoriginalurl('1901'))
        self.driver.implicitly_wait(30)
        time.sleep(3)
        
        #驗證遊戲網址
        self.verified_gamelink('1901')
        result = self.verified_gamelink('1901')
        print("打開網址是："+ result)

        #取得token
        self.get_token('1901')
        tokena = self.get_token('1901')
        print(tokena)

        #self.driver.save_screenshot('./result/'+get_day()+'\\'+get_time()+'-1901-loading.png')
        time.sleep(5)
        #self.driver.save_screenshot('./result/'+get_day()+'\\'+get_time()+'-1901-gamepage.png')
        time.sleep(5)
        
        #進入畫布(遊戲頁面)
        canvas = driver.find_element_by_xpath("//canvas")       
        
        #spin
        gamevariable.getgameinfo.click_spin('spin21')

        #切換到投注記錄
        self.driver.switch_to.window(driver.window_handles[2])

        #驗證1901是否投注成功
        self.verified_br(tokena,'1901')

    
        #打開1902遊戲測試頁面
        self.driver.switch_to.window(driver.window_handles[1])
        self.driver.get(get_gameoriginalurl('1902'))
        self.driver.implicitly_wait(30)
        time.sleep(3)
        
        #驗證遊戲網址
        self.verified_gamelink('1902')
        result = self.verified_gamelink('1902')
        print("打開網址是："+ result)

        #取得token
        self.get_token('1902')
        tokena = self.get_token('1902')
        print(tokena)

        #self.driver.save_screenshot('./result/'+get_day()+'\\'+get_time()+'-1902-loading.png')
        time.sleep(5)
        #self.driver.save_screenshot('./result/'+get_day()+'\\'+get_time()+'-1902-gamepage.png')
        time.sleep(5)
        
        #進入畫布(遊戲頁面)
        canvas = driver.find_element_by_xpath("//canvas")       
        
        #spin
        gamevariable.getgameinfo.click_spin('spin21')

        #切換到投注記錄
        self.driver.switch_to.window(driver.window_handles[2])

        #驗證1902是否投注成功
        self.verified_br(tokena,'1902')

        #打開1903遊戲測試頁面
        self.driver.switch_to.window(driver.window_handles[1])
        self.driver.get(get_gameoriginalurl('1903'))
        self.driver.implicitly_wait(30)
        time.sleep(3)
        
        #驗證遊戲網址
        self.verified_gamelink('1903')
        result = self.verified_gamelink('1903')
        print("打開網址是："+ result)

        #取得token
        self.get_token('1903')
        tokena = self.get_token('1903')
        print(tokena)

        #self.driver.save_screenshot('./result/'+get_day()+'\\'+get_time()+'-1903-loading.png')
        time.sleep(5)
        #self.driver.save_screenshot('./result/'+get_day()+'\\'+get_time()+'-1903-gamepage.png')
        time.sleep(5)
        
        #進入畫布(遊戲頁面)
        canvas = driver.find_element_by_xpath("//canvas")       
        
        #spin
        gamevariable.getgameinfo.click_spin('spin21')

        #切換到投注記錄
        self.driver.switch_to.window(driver.window_handles[2])

        #驗證1903是否投注成功
        self.verified_br(tokena,'1903')

    
        #打開1904遊戲測試頁面
        self.driver.switch_to.window(driver.window_handles[1])
        self.driver.get(get_gameoriginalurl('1904'))
        self.driver.implicitly_wait(30)
        time.sleep(3)
        
        #驗證遊戲網址
        self.verified_gamelink('1904')
        result = self.verified_gamelink('1904')
        print("打開網址是："+ result)

        #取得token
        self.get_token('1904')
        tokena = self.get_token('1904')
        print(tokena)

        #self.driver.save_screenshot('./result/'+get_day()+'\\'+get_time()+'-1904-loading.png')
        time.sleep(5)
        #self.driver.save_screenshot('./result/'+get_day()+'\\'+get_time()+'-1904-gamepage.png')
        time.sleep(5)
        
        #進入畫布(遊戲頁面)
        canvas = driver.find_element_by_xpath("//canvas")       
        
        #spin
        gamevariable.getgameinfo.click_spin('spin21')

        #切換到投注記錄
        self.driver.switch_to.window(driver.window_handles[2])

        #驗證1904是否投注成功
        self.verified_br(tokena,'1904')

    
        #打開1905遊戲測試頁面
        self.driver.switch_to.window(driver.window_handles[1])
        self.driver.get(get_gameoriginalurl('1905'))
        self.driver.implicitly_wait(30)
        time.sleep(3)
        
        #驗證遊戲網址
        self.verified_gamelink('1905')
        result = self.verified_gamelink('1905')
        print("打開網址是："+ result)

        #取得token
        self.get_token('1905')
        tokena = self.get_token('1905')
        print(tokena)

        #self.driver.save_screenshot('./result/'+get_day()+'\\'+get_time()+'-1905-loading.png')
        time.sleep(5)
        #self.driver.save_screenshot('./result/'+get_day()+'\\'+get_time()+'-1905-gamepage.png')
        time.sleep(5)
        
        #進入畫布(遊戲頁面)
        canvas = driver.find_element_by_xpath("//canvas")       
        
        #spin
        gamevariable.getgameinfo.click_spin('spin21')

        #切換到投注記錄
        self.driver.switch_to.window(driver.window_handles[2])

        #驗證1905是否投注成功
        self.verified_br(tokena,'1905')

        #打開1906遊戲測試頁面
        self.driver.switch_to.window(driver.window_handles[1])
        self.driver.get(get_gameoriginalurl('1906'))
        self.driver.implicitly_wait(30)
        time.sleep(3)
        
        #驗證遊戲網址
        self.verified_gamelink('1906')
        result = self.verified_gamelink('1906')
        print("打開網址是："+ result)

        #取得token
        self.get_token('1906')
        tokena = self.get_token('1906')
        print(tokena)

        #self.driver.save_screenshot('./result/'+get_day()+'\\'+get_time()+'-1906-loading.png')
        time.sleep(5)
        #self.driver.save_screenshot('./result/'+get_day()+'\\'+get_time()+'-1906-gamepage.png')
        time.sleep(5)
        
        #進入畫布(遊戲頁面)
        canvas = driver.find_element_by_xpath("//canvas")       
        
        #spin
        gamevariable.getgameinfo.click_spin('spin21')

        #切換到投注記錄
        self.driver.switch_to.window(driver.window_handles[2])

        #驗證1906是否投注成功
        self.verified_br(tokena,'1906')

    
        #打開1907遊戲測試頁面
        self.driver.switch_to.window(driver.window_handles[1])
        self.driver.get(get_gameoriginalurl('1907'))
        self.driver.implicitly_wait(30)
        time.sleep(3)
        
        #驗證遊戲網址
        self.verified_gamelink('1907')
        result = self.verified_gamelink('1907')
        print("打開網址是："+ result)

        #取得token
        self.get_token('1907')
        tokena = self.get_token('1907')
        print(tokena)

        #self.driver.save_screenshot('./result/'+get_day()+'\\'+get_time()+'-1907-loading.png')
        time.sleep(5)
        #self.driver.save_screenshot('./result/'+get_day()+'\\'+get_time()+'-1907-gamepage.png')
        time.sleep(5)
        
        #進入畫布(遊戲頁面)
        canvas = driver.find_element_by_xpath("//canvas")       
        
        #spin
        gamevariable.getgameinfo.click_spin('spin21')

        #切換到投注記錄
        self.driver.switch_to.window(driver.window_handles[2])

        #驗證1907是否投注成功
        self.verified_br(tokena,'1907')

        #打開1908遊戲測試頁面
        self.driver.switch_to.window(driver.window_handles[1])
        self.driver.get(get_gameoriginalurl('1908'))
        self.driver.implicitly_wait(30)
        time.sleep(3)
        
        #驗證遊戲網址
        self.verified_gamelink('1908')
        result = self.verified_gamelink('1908')
        print("打開網址是："+ result)

        #取得token
        self.get_token('1908')
        tokena = self.get_token('1908')
        print(tokena)

        #self.driver.save_screenshot('./result/'+get_day()+'\\'+get_time()+'-1908-loading.png')
        time.sleep(5)
        #self.driver.save_screenshot('./result/'+get_day()+'\\'+get_time()+'-1908-gamepage.png')
        time.sleep(5)
        
        #進入畫布(遊戲頁面)
        canvas = driver.find_element_by_xpath("//canvas")       
        
        #spin
        gamevariable.getgameinfo.click_spin('spin21')

        #切換到投注記錄
        self.driver.switch_to.window(driver.window_handles[2])

        #驗證1908是否投注成功
        self.verified_br(tokena,'1908')


    def located_element(self, locator):
        wait = WebDriverWait(self.driver,30)
        element = wait.until(EC.presence_of_element_located((locator)))
        return element

    def is_element_present(self, how, what):
        try: 
            self.driver.find_element(by=how, value=what)
        except NoSuchElementException as e: 
            return False
        return True
    
    def is_alert_present(self):
        try: 
            self.driver.switch_to_alert()
        except NoAlertPresentException as e: 
            return False
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

    
    # def click_locxy(driver, x, y, left_click=True):    
    # # driver:browser
    # # x:页面x坐标
    # # y:页面y坐标
    # # left_click:True为鼠标左键点击，否则为右键点击
    #     if left_click:
    #         ActionChains(driver).move_by_offset(x, y).click().perform()
    #     else:
    #         ActionChains(driver).move_by_offset(x, y).context_click().perform()
    #     ActionChains(driver).move_by_offset(-x, -y).perform() # 将鼠标位置恢复到移动前
    def getClippedImage(driver, canvas, x, y, w, h):
    ### Get a clipped image from canvas using context.getImageData.
        data = driver.execute_script(
            "var canvas= arguments[0];  var x=arguments[1];  var y=arguments[2]; var w=arguments[3];  var h=arguments[4];  var context = canvas.getContext(‘2d‘);  var dataObj= context.getImageData(x, y, w, h);  var data = dataObj.data; return data;"
            ,canvas, x, y, w, h) 
        data_bytes = array.array('B', data).tostring()
        im = Image.fromstring("RGBA", (w, h), data_bytes)
        return im

    def tearDown(self):
        #關閉瀏覽器
        self.driver.quit()
        #關閉驗證文字
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
    unittest.addTest(test_newuat_old_test("test16slot"))
    unittest.addTest(test_newuat_old_test("testscratch"))
    unittest.addTest(test_newuat_old_test("testfruit"))
    unittest.addTest(test_newuat_old_test("test18slot"))
    unittest.addTest(test_newuat_old_test("test19slot"))

    #将测试结果写入到result.html中
    fp=open(get_documenttime()+"-new staging result.html",'wb')
    runner=HTMLTestRunner(stream=fp,title='UAT old game Test Report',description='Result:',tester='jay')
    runner.run(unittest)
    fp.close()