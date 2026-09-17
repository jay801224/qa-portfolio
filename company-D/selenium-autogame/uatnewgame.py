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
import unittest, time, re, os, sys
import pyautogui
import gamevariable

#staging測試腳本

playerusername = '<ACCOUNT>'
#輸入帳號，只能大寫
playerpassword = '<REDACTED>'
#輸入密碼

homeurl = 'http://example.internal/'

#gamedomain = 'https://example.internal'
gamedomain = 'https://example.internal'
#輸入遊戲網址domain，換環境或測試CDN時會需要

#betrecordurl = 'https://example.internal'
betrecordurl = 'https://example.internal'
#輸入投注紀錄網址domain，換環境或測試CDN時會需要

serverurl = 'example.internal'

brgamename = "//table[@id='__BVID__11']/tbody/tr/td[3]"
#betrecord game name 位置

brgametotalbet = "//table[@id='__BVID__11']/tbody/tr/td[4]/div"
#betrecord total bet 位置

brgamebuyfree = "//table[@id='__BVID__11']/tbody/tr/td[5]/div"
#betrecord buy free game 位置

#https://example.internal/api/<PRODUCT>/launch/2001/?data=<REDACTED>&urlToken=<REDACTED>
#開遊戲報API錯誤

def get_day():
    currentday = time.strftime("%Y-%m-%d", time.localtime(time.time()))
    return currentday
#取得今日日期

def get_time():
    currenttime = time.strftime("%Y-%m-%d-%H_%M_%S", time.localtime(time.time()))
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


class test_newuat_new_test(unittest.TestCase):
    def setUp(self):
        # self.driver = webdriver.Chrome()
        options = webdriver.ChromeOptions()
        # options.add_argument('blink-settings=imagesEnabled=false') 
        options.add_argument("--incognito")
        options.add_argument('--no-sandbox')
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
        elif 2100 <= intgameid and 2104 >= intgameid :
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
        elif 2800 <= intgameid and 2804 >= intgameid :
            return gamedomain+"/28fruit/?gameid="+game_id
        elif 2900 <= intgameid and 2902 >= intgameid :
            return gamedomain+"/29grid/?gameid="+game_id
        elif ( intgameid == 3000 ) or ( intgameid == 3001 ) or ( intgameid == 3002 ):
            return gamedomain+"/30slot/?gameid="+game_id
        elif 3100 <= intgameid and 3102 >= intgameid :
            return gamedomain+"/31slot/?gameid="+game_id
        elif 3200 <= intgameid and 3202 >= intgameid :
            return gamedomain+"/32slot/?gameid="+game_id
        else :
            return None

    def verified_gamelink(self,game_id):

        driver = self.driver
        currentPageUrl = driver.current_url
        #現在的網址命名變數

        gamelink = currentPageUrl.split('&token=')[0]
        #取token之前的網址

        gameexpecturl = self.get_gameurl(game_id)

        if gamelink == gameexpecturl :
            return gamelink
        else :
            print ("當前網址是:"+ gamelink)
        
        assert gamelink == gameexpecturl, "当前遊戲网址非预期！"
        #驗證網址是否正確
        

    
    def get_token(self,game_id):
        
        driver = self.driver
        currentPageUrl = driver.current_url
        #現在的網址命名變數

        urltoken = currentPageUrl.split("&")[1]
        #取&token整串

        return urltoken

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
                print ("驗證遊戲名稱超時!!!!")
                self.fail("time out")
                
        try:
            gamename = driver.find_element_by_xpath(brgamename).text
            self.assertEqual(get_brgamename, gamename)
            print("遊戲名稱驗證結束")
        except AssertionError as e:
            self.verificationErrors.append(str(e))
            print ("錯誤 : 驗證遊戲名稱")
    
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
                print ("驗證遊戲投注金額超時!!!!")
                self.fail("time out")
        try:
            gametotalbet = driver.find_element_by_xpath(brgametotalbet).text
            self.assertEqual( get_brgametotalbet, gametotalbet )
            print("投注金額驗證結束")
        except AssertionError as e:
            print ("錯誤 : 驗證遊戲投注金額")
            self.verificationErrors.append(str(e))
    
    #betrecord buy free game verified
    def verified_br_buyfreegame(self,game_id):
        driver = self.driver
        get_brbuyfree = gamevariable.getgameinfo.get_gamebuyfree(game_id)

        for i in range(60):
            try:
                if self.is_element_present(By.XPATH, brgamebuyfree): 
                    break
            except: 
                pass
                self.driver.implicitly_wait(30)
            else:
                print ("購買免費遊戲金額驗證超時!!!!")
                self.fail("time out")
        try:
            gamebuyfreetotalbet = driver.find_element_by_xpath(brgamebuyfree).text
            self.assertEqual( get_brbuyfree, gamebuyfreetotalbet )
            print("購買免費遊戲驗證結束")
        except AssertionError as e:
            print ("錯誤 : 購買免費遊戲金額驗證")
            self.verificationErrors.append(str(e))
    
    #betrecord language verfied
    def verified_br(self,token,game_id):

        driver = self.driver

        recordurl_id = betrecordurl+"/?"+ token +"&lang=id&serverurl=https%3A%2F%2F"+serverurl
        recordurl_en = betrecordurl+"/?"+ token +"&lang=en&serverurl=https%3A%2F%2F"+serverurl
        recordurl_ko = betrecordurl+"/?"+ token +"&lang=ko&serverurl=https%3A%2F%2F"+serverurl
        recordurl_cn = betrecordurl+"/?"+ token +"&lang=zh-cn&serverurl=https%3A%2F%2F"+serverurl
    
        driver.get(recordurl_id)
        print("前往印尼文投注記錄")
        driver.implicitly_wait(30)
        self.verified_br_gamename(game_id,"id")
        self.verified_br_totalbet(game_id)
        print("印尼文驗證結束")
        driver.get(recordurl_en)
        print("前往英文投注記錄")
        driver.implicitly_wait(30)
        self.verified_br_gamename(game_id,"en")
        self.verified_br_totalbet(game_id)
        print("英文驗證結束")
        driver.get(recordurl_ko)
        print("前往韓文投注記錄")
        driver.implicitly_wait(30)
        self.verified_br_gamename(game_id,"ko")
        self.verified_br_totalbet(game_id)
        print("韓文驗證結束")
        driver.get(recordurl_cn)
        print("前往簡體中文投注記錄")
        driver.implicitly_wait(30)
        self.verified_br_gamename(game_id,"cn")
        self.verified_br_totalbet(game_id)
        print("簡體中文驗證結束")

        #驗證投注記錄4個語系
    
    def test21fruit(self):
        print_time()
        driver = self.driver
        #打開staging 商戶登陸頁面
        self.driver.get(homeurl)
        time.sleep(3)
        self.logininfo()
        self.confirmloginfo()

        #打開2100遊戲測試頁面
        self.driver.execute_script("window.open()")
        self.driver.switch_to.window(driver.window_handles[1])
        self.driver.get(get_gameoriginalurl('2100'))
        self.driver.implicitly_wait(30)
        time.sleep(3)
        
        #驗證遊戲網址
        self.verified_gamelink('2100')
        result = self.verified_gamelink('2100')
        print("打開網址是："+ result)    

        #取得token
        self.get_token('2100')
        tokena = self.get_token('2100')
        print(tokena)

        #self.driver.save_screenshot('./result/'+get_day()+'\\'+get_time()+'-2100-loading.png')
        time.sleep(5)
        #self.driver.save_screenshot('./result/'+get_day()+'\\'+get_time()+'-2100-gamepage.png')
        time.sleep(5)
        
        #進入畫布(遊戲頁面)
        canvas = driver.find_element_by_xpath("//canvas")       
        
        #spin
        gamevariable.getgameinfo.click_spin('spin21')

        #另開新視窗
        self.driver.execute_script("window.open()")
        self.driver.switch_to.window(driver.window_handles[2])

        #驗證2100是否投注成功
        self.verified_br(tokena,'2100')
    
        #打開2101遊戲測試頁面
        self.driver.switch_to.window(driver.window_handles[1])
        self.driver.get(get_gameoriginalurl('2101'))
        self.driver.implicitly_wait(30)
        time.sleep(3)
        
        #驗證遊戲網址
        self.verified_gamelink('2101')
        result = self.verified_gamelink('2101')
        print("打開網址是："+ result)

        #取得token
        self.get_token('2101')
        tokena = self.get_token('2101')
        print(tokena)

        #self.driver.save_screenshot('./result/'+get_day()+'\\'+get_time()+'-2101-loading.png')
        time.sleep(5)
        #self.driver.save_screenshot('./result/'+get_day()+'\\'+get_time()+'-2101-gamepage.png')
        time.sleep(5)
        
        #進入畫布(遊戲頁面)
        canvas = driver.find_element_by_xpath("//canvas")       
        
        #spin
        gamevariable.getgameinfo.click_spin('spin21')

        #切換到投注記錄
        self.driver.switch_to.window(driver.window_handles[2])

        #驗證2101是否投注成功
        self.verified_br(tokena,'2101')
    
    
        #打開2102遊戲測試頁面
        self.driver.switch_to.window(driver.window_handles[1])
        self.driver.get(get_gameoriginalurl('2102'))
        self.driver.implicitly_wait(30)
        time.sleep(3)
        
        #驗證遊戲網址
        self.verified_gamelink('2102')
        result = self.verified_gamelink('2102')
        print("打開網址是："+ result)

        #取得token
        self.get_token('2102')
        tokena = self.get_token('2102')
        print(tokena)

        #self.driver.save_screenshot('./result/'+get_day()+'\\'+get_time()+'-2102-loading.png')
        time.sleep(5)
        #self.driver.save_screenshot('./result/'+get_day()+'\\'+get_time()+'-2102-gamepage.png')
        time.sleep(5)
        
        #進入畫布(遊戲頁面)
        canvas = driver.find_element_by_xpath("//canvas")       
        
        #spin
        gamevariable.getgameinfo.click_spin('spin21')

        #切換到投注記錄
        self.driver.switch_to.window(driver.window_handles[2])

        #驗證2102是否投注成功
        self.verified_br(tokena,'2102')

        #打開2103遊戲測試頁面
        self.driver.switch_to.window(driver.window_handles[1])
        self.driver.get(get_gameoriginalurl('2103'))
        self.driver.implicitly_wait(30)
        time.sleep(3)
        
        #驗證遊戲網址
        self.verified_gamelink('2103')
        result = self.verified_gamelink('2103')
        print("打開網址是："+ result)

        #取得token
        self.get_token('2103')
        tokena = self.get_token('2103')
        print(tokena)

        #self.driver.save_screenshot('./result/'+get_day()+'\\'+get_time()+'-2103-loading.png')
        time.sleep(5)
        #self.driver.save_screenshot('./result/'+get_day()+'\\'+get_time()+'-2103-gamepage.png')
        time.sleep(5)
        
        #進入畫布(遊戲頁面)
        canvas = driver.find_element_by_xpath("//canvas")       
        
        #spin
        gamevariable.getgameinfo.click_spin('spin21')

        #切換到投注記錄
        self.driver.switch_to.window(driver.window_handles[2])

        #驗證2103是否投注成功
        self.verified_br(tokena,'2103')
    
        #打開2104遊戲測試頁面
        self.driver.switch_to.window(driver.window_handles[1])
        self.driver.get(get_gameoriginalurl('2104'))
        self.driver.implicitly_wait(30)
        time.sleep(3)
        
        #驗證遊戲網址
        self.verified_gamelink('2104')
        result = self.verified_gamelink('2104')
        print("打開網址是："+ result)

        #取得token
        self.get_token('2104')
        tokena = self.get_token('2104')
        print(tokena)

        #self.driver.save_screenshot('./result/'+get_day()+'\\'+get_time()+'-2104-loading.png')
        time.sleep(5)
        #self.driver.save_screenshot('./result/'+get_day()+'\\'+get_time()+'-2104-gamepage.png')
        time.sleep(5)
        
        #進入畫布(遊戲頁面)
        canvas = driver.find_element_by_xpath("//canvas")       
        
        #spin
        gamevariable.getgameinfo.click_spin('spin21')

        #切換到投注記錄
        self.driver.switch_to.window(driver.window_handles[2])

        #驗證2104是否投注成功
        self.verified_br(tokena,'2104')

    def test22slot(self):
        print_time()
        driver = self.driver
        #打開staging 商戶登陸頁面
        self.driver.get(homeurl)
        time.sleep(3)
        self.logininfo()
        self.confirmloginfo()

        #打開2200遊戲測試頁面
        self.driver.execute_script("window.open()")
        self.driver.switch_to.window(driver.window_handles[1])
        self.driver.get(get_gameoriginalurl('2200'))
        self.driver.implicitly_wait(30)
        time.sleep(3)
        
        #驗證遊戲網址
        self.verified_gamelink('2200')
        result = self.verified_gamelink('2200')
        print("打開網址是："+ result)    

        #取得token
        self.get_token('2200')
        tokena = self.get_token('2200')
        print(tokena)

        #self.driver.save_screenshot('./result/'+get_day()+'\\'+get_time()+'-2200-loading.png')
        time.sleep(5)
        #self.driver.save_screenshot('./result/'+get_day()+'\\'+get_time()+'-2200-gamepage.png')
        time.sleep(5)
        
        #進入畫布(遊戲頁面)
        canvas = driver.find_element_by_xpath("//canvas")       
        
        #spin
        gamevariable.getgameinfo.click_spin('spin24')

        #另開新視窗
        self.driver.execute_script("window.open()")
        self.driver.switch_to.window(driver.window_handles[2])

        #驗證2200是否投注成功
        self.verified_br(tokena,'2200')

        #打開2201遊戲測試頁面
        self.driver.switch_to.window(driver.window_handles[1])
        self.driver.get(get_gameoriginalurl('2201'))
        self.driver.implicitly_wait(30)
        time.sleep(3)
        
        #驗證遊戲網址
        self.verified_gamelink('2201')
        result = self.verified_gamelink('2201')
        print("打開網址是："+ result)

        #取得token
        self.get_token('2201')
        tokena = self.get_token('2201')
        print(tokena)

        #self.driver.save_screenshot('./result/'+get_day()+'\\'+get_time()+'-2201-loading.png')
        time.sleep(5)
        #self.driver.save_screenshot('./result/'+get_day()+'\\'+get_time()+'-2201-gamepage.png')
        time.sleep(5)
        
        #進入畫布(遊戲頁面)
        canvas = driver.find_element_by_xpath("//canvas")       
        
        #spin
        gamevariable.getgameinfo.click_spin('spin24')

        #切換到投注記錄
        self.driver.switch_to.window(driver.window_handles[2])

        #驗證2201是否投注成功
        self.verified_br(tokena,'2201')
    
    
        #打開2202遊戲測試頁面
        self.driver.switch_to.window(driver.window_handles[1])
        self.driver.get(get_gameoriginalurl('2202'))
        self.driver.implicitly_wait(30)
        time.sleep(3)
        
        #驗證遊戲網址
        self.verified_gamelink('2202')
        result = self.verified_gamelink('2202')
        print("打開網址是："+ result)

        #取得token
        self.get_token('2202')
        tokena = self.get_token('2202')
        print(tokena)

        #self.driver.save_screenshot('./result/'+get_day()+'\\'+get_time()+'-2202-loading.png')
        time.sleep(5)
        #self.driver.save_screenshot('./result/'+get_day()+'\\'+get_time()+'-2202-gamepage.png')
        time.sleep(5)
        
        #進入畫布(遊戲頁面)
        canvas = driver.find_element_by_xpath("//canvas")       
        
        #spin
        gamevariable.getgameinfo.click_spin('spin24')

        #切換到投注記錄
        self.driver.switch_to.window(driver.window_handles[2])

        #驗證2202是否投注成功
        self.verified_br(tokena,'2202')
    
        #打開2203遊戲測試頁面
        self.driver.switch_to.window(driver.window_handles[1])
        self.driver.get(get_gameoriginalurl('2203'))
        self.driver.implicitly_wait(30)
        time.sleep(3)
        
        #驗證遊戲網址
        self.verified_gamelink('2203')
        result = self.verified_gamelink('2203')
        print("打開網址是："+ result)

        #取得token
        self.get_token('2203')
        tokena = self.get_token('2203')
        print(tokena)

        #self.driver.save_screenshot('./result/'+get_day()+'\\'+get_time()+'-2203-loading.png')
        time.sleep(5)
        #self.driver.save_screenshot('./result/'+get_day()+'\\'+get_time()+'-2203-gamepage.png')
        time.sleep(5)
        
        #進入畫布(遊戲頁面)
        canvas = driver.find_element_by_xpath("//canvas")       
        
        #spin
        gamevariable.getgameinfo.click_spin('spin24')

        #切換到投注記錄
        self.driver.switch_to.window(driver.window_handles[2])

        #驗證2203是否投注成功
        self.verified_br(tokena,'2203')

    def test23slot(self):
        print_time()
        driver = self.driver
        #打開staging 商戶登陸頁面
        self.driver.get(homeurl)
        time.sleep(3)
        self.logininfo()
        self.confirmloginfo()

        #打開2300遊戲測試頁面
        self.driver.execute_script("window.open()")
        self.driver.switch_to.window(driver.window_handles[1])
        self.driver.get(get_gameoriginalurl('2300'))
        self.driver.implicitly_wait(30)
        time.sleep(3)
        
        #驗證遊戲網址
        self.verified_gamelink('2300')
        result = self.verified_gamelink('2300')
        print("打開網址是："+ result)    

        #取得token
        self.get_token('2300')
        tokena = self.get_token('2300')
        print(tokena)

        #self.driver.save_screenshot('./result/'+get_day()+'\\'+get_time()+'-2300-loading.png')
        time.sleep(5)
        #self.driver.save_screenshot('./result/'+get_day()+'\\'+get_time()+'-2300-gamepage.png')
        time.sleep(5)
        
        #進入畫布(遊戲頁面)
        canvas = driver.find_element_by_xpath("//canvas")       
        
        #spin
        gamevariable.getgameinfo.click_spin('spin24')

        #另開新視窗
        self.driver.execute_script("window.open()")
        self.driver.switch_to.window(driver.window_handles[2])

        #驗證2300是否投注成功
        self.verified_br(tokena,'2300')
    
        #打開2301遊戲測試頁面
        self.driver.switch_to.window(driver.window_handles[1])
        self.driver.get(get_gameoriginalurl('2301'))
        self.driver.implicitly_wait(30)
        time.sleep(3)
        
        #驗證遊戲網址
        self.verified_gamelink('2301')
        result = self.verified_gamelink('2301')
        print("打開網址是："+ result)

        #取得token
        self.get_token('2301')
        tokena = self.get_token('2301')
        print(tokena)

        #self.driver.save_screenshot('./result/'+get_day()+'\\'+get_time()+'-2301-loading.png')
        time.sleep(5)
        #self.driver.save_screenshot('./result/'+get_day()+'\\'+get_time()+'-2301-gamepage.png')
        time.sleep(5)
        
        #進入畫布(遊戲頁面)
        canvas = driver.find_element_by_xpath("//canvas")       
        
        #spin
        gamevariable.getgameinfo.click_spin('spin24')

        #切換到投注記錄
        self.driver.switch_to.window(driver.window_handles[2])

        #驗證2301是否投注成功
        self.verified_br(tokena,'2301')
    
    
        #打開2302遊戲測試頁面
        self.driver.switch_to.window(driver.window_handles[1])
        self.driver.get(get_gameoriginalurl('2302'))
        self.driver.implicitly_wait(30)
        time.sleep(3)
        
        #驗證遊戲網址
        self.verified_gamelink('2302')
        result = self.verified_gamelink('2302')
        print("打開網址是："+ result)

        #取得token
        self.get_token('2302')
        tokena = self.get_token('2302')
        print(tokena)

        #self.driver.save_screenshot('./result/'+get_day()+'\\'+get_time()+'-2302-loading.png')
        time.sleep(5)
        #self.driver.save_screenshot('./result/'+get_day()+'\\'+get_time()+'-2302-gamepage.png')
        time.sleep(5)
        
        #進入畫布(遊戲頁面)
        canvas = driver.find_element_by_xpath("//canvas")       
        
        #spin
        gamevariable.getgameinfo.click_spin('spin24')

        #切換到投注記錄
        self.driver.switch_to.window(driver.window_handles[2])

        #驗證2302是否投注成功
        self.verified_br(tokena,'2302')
    
    def test24slot(self):
        print_time()
        driver = self.driver
        #打開staging 商戶登陸頁面
        self.driver.get(homeurl)
        time.sleep(3)
        self.logininfo()
        self.confirmloginfo()

        #打開2400遊戲測試頁面
        self.driver.execute_script("window.open()")
        self.driver.switch_to.window(driver.window_handles[1])
        self.driver.get(get_gameoriginalurl('2400'))
        self.driver.implicitly_wait(30)
        time.sleep(3)
        
        #驗證2400遊戲網址
        self.verified_gamelink('2400')
        result = self.verified_gamelink('2400')
        print("打開網址是："+ result)    

        #取得token
        self.get_token('2400')
        tokena = self.get_token('2400')
        print(tokena)

        #self.driver.save_screenshot('./result/'+get_day()+'\\'+get_time()+'-2400-loading.png')
        time.sleep(5)
        #self.driver.save_screenshot('./result/'+get_day()+'\\'+get_time()+'-2400-gamepage.png')
        time.sleep(5)
        
        #進入畫布(遊戲頁面)
        canvas = driver.find_element_by_xpath("//canvas")       
        
        #spin
        gamevariable.getgameinfo.click_spin('spin24')

        #另開新視窗
        self.driver.execute_script("window.open()")
        self.driver.switch_to.window(driver.window_handles[2])

        #驗證2400是否投注成功
        self.verified_br(tokena,'2400')

        #重載2400頁面
        self.driver.switch_to.window(driver.window_handles[1])
        self.driver.get(get_gameoriginalurl('2400'))
        self.driver.implicitly_wait(30)
        time.sleep(3)
        time.sleep(5)
        time.sleep(5)
        
        #進入畫布(遊戲頁面)
        canvas = driver.find_element_by_xpath("//canvas")       
        
        #buy free game
        gamevariable.getgameinfo.click_buyfree('buy24')

        #切換投注記錄視窗
        self.driver.switch_to.window(driver.window_handles[2])

        #驗證2400 buy free game是否成功
        self.verified_br(tokena,'2400')
        time.sleep(2)
        self.verified_br_buyfreegame('2400')

        #打開2401遊戲測試頁面
        self.driver.switch_to.window(driver.window_handles[1])
        self.driver.get(get_gameoriginalurl('2401'))
        self.driver.implicitly_wait(30)
        time.sleep(3)
        
        #驗證2401遊戲網址
        self.verified_gamelink('2401')
        result = self.verified_gamelink('2401')
        print("打開網址是："+ result)

        #取得token
        self.get_token('2401')
        tokena = self.get_token('2401')
        print(tokena)

        #self.driver.save_screenshot('./result/'+get_day()+'\\'+get_time()+'-2401-loading.png')
        time.sleep(5)
        #self.driver.save_screenshot('./result/'+get_day()+'\\'+get_time()+'-2401-gamepage.png')
        time.sleep(5)
        
        #進入畫布(遊戲頁面)
        canvas = driver.find_element_by_xpath("//canvas")       
        
        #spin
        gamevariable.getgameinfo.click_spin('spin24')

        #切換到投注記錄
        self.driver.switch_to.window(driver.window_handles[2])

        #驗證2401是否投注成功
        self.verified_br(tokena,'2401')
        
        #重載2401頁面
        self.driver.switch_to.window(driver.window_handles[1])
        self.driver.get(get_gameoriginalurl('2401'))
        self.driver.implicitly_wait(30)
        time.sleep(3)
        time.sleep(5)
        time.sleep(5)
        
        #進入畫布(遊戲頁面)
        canvas = driver.find_element_by_xpath("//canvas")       
        
        #buy free game
        gamevariable.getgameinfo.click_buyfree('buy24')

        #切換投注記錄視窗
        self.driver.switch_to.window(driver.window_handles[2])

        #驗證2401 buy free game是否成功
        self.verified_br(tokena,'2401')
        time.sleep(2)
        self.verified_br_buyfreegame('2401')

        #打開2402遊戲測試頁面
        self.driver.switch_to.window(driver.window_handles[1])
        self.driver.get(get_gameoriginalurl('2402'))
        self.driver.implicitly_wait(30)
        time.sleep(3)
        
        #驗證2402遊戲網址
        self.verified_gamelink('2402')
        result = self.verified_gamelink('2402')
        print("打開網址是："+ result)

        #取得token
        self.get_token('2402')
        tokena = self.get_token('2402')
        print(tokena)

        #self.driver.save_screenshot('./result/'+get_day()+'\\'+get_time()+'-2402-loading.png')
        time.sleep(5)
        #self.driver.save_screenshot('./result/'+get_day()+'\\'+get_time()+'-2402-gamepage.png')
        time.sleep(5)
        
        #進入畫布(遊戲頁面)
        canvas = driver.find_element_by_xpath("//canvas")       
        
        #spin
        gamevariable.getgameinfo.click_spin('spin24')

        #切換到投注記錄
        self.driver.switch_to.window(driver.window_handles[2])

        #驗證2402是否投注成功
        self.verified_br(tokena,'2402')
        
        #重載2402頁面
        self.driver.switch_to.window(driver.window_handles[1])
        self.driver.get(get_gameoriginalurl('2402'))
        self.driver.implicitly_wait(30)
        time.sleep(3)
        time.sleep(5)
        time.sleep(5)
        
        #進入畫布(遊戲頁面)
        canvas = driver.find_element_by_xpath("//canvas")       
        
        #buy free game
        gamevariable.getgameinfo.click_buyfree('buy24')

        #切換投注記錄視窗
        self.driver.switch_to.window(driver.window_handles[2])

        #驗證2402 buy free game是否成功
        self.verified_br(tokena,'2402')
        time.sleep(2)
        self.verified_br_buyfreegame('2402')

        #打開2403遊戲測試頁面
        self.driver.switch_to.window(driver.window_handles[1])
        self.driver.get(get_gameoriginalurl('2403'))
        self.driver.implicitly_wait(30)
        time.sleep(3)
        
        #驗證2403遊戲網址
        self.verified_gamelink('2403')
        result = self.verified_gamelink('2403')
        print("打開網址是："+ result)

        #取得token
        self.get_token('2403')
        tokena = self.get_token('2403')
        print(tokena)

        #self.driver.save_screenshot('./result/'+get_day()+'\\'+get_time()+'-2403-loading.png')
        time.sleep(5)
        #self.driver.save_screenshot('./result/'+get_day()+'\\'+get_time()+'-2403-gamepage.png')
        time.sleep(5)
        
        #進入畫布(遊戲頁面)
        canvas = driver.find_element_by_xpath("//canvas")       
        
        #spin
        gamevariable.getgameinfo.click_spin('spin24')

        #切換到投注記錄
        self.driver.switch_to.window(driver.window_handles[2])

        #驗證2403是否投注成功
        self.verified_br(tokena,'2403')

        #重載2403頁面
        self.driver.switch_to.window(driver.window_handles[1])
        self.driver.get(get_gameoriginalurl('2403'))
        self.driver.implicitly_wait(30)
        time.sleep(3)
        time.sleep(5)
        time.sleep(5)
        
        #進入畫布(遊戲頁面)
        canvas = driver.find_element_by_xpath("//canvas")       
        
        #buy free game
        gamevariable.getgameinfo.click_buyfree('buy24')

        #切換投注記錄視窗
        self.driver.switch_to.window(driver.window_handles[2])

        #驗證2403 buy free game是否成功
        self.verified_br(tokena,'2403')
        time.sleep(2)
        self.verified_br_buyfreegame('2403')

    def test25grid(self):
        print_time()
        driver = self.driver
        #打開staging 商戶登陸頁面
        self.driver.get(homeurl)
        time.sleep(3)
        self.logininfo()
        self.confirmloginfo()

        #打開2500遊戲測試頁面
        self.driver.execute_script("window.open()")
        self.driver.switch_to.window(driver.window_handles[1])
        self.driver.get(get_gameoriginalurl('2500'))
        self.driver.implicitly_wait(30)
        time.sleep(3)
        
        #驗證2500遊戲網址
        self.verified_gamelink('2500')
        result = self.verified_gamelink('2500')
        print("打開網址是："+ result)    

        #取得token
        self.get_token('2500')
        tokena = self.get_token('2500')
        print(tokena)

        #self.driver.save_screenshot('./result/'+get_day()+'\\'+get_time()+'-2500-loading.png')
        time.sleep(5)
        #self.driver.save_screenshot('./result/'+get_day()+'\\'+get_time()+'-2500-gamepage.png')
        time.sleep(5)
        
        #進入畫布(遊戲頁面)
        canvas = driver.find_element_by_xpath("//canvas")       
        
        #spin
        gamevariable.getgameinfo.click_spin('spin24')

        #另開新視窗
        self.driver.execute_script("window.open()")
        self.driver.switch_to.window(driver.window_handles[2])

        #驗證2500是否投注成功
        self.verified_br(tokena,'2500')

        #打開2501遊戲測試頁面
        self.driver.switch_to.window(driver.window_handles[1])
        self.driver.get(get_gameoriginalurl('2501'))
        self.driver.implicitly_wait(30)
        time.sleep(3)
        
        #驗證2501遊戲網址
        self.verified_gamelink('2501')
        result = self.verified_gamelink('2501')
        print("打開網址是："+ result)

        #取得token
        self.get_token('2501')
        tokena = self.get_token('2501')
        print(tokena)

        #self.driver.save_screenshot('./result/'+get_day()+'\\'+get_time()+'-2501-loading.png')
        time.sleep(5)
        #self.driver.save_screenshot('./result/'+get_day()+'\\'+get_time()+'-2501-gamepage.png')
        time.sleep(5)
        
        #進入畫布(遊戲頁面)
        canvas = driver.find_element_by_xpath("//canvas")       
        
        #spin
        gamevariable.getgameinfo.click_spin('spin24')

        #切換到投注記錄
        self.driver.switch_to.window(driver.window_handles[2])

        #驗證2501是否投注成功
        self.verified_br(tokena,'2501')

        #打開2502遊戲測試頁面
        self.driver.switch_to.window(driver.window_handles[1])
        self.driver.get(get_gameoriginalurl('2502'))
        self.driver.implicitly_wait(30)
        time.sleep(3)
        
        #驗證2502遊戲網址
        self.verified_gamelink('2502')
        result = self.verified_gamelink('2502')
        print("打開網址是："+ result)

        #取得token
        self.get_token('2502')
        tokena = self.get_token('2502')
        print(tokena)

        #self.driver.save_screenshot('./result/'+get_day()+'\\'+get_time()+'-2502-loading.png')
        time.sleep(5)
        #self.driver.save_screenshot('./result/'+get_day()+'\\'+get_time()+'-2502-gamepage.png')
        time.sleep(5)
        
        #進入畫布(遊戲頁面)
        canvas = driver.find_element_by_xpath("//canvas")       
        
        #spin
        gamevariable.getgameinfo.click_spin('spin24')

        #切換到投注記錄
        self.driver.switch_to.window(driver.window_handles[2])

        #驗證2502是否投注成功
        self.verified_br(tokena,'2502')

        #打開2503遊戲測試頁面
        self.driver.switch_to.window(driver.window_handles[1])
        self.driver.get(get_gameoriginalurl('2503'))
        self.driver.implicitly_wait(30)
        time.sleep(3)
        
        #驗證2503遊戲網址
        self.verified_gamelink('2503')
        result = self.verified_gamelink('2503')
        print("打開網址是："+ result)

        #取得token
        self.get_token('2503')
        tokena = self.get_token('2503')
        print(tokena)

        #self.driver.save_screenshot('./result/'+get_day()+'\\'+get_time()+'-2503-loading.png')
        time.sleep(5)
        #self.driver.save_screenshot('./result/'+get_day()+'\\'+get_time()+'-2503-gamepage.png')
        time.sleep(5)
        
        #進入畫布(遊戲頁面)
        canvas = driver.find_element_by_xpath("//canvas")       
        
        #spin
        gamevariable.getgameinfo.click_spin('spin24')

        #切換到投注記錄
        self.driver.switch_to.window(driver.window_handles[2])

        #驗證2503是否投注成功
        self.verified_br(tokena,'2503')

        #打開2501遊戲測試頁面
        self.driver.switch_to.window(driver.window_handles[1])
        self.driver.get(get_gameoriginalurl('2504'))
        self.driver.implicitly_wait(30)
        time.sleep(3)
        
        #驗證2504遊戲網址
        self.verified_gamelink('2504')
        result = self.verified_gamelink('2504')
        print("打開網址是："+ result)

        #取得token
        self.get_token('2504')
        tokena = self.get_token('2504')
        print(tokena)

        #self.driver.save_screenshot('./result/'+get_day()+'\\'+get_time()+'-2504-loading.png')
        time.sleep(5)
        #self.driver.save_screenshot('./result/'+get_day()+'\\'+get_time()+'-2504-gamepage.png')
        time.sleep(5)
        
        #進入畫布(遊戲頁面)
        canvas = driver.find_element_by_xpath("//canvas")       
        
        #spin
        gamevariable.getgameinfo.click_spin('spin24')

        #切換到投注記錄
        self.driver.switch_to.window(driver.window_handles[2])

        #驗證2504是否投注成功
        self.verified_br(tokena,'2504')

    def test26slot(self):
        print_time()
        driver = self.driver
        #打開staging 商戶登陸頁面
        self.driver.get(homeurl)
        time.sleep(3)
        self.logininfo()
        self.confirmloginfo()

        #打開2600遊戲測試頁面
        self.driver.execute_script("window.open()")
        self.driver.switch_to.window(driver.window_handles[1])
        self.driver.get(get_gameoriginalurl('2600'))
        self.driver.implicitly_wait(30)
        time.sleep(3)
        
        #驗證2600遊戲網址
        self.verified_gamelink('2600')
        result = self.verified_gamelink('2600')
        print("打開網址是："+ result)    

        #取得token
        self.get_token('2600')
        tokena = self.get_token('2600')
        print(tokena)

        #self.driver.save_screenshot('./result/'+get_day()+'\\'+get_time()+'-2600-loading.png')
        time.sleep(5)
        #self.driver.save_screenshot('./result/'+get_day()+'\\'+get_time()+'-2600-gamepage.png')
        time.sleep(5)
        
        #進入畫布(遊戲頁面)
        canvas = driver.find_element_by_xpath("//canvas")       
        
        #spin
        gamevariable.getgameinfo.click_spin('spin24')

        #另開新視窗
        self.driver.execute_script("window.open()")
        self.driver.switch_to.window(driver.window_handles[2])

        #驗證2600是否投注成功
        self.verified_br(tokena,'2600')
        
        #重載2600頁面
        self.driver.switch_to.window(driver.window_handles[1])
        self.driver.get(get_gameoriginalurl('2600'))
        self.driver.implicitly_wait(30)
        time.sleep(3)
        time.sleep(5)
        time.sleep(5)
        
        #進入畫布(遊戲頁面)
        canvas = driver.find_element_by_xpath("//canvas")       
        
        #buy free game
        gamevariable.getgameinfo.click_buyfree('buy27')

        #切換投注記錄視窗
        self.driver.switch_to.window(driver.window_handles[2])

        #驗證2600 buy free game是否成功
        self.verified_br(tokena,'2600')
        time.sleep(2)
        self.verified_br_buyfreegame('2600')

        #打開2601遊戲測試頁面
        self.driver.switch_to.window(driver.window_handles[1])
        self.driver.get(get_gameoriginalurl('2601'))
        self.driver.implicitly_wait(30)
        time.sleep(3)
        
        #驗證2601遊戲網址
        self.verified_gamelink('2601')
        result = self.verified_gamelink('2601')
        print("打開網址是："+ result)    

        #取得token
        self.get_token('2601')
        tokena = self.get_token('2601')
        print(tokena)

        #self.driver.save_screenshot('./result/'+get_day()+'\\'+get_time()+'-2601-loading.png')
        time.sleep(5)
        #self.driver.save_screenshot('./result/'+get_day()+'\\'+get_time()+'-2601-gamepage.png')
        time.sleep(5)
        
        #進入畫布(遊戲頁面)
        canvas = driver.find_element_by_xpath("//canvas")       
        
        #spin
        gamevariable.getgameinfo.click_spin('spin24')

        #另開新視窗
        self.driver.switch_to.window(driver.window_handles[2])

        #驗證2601是否投注成功
        self.verified_br(tokena,'2601')
        
        #重載2601頁面
        self.driver.switch_to.window(driver.window_handles[1])
        self.driver.get(get_gameoriginalurl('2601'))
        self.driver.implicitly_wait(30)
        time.sleep(3)
        time.sleep(5)
        time.sleep(5)
        
        #進入畫布(遊戲頁面)
        canvas = driver.find_element_by_xpath("//canvas")       
        
        #buy free game
        gamevariable.getgameinfo.click_buyfree('buy27')

        #切換投注記錄視窗
        self.driver.switch_to.window(driver.window_handles[2])

        #驗證2601 buy free game是否成功
        self.verified_br(tokena,'2601')
        time.sleep(2)
        self.verified_br_buyfreegame('2601')

        #打開2602遊戲測試頁面
        self.driver.switch_to.window(driver.window_handles[1])
        self.driver.get(get_gameoriginalurl('2602'))
        self.driver.implicitly_wait(30)
        time.sleep(3)
        
        #驗證2602遊戲網址
        self.verified_gamelink('2602')
        result = self.verified_gamelink('2602')
        print("打開網址是："+ result)    

        #取得token
        self.get_token('2602')
        tokena = self.get_token('2602')
        print(tokena)

        #self.driver.save_screenshot('./result/'+get_day()+'\\'+get_time()+'-2602-loading.png')
        time.sleep(5)
        #self.driver.save_screenshot('./result/'+get_day()+'\\'+get_time()+'-2602-gamepage.png')
        time.sleep(5)
        
        #進入畫布(遊戲頁面)
        canvas = driver.find_element_by_xpath("//canvas")       
        
        #spin
        gamevariable.getgameinfo.click_spin('spin24')

        #切換視窗
        self.driver.switch_to.window(driver.window_handles[2])

        #驗證2602是否投注成功
        self.verified_br(tokena,'2602')
        
        #重載2602頁面
        self.driver.switch_to.window(driver.window_handles[1])
        self.driver.get(get_gameoriginalurl('2602'))
        self.driver.implicitly_wait(30)
        time.sleep(3)
        time.sleep(5)
        time.sleep(5)
        
        #進入畫布(遊戲頁面)
        canvas = driver.find_element_by_xpath("//canvas")       
        
        #buy free game
        gamevariable.getgameinfo.click_buyfree('buy27')

        #切換投注記錄視窗
        self.driver.switch_to.window(driver.window_handles[2])

        #驗證2602 buy free game是否成功
        self.verified_br(tokena,'2602')
        time.sleep(2)
        self.verified_br_buyfreegame('2602')

        #打開2603遊戲測試頁面
        self.driver.switch_to.window(driver.window_handles[1])
        self.driver.get(get_gameoriginalurl('2603'))
        self.driver.implicitly_wait(30)
        time.sleep(3)
        
        #驗證2603遊戲網址
        self.verified_gamelink('2603')
        result = self.verified_gamelink('2603')
        print("打開網址是："+ result)    

        #取得token
        self.get_token('2603')
        tokena = self.get_token('2603')
        print(tokena)

        #self.driver.save_screenshot('./result/'+get_day()+'\\'+get_time()+'-2603-loading.png')
        time.sleep(5)
        #self.driver.save_screenshot('./result/'+get_day()+'\\'+get_time()+'-2603-gamepage.png')
        time.sleep(5)
        
        #進入畫布(遊戲頁面)
        canvas = driver.find_element_by_xpath("//canvas")       
        
        #spin
        gamevariable.getgameinfo.click_spin('spin24')

        #切換視窗
        self.driver.switch_to.window(driver.window_handles[2])

        #驗證2603是否投注成功
        self.verified_br(tokena,'2603')
        
        #重載2603頁面
        self.driver.switch_to.window(driver.window_handles[1])
        self.driver.get(get_gameoriginalurl('2603'))
        self.driver.implicitly_wait(30)
        time.sleep(3)
        time.sleep(5)
        time.sleep(5)
        
        #進入畫布(遊戲頁面)
        canvas = driver.find_element_by_xpath("//canvas")       
        
        #buy free game
        gamevariable.getgameinfo.click_buyfree('buy27')

        #切換投注記錄視窗
        self.driver.switch_to.window(driver.window_handles[2])

        #驗證2603 buy free game是否成功
        self.verified_br(tokena,'2603')
        time.sleep(2)
        self.verified_br_buyfreegame('2603')
    
    def test27slot(self):
        print_time()
        driver = self.driver
        #打開staging 商戶登陸頁面
        self.driver.get(homeurl)
        time.sleep(3)
        self.logininfo()
        self.confirmloginfo()

        #打開2700遊戲測試頁面
        self.driver.execute_script("window.open()")
        self.driver.switch_to.window(driver.window_handles[1])
        self.driver.get(get_gameoriginalurl('2700'))
        self.driver.implicitly_wait(30)
        time.sleep(3)
        
        #驗證遊戲網址
        self.verified_gamelink('2700')
        result = self.verified_gamelink('2700')
        print("打開網址是："+ result)    

        #取得token
        self.get_token('2700')
        tokena = self.get_token('2700')
        print(tokena)

        #self.driver.save_screenshot('./result/'+get_day()+'\\'+get_time()+'-2700-loading.png')
        time.sleep(5)
        #self.driver.save_screenshot('./result/'+get_day()+'\\'+get_time()+'-2700-gamepage.png')
        time.sleep(5)
        
        #進入畫布(遊戲頁面)
        canvas = driver.find_element_by_xpath("//canvas")       
        
        #spin
        gamevariable.getgameinfo.click_spin('spin24')

        #另開新視窗
        self.driver.execute_script("window.open()")
        self.driver.switch_to.window(driver.window_handles[2])

        #驗證2700是否投注成功
        self.verified_br(tokena,'2700')

        #重載2700頁面
        self.driver.switch_to.window(driver.window_handles[1])
        self.driver.get(get_gameoriginalurl('2700'))
        self.driver.implicitly_wait(30)
        time.sleep(3)
        time.sleep(5)
        time.sleep(5)
        
        #進入畫布(遊戲頁面)
        canvas = driver.find_element_by_xpath("//canvas")       
        
        #buy free game
        gamevariable.getgameinfo.click_buyfree('buy27')

        #切換投注記錄視窗
        self.driver.switch_to.window(driver.window_handles[2])

        #驗證2700 buy free game是否成功
        self.verified_br(tokena,'2700')
        time.sleep(2)
        self.verified_br_buyfreegame('2700')

        #打開2701遊戲測試頁面
        self.driver.switch_to.window(driver.window_handles[1])
        self.driver.get(get_gameoriginalurl('2701'))
        self.driver.implicitly_wait(30)
        time.sleep(3)
        
        #驗證遊戲網址
        self.verified_gamelink('2701')
        result = self.verified_gamelink('2701')
        print("打開網址是："+ result)    

        #取得token
        self.get_token('2701')
        tokena = self.get_token('2701')
        print(tokena)

        #self.driver.save_screenshot('./result/'+get_day()+'\\'+get_time()+'-2701-loading.png')
        time.sleep(5)
        #self.driver.save_screenshot('./result/'+get_day()+'\\'+get_time()+'-2701-gamepage.png')
        time.sleep(5)
        
        #進入畫布(遊戲頁面)
        canvas = driver.find_element_by_xpath("//canvas")       
        
        #spin
        gamevariable.getgameinfo.click_spin('spin24')

        #另開新視窗
        self.driver.switch_to.window(driver.window_handles[2])

        #驗證2701是否投注成功
        self.verified_br(tokena,'2701')

        #重載2701頁面
        self.driver.switch_to.window(driver.window_handles[1])
        self.driver.get(get_gameoriginalurl('2701'))
        self.driver.implicitly_wait(30)
        time.sleep(3)
        time.sleep(5)
        time.sleep(5)
        
        #進入畫布(遊戲頁面)
        canvas = driver.find_element_by_xpath("//canvas")       
        
        #buy free game
        gamevariable.getgameinfo.click_buyfree('buy27')

        #切換投注記錄視窗
        self.driver.switch_to.window(driver.window_handles[2])

        #驗證2701 buy free game是否成功
        self.verified_br(tokena,'2701')
        time.sleep(2)
        self.verified_br_buyfreegame('2701')

        #打開2702遊戲測試頁面
        self.driver.switch_to.window(driver.window_handles[1])
        self.driver.get(get_gameoriginalurl('2702'))
        self.driver.implicitly_wait(30)
        time.sleep(3)
        
        #驗證遊戲網址
        self.verified_gamelink('2702')
        result = self.verified_gamelink('2702')
        print("打開網址是："+ result)    

        #取得token
        self.get_token('2702')
        tokena = self.get_token('2702')
        print(tokena)

        #self.driver.save_screenshot('./result/'+get_day()+'\\'+get_time()+'-2702-loading.png')
        time.sleep(5)
        #self.driver.save_screenshot('./result/'+get_day()+'\\'+get_time()+'-2702-gamepage.png')
        time.sleep(5)
        
        #進入畫布(遊戲頁面)
        canvas = driver.find_element_by_xpath("//canvas")       
        
        #spin
        gamevariable.getgameinfo.click_spin('spin24')

        #另開新視窗
        self.driver.execute_script("window.open()")
        self.driver.switch_to.window(driver.window_handles[2])

        #驗證2702是否投注成功
        self.verified_br(tokena,'2702')

        #重載2702頁面
        self.driver.switch_to.window(driver.window_handles[1])
        self.driver.get(get_gameoriginalurl('2702'))
        self.driver.implicitly_wait(30)
        time.sleep(3)
        time.sleep(5)
        time.sleep(5)
        
        #進入畫布(遊戲頁面)
        canvas = driver.find_element_by_xpath("//canvas")       
        
        #buy free game
        gamevariable.getgameinfo.click_buyfree('buy27')

        #切換投注記錄視窗
        self.driver.switch_to.window(driver.window_handles[2])

        #驗證2702 buy free game是否成功
        self.verified_br(tokena,'2702')
        time.sleep(2)
        self.verified_br_buyfreegame('2702')

        #打開2703遊戲測試頁面
        self.driver.switch_to.window(driver.window_handles[1])
        self.driver.get(get_gameoriginalurl('2703'))
        self.driver.implicitly_wait(30)
        time.sleep(3)
        
        #驗證遊戲網址
        self.verified_gamelink('2703')
        result = self.verified_gamelink('2703')
        print("打開網址是："+ result)    

        #取得token
        self.get_token('2703')
        tokena = self.get_token('2703')
        print(tokena)

        #self.driver.save_screenshot('./result/'+get_day()+'\\'+get_time()+'-2703-loading.png')
        time.sleep(5)
        #self.driver.save_screenshot('./result/'+get_day()+'\\'+get_time()+'-2703-gamepage.png')
        time.sleep(5)
        
        #進入畫布(遊戲頁面)
        canvas = driver.find_element_by_xpath("//canvas")       
        
        #spin
        gamevariable.getgameinfo.click_spin('spin24')

        #切換新視窗
        self.driver.switch_to.window(driver.window_handles[2])

        #驗證2703是否投注成功
        self.verified_br(tokena,'2703')

        #重載2703頁面
        self.driver.switch_to.window(driver.window_handles[1])
        self.driver.get(get_gameoriginalurl('2703'))
        self.driver.implicitly_wait(30)
        time.sleep(3)
        time.sleep(5)
        time.sleep(5)
        
        #進入畫布(遊戲頁面)
        canvas = driver.find_element_by_xpath("//canvas")       
        
        #buy free game
        gamevariable.getgameinfo.click_buyfree('buy27')

        #切換投注記錄視窗
        self.driver.switch_to.window(driver.window_handles[2])

        #驗證2703 buy free game是否成功
        self.verified_br(tokena,'2703')
        time.sleep(2)
        self.verified_br_buyfreegame('2703')

    def test28fruit(self):
        print_time()
        driver = self.driver
        #打開staging 商戶登陸頁面
        self.driver.get(homeurl)
        time.sleep(3)
        self.logininfo()
        self.confirmloginfo()

        #打開2800遊戲測試頁面
        self.driver.execute_script("window.open()")
        self.driver.switch_to.window(driver.window_handles[1])
        self.driver.get(get_gameoriginalurl('2800'))
        self.driver.implicitly_wait(30)
        time.sleep(3)
        
        #驗證遊戲網址
        self.verified_gamelink('2800')
        result = self.verified_gamelink('2800')
        print("打開網址是："+ result)    

        #取得token
        self.get_token('2800')
        tokena = self.get_token('2800')
        print(tokena)

        #self.driver.save_screenshot('./result/'+get_day()+'\\'+get_time()+'-2800-loading.png')
        time.sleep(5)
        #self.driver.save_screenshot('./result/'+get_day()+'\\'+get_time()+'-2800-gamepage.png')
        time.sleep(5)
        
        #進入畫布(遊戲頁面)
        canvas = driver.find_element_by_xpath("//canvas")       
        
        #spin
        gamevariable.getgameinfo.click_spin('space')

        #另開新視窗
        self.driver.execute_script("window.open()")
        self.driver.switch_to.window(driver.window_handles[2])

        #驗證2800是否投注成功
        self.verified_br(tokena,'2800')

        #打開2801遊戲測試頁面
        self.driver.switch_to.window(driver.window_handles[1])
        self.driver.get(get_gameoriginalurl('2801'))
        self.driver.implicitly_wait(30)
        time.sleep(3)
        
        #驗證遊戲網址
        self.verified_gamelink('2801')
        result = self.verified_gamelink('2801')
        print("打開網址是："+ result)    

        #取得token
        self.get_token('2801')
        tokena = self.get_token('2801')
        print(tokena)

        #self.driver.save_screenshot('./result/'+get_day()+'\\'+get_time()+'-2801-loading.png')
        time.sleep(5)
        #self.driver.save_screenshot('./result/'+get_day()+'\\'+get_time()+'-2801-gamepage.png')
        time.sleep(5)
        
        #進入畫布(遊戲頁面)
        canvas = driver.find_element_by_xpath("//canvas")       
        
        #spin
        gamevariable.getgameinfo.click_spin('space')

        #切換視窗
        self.driver.switch_to.window(driver.window_handles[2])

        #驗證2801是否投注成功
        self.verified_br(tokena,'2801')

        #打開2802遊戲測試頁面
        self.driver.switch_to.window(driver.window_handles[1])
        self.driver.get(get_gameoriginalurl('2802'))
        self.driver.implicitly_wait(30)
        time.sleep(3)
        
        #驗證遊戲網址
        self.verified_gamelink('2802')
        result = self.verified_gamelink('2802')
        print("打開網址是："+ result)    

        #取得token
        self.get_token('2802')
        tokena = self.get_token('2802')
        print(tokena)

        #self.driver.save_screenshot('./result/'+get_day()+'\\'+get_time()+'-2802-loading.png')
        time.sleep(5)
        #self.driver.save_screenshot('./result/'+get_day()+'\\'+get_time()+'-2802-gamepage.png')
        time.sleep(5)
        
        #進入畫布(遊戲頁面)
        canvas = driver.find_element_by_xpath("//canvas")       
        
        #spin
        gamevariable.getgameinfo.click_spin('space')

        #切換視窗
        self.driver.switch_to.window(driver.window_handles[2])

        #驗證2802是否投注成功
        self.verified_br(tokena,'2802')

        #打開2803遊戲測試頁面
        self.driver.switch_to.window(driver.window_handles[1])
        self.driver.get(get_gameoriginalurl('2803'))
        self.driver.implicitly_wait(30)
        time.sleep(3)
        
        #驗證遊戲網址
        self.verified_gamelink('2803')
        result = self.verified_gamelink('2803')
        print("打開網址是："+ result)    

        #取得token
        self.get_token('2803')
        tokena = self.get_token('2803')
        print(tokena)

        #self.driver.save_screenshot('./result/'+get_day()+'\\'+get_time()+'-2803-loading.png')
        time.sleep(5)
        #self.driver.save_screenshot('./result/'+get_day()+'\\'+get_time()+'-2803-gamepage.png')
        time.sleep(5)
        
        #進入畫布(遊戲頁面)
        canvas = driver.find_element_by_xpath("//canvas")       
        
        #spin
        gamevariable.getgameinfo.click_spin('space')

        #切換視窗
        self.driver.switch_to.window(driver.window_handles[2])

        #驗證2803是否投注成功
        self.verified_br(tokena,'2803')

        #打開2804遊戲測試頁面
        self.driver.switch_to.window(driver.window_handles[1])
        self.driver.get(get_gameoriginalurl('2804'))
        self.driver.implicitly_wait(30)
        time.sleep(3)
        
        #驗證遊戲網址
        self.verified_gamelink('2804')
        result = self.verified_gamelink('2804')
        print("打開網址是："+ result)    

        #取得token
        self.get_token('2804')
        tokena = self.get_token('2804')
        print(tokena)

        #self.driver.save_screenshot('./result/'+get_day()+'\\'+get_time()+'-2804-loading.png')
        time.sleep(5)
        #self.driver.save_screenshot('./result/'+get_day()+'\\'+get_time()+'-2804-gamepage.png')
        time.sleep(5)
        
        #進入畫布(遊戲頁面)
        canvas = driver.find_element_by_xpath("//canvas")       
        
        #spin
        gamevariable.getgameinfo.click_spin('space')

        #切換視窗
        self.driver.switch_to.window(driver.window_handles[2])

        #驗證2804是否投注成功
        self.verified_br(tokena,'2804')

    def test29grid(self):
        print_time()
        driver = self.driver
        #打開staging 商戶登陸頁面
        self.driver.get(homeurl)
        time.sleep(3)
        self.logininfo()
        self.confirmloginfo()

        #打開2900遊戲測試頁面
        self.driver.execute_script("window.open()")
        self.driver.switch_to.window(driver.window_handles[1])
        self.driver.get(get_gameoriginalurl('2900'))
        self.driver.implicitly_wait(30)
        time.sleep(3)
        
        #驗證遊戲網址
        self.verified_gamelink('2900')
        result = self.verified_gamelink('2900')
        print("打開網址是："+ result)    

        #取得token
        self.get_token('2900')
        tokena = self.get_token('2900')
        print(tokena)

        #self.driver.save_screenshot('./result/'+get_day()+'\\'+get_time()+'-2900-loading.png')
        time.sleep(5)
        #self.driver.save_screenshot('./result/'+get_day()+'\\'+get_time()+'-2900-gamepage.png')
        time.sleep(5)
        
        #進入畫布(遊戲頁面)
        canvas = driver.find_element_by_xpath("//canvas")       
        
        #spin
        gamevariable.getgameinfo.click_spin('space')

        #另開新視窗
        self.driver.execute_script("window.open()")
        self.driver.switch_to.window(driver.window_handles[2])

        #驗證2900是否投注成功
        self.verified_br(tokena,'2900')

        #重載2900頁面
        self.driver.switch_to.window(driver.window_handles[1])
        self.driver.get(get_gameoriginalurl('2900'))
        self.driver.implicitly_wait(30)
        time.sleep(3)
        time.sleep(5)
        time.sleep(5)
        
        #進入畫布(遊戲頁面)
        canvas = driver.find_element_by_xpath("//canvas")       
        
        #buy free game
        gamevariable.getgameinfo.click_buyfree('buy29')

        #切換投注記錄視窗
        self.driver.switch_to.window(driver.window_handles[2])

        #驗證2900 buy free game是否成功
        self.verified_br(tokena,'2900')
        time.sleep(2)
        self.verified_br_buyfreegame('2900')

        #打開2901遊戲測試頁面
        self.driver.switch_to.window(driver.window_handles[1])
        self.driver.get(get_gameoriginalurl('2901'))
        self.driver.implicitly_wait(30)
        time.sleep(3)
        
        #驗證遊戲網址
        self.verified_gamelink('2901')
        result = self.verified_gamelink('2901')
        print("打開網址是："+ result)    

        #取得token
        self.get_token('2901')
        tokena = self.get_token('2901')
        print(tokena)

        #self.driver.save_screenshot('./result/'+get_day()+'\\'+get_time()+'-2901-loading.png')
        time.sleep(5)
        #self.driver.save_screenshot('./result/'+get_day()+'\\'+get_time()+'-2901-gamepage.png')
        time.sleep(5)
        
        #進入畫布(遊戲頁面)
        canvas = driver.find_element_by_xpath("//canvas")       
        
        #spin
        gamevariable.getgameinfo.click_spin('space')

        #切換視窗
        self.driver.switch_to.window(driver.window_handles[2])

        #驗證2901是否投注成功
        self.verified_br(tokena,'2901')

        #重載2901頁面
        self.driver.switch_to.window(driver.window_handles[1])
        self.driver.get(get_gameoriginalurl('2901'))
        self.driver.implicitly_wait(30)
        time.sleep(3)
        time.sleep(5)
        time.sleep(5)
        
        #進入畫布(遊戲頁面)
        canvas = driver.find_element_by_xpath("//canvas")       
        
        #buy free game
        gamevariable.getgameinfo.click_buyfree('buy29')

        #切換投注記錄視窗
        self.driver.switch_to.window(driver.window_handles[2])

        #驗證2901 buy free game是否成功
        self.verified_br(tokena,'2901')
        time.sleep(2)
        self.verified_br_buyfreegame('2901')

        #打開2902遊戲測試頁面
        self.driver.switch_to.window(driver.window_handles[1])
        self.driver.get(get_gameoriginalurl('2902'))
        self.driver.implicitly_wait(30)
        time.sleep(3)
        
        #驗證遊戲網址
        self.verified_gamelink('2902')
        result = self.verified_gamelink('2902')
        print("打開網址是："+ result)    

        #取得token
        self.get_token('2902')
        tokena = self.get_token('2902')
        print(tokena)

        #self.driver.save_screenshot('./result/'+get_day()+'\\'+get_time()+'-2902-loading.png')
        time.sleep(5)
        #self.driver.save_screenshot('./result/'+get_day()+'\\'+get_time()+'-2902-gamepage.png')
        time.sleep(5)
        
        #進入畫布(遊戲頁面)
        canvas = driver.find_element_by_xpath("//canvas")       
        
        #spin
        gamevariable.getgameinfo.click_spin('space')

        #切換視窗
        self.driver.switch_to.window(driver.window_handles[2])

        #驗證2902是否投注成功
        self.verified_br(tokena,'2902')

        #重載2902頁面
        self.driver.switch_to.window(driver.window_handles[1])
        self.driver.get(get_gameoriginalurl('2902'))
        self.driver.implicitly_wait(30)
        time.sleep(3)
        time.sleep(5)
        time.sleep(5)
        
        #進入畫布(遊戲頁面)
        canvas = driver.find_element_by_xpath("//canvas")       
        
        #buy free game
        gamevariable.getgameinfo.click_buyfree('buy29')

        #切換投注記錄視窗
        self.driver.switch_to.window(driver.window_handles[2])

        #驗證2902 buy free game是否成功
        self.verified_br(tokena,'2902')
        time.sleep(2)
        self.verified_br_buyfreegame('2902')
    
    def test30slot(self):
        print_time()
        driver = self.driver
        #打開staging 商戶登陸頁面
        self.driver.get(homeurl)
        time.sleep(3)
        self.logininfo()
        self.confirmloginfo()

        #打開3000遊戲測試頁面
        self.driver.execute_script("window.open()")
        self.driver.switch_to.window(driver.window_handles[1])
        self.driver.get(get_gameoriginalurl('3000'))
        self.driver.implicitly_wait(30)
        time.sleep(3)
        
        #驗證遊戲網址
        self.verified_gamelink('3000')
        result = self.verified_gamelink('3000')
        print("打開網址是："+ result)    

        #取得token
        self.get_token('3000')
        tokena = self.get_token('3000')
        print(tokena)

        #self.driver.save_screenshot('./result/'+get_day()+'\\'+get_time()+'-3000-loading.png')
        time.sleep(5)
        #self.driver.save_screenshot('./result/'+get_day()+'\\'+get_time()+'-3000-gamepage.png')
        time.sleep(5)
        
        #進入畫布(遊戲頁面)
        canvas = driver.find_element_by_xpath("//canvas")       
        
        #spin
        gamevariable.getgameinfo.click_spin('space')

        #另開新視窗
        self.driver.execute_script("window.open()")
        self.driver.switch_to.window(driver.window_handles[2])

        #驗證3000是否投注成功
        self.verified_br(tokena,'3000')

        #重載3000頁面
        self.driver.switch_to.window(driver.window_handles[1])
        self.driver.get(get_gameoriginalurl('3000'))
        self.driver.implicitly_wait(30)
        time.sleep(3)
        time.sleep(5)
        time.sleep(5)
        
        #進入畫布(遊戲頁面)
        canvas = driver.find_element_by_xpath("//canvas")       
        
        #buy free game
        gamevariable.getgameinfo.click_buyfree('buy30')

        #切換投注記錄視窗
        self.driver.switch_to.window(driver.window_handles[2])

        #驗證3000 buy free game是否成功
        self.verified_br(tokena,'3000')
        time.sleep(2)
        self.verified_br_buyfreegame('3000')

        #打開3001遊戲測試頁面
        self.driver.execute_script("window.open()")
        self.driver.switch_to.window(driver.window_handles[1])
        self.driver.get(get_gameoriginalurl('3001'))
        self.driver.implicitly_wait(30)
        time.sleep(3)
        
        #驗證遊戲網址
        self.verified_gamelink('3001')
        result = self.verified_gamelink('3001')
        print("打開網址是："+ result)    

        #取得token
        self.get_token('3001')
        tokena = self.get_token('3001')
        print(tokena)

        #self.driver.save_screenshot('./result/'+get_day()+'\\'+get_time()+'-3001-loading.png')
        time.sleep(5)
        #self.driver.save_screenshot('./result/'+get_day()+'\\'+get_time()+'-3001-gamepage.png')
        time.sleep(5)
        
        #進入畫布(遊戲頁面)
        canvas = driver.find_element_by_xpath("//canvas")       
        
        #spin
        gamevariable.getgameinfo.click_spin('space')

        #另開新視窗
        self.driver.execute_script("window.open()")
        self.driver.switch_to.window(driver.window_handles[2])

        #驗證3001是否投注成功
        self.verified_br(tokena,'3001')

        #重載3001頁面
        self.driver.switch_to.window(driver.window_handles[1])
        self.driver.get(get_gameoriginalurl('3001'))
        self.driver.implicitly_wait(30)
        time.sleep(3)
        time.sleep(5)
        time.sleep(5)
        
        #進入畫布(遊戲頁面)
        canvas = driver.find_element_by_xpath("//canvas")       
        
        #buy free game
        gamevariable.getgameinfo.click_buyfree('buy30')

        #切換投注記錄視窗
        self.driver.switch_to.window(driver.window_handles[2])

        #驗證3001 buy free game是否成功
        self.verified_br(tokena,'3001')
        time.sleep(2)
        self.verified_br_buyfreegame('3001')

        #打開3002遊戲測試頁面
        self.driver.execute_script("window.open()")
        self.driver.switch_to.window(driver.window_handles[1])
        self.driver.get(get_gameoriginalurl('3002'))
        self.driver.implicitly_wait(30)
        time.sleep(3)
        
        #驗證遊戲網址
        self.verified_gamelink('3002')
        result = self.verified_gamelink('3002')
        print("打開網址是："+ result)    

        #取得token
        self.get_token('3002')
        tokena = self.get_token('3002')
        print(tokena)

        #self.driver.save_screenshot('./result/'+get_day()+'\\'+get_time()+'-3002-loading.png')
        time.sleep(5)
        #self.driver.save_screenshot('./result/'+get_day()+'\\'+get_time()+'-3002-gamepage.png')
        time.sleep(5)
        
        #進入畫布(遊戲頁面)
        canvas = driver.find_element_by_xpath("//canvas")       
        
        #spin
        gamevariable.getgameinfo.click_spin('space')

        #另開新視窗
        self.driver.execute_script("window.open()")
        self.driver.switch_to.window(driver.window_handles[2])

        #驗證3002是否投注成功
        self.verified_br(tokena,'3002')

        #重載3002頁面
        self.driver.switch_to.window(driver.window_handles[1])
        self.driver.get(get_gameoriginalurl('3002'))
        self.driver.implicitly_wait(30)
        time.sleep(3)
        time.sleep(5)
        time.sleep(5)
        
        #進入畫布(遊戲頁面)
        canvas = driver.find_element_by_xpath("//canvas")       
        
        #buy free game
        gamevariable.getgameinfo.click_buyfree('buy30')

        #切換投注記錄視窗
        self.driver.switch_to.window(driver.window_handles[2])

        #驗證3002 buy free game是否成功
        self.verified_br(tokena,'3002')
        time.sleep(2)
        self.verified_br_buyfreegame('3002')
    
    def test31slot(self):
        print_time()
        driver = self.driver
        #打開staging 商戶登陸頁面
        self.driver.get(homeurl)
        time.sleep(3)
        self.logininfo()
        self.confirmloginfo()

        #打開3100遊戲測試頁面
        self.driver.execute_script("window.open()")
        self.driver.switch_to.window(driver.window_handles[1])
        self.driver.get(get_gameoriginalurl('3100'))
        self.driver.implicitly_wait(30)
        time.sleep(3)
        
        #驗證3100遊戲網址
        self.verified_gamelink('3100')
        result = self.verified_gamelink('3100')
        print("打開網址是："+ result)    

        #取得token
        self.get_token('3100')
        tokena = self.get_token('3100')
        print(tokena)

        #self.driver.save_screenshot('./result/'+get_day()+'\\'+get_time()+'-3100-loading.png')
        time.sleep(5)
        #self.driver.save_screenshot('./result/'+get_day()+'\\'+get_time()+'-3100-gamepage.png')
        time.sleep(5)
        
        #進入畫布(遊戲頁面)
        canvas = driver.find_element_by_xpath("//canvas")       
        
        #spin
        gamevariable.getgameinfo.click_spin('space')

        #另開新視窗
        self.driver.execute_script("window.open()")
        self.driver.switch_to.window(driver.window_handles[2])

        #驗證3100是否投注成功
        self.verified_br(tokena,'3100')

        #重載3100頁面
        self.driver.switch_to.window(driver.window_handles[1])
        self.driver.get(get_gameoriginalurl('3100'))
        self.driver.implicitly_wait(30)
        time.sleep(3)
        time.sleep(5)
        time.sleep(5)
        
        #進入畫布(遊戲頁面)
        canvas = driver.find_element_by_xpath("//canvas")       
        
        #buy free game
        gamevariable.getgameinfo.click_buyfree('buy31')

        #切換投注記錄視窗
        self.driver.switch_to.window(driver.window_handles[2])

        #驗證3100 buy free game是否成功
        self.verified_br(tokena,'3100')
        time.sleep(2)
        self.verified_br_buyfreegame('3100')

        #打開3101遊戲測試頁面
        self.driver.switch_to.window(driver.window_handles[1])
        self.driver.get(get_gameoriginalurl('3101'))
        self.driver.implicitly_wait(30)
        time.sleep(3)
        
        #驗證3101遊戲網址
        self.verified_gamelink('3101')
        result = self.verified_gamelink('3101')
        print("打開網址是："+ result)    

        #取得token
        self.get_token('3101')
        tokena = self.get_token('3101')
        print(tokena)

        #self.driver.save_screenshot('./result/'+get_day()+'\\'+get_time()+'-3101-loading.png')
        time.sleep(5)
        #self.driver.save_screenshot('./result/'+get_day()+'\\'+get_time()+'-3101-gamepage.png')
        time.sleep(5)
        
        #進入畫布(遊戲頁面)
        canvas = driver.find_element_by_xpath("//canvas")       
        
        #spin
        gamevariable.getgameinfo.click_spin('space')

        #切換視窗
        self.driver.switch_to.window(driver.window_handles[2])

        #驗證3101是否投注成功
        self.verified_br(tokena,'3101')

        #重載3101頁面
        self.driver.switch_to.window(driver.window_handles[1])
        self.driver.get(get_gameoriginalurl('3101'))
        self.driver.implicitly_wait(30)
        time.sleep(3)
        time.sleep(5)
        time.sleep(5)
        
        #進入畫布(遊戲頁面)
        canvas = driver.find_element_by_xpath("//canvas")       
        
        #buy free game
        gamevariable.getgameinfo.click_buyfree('buy31')

        #切換投注記錄視窗
        self.driver.switch_to.window(driver.window_handles[2])

        #驗證3101 buy free game是否成功
        self.verified_br(tokena,'3101')
        time.sleep(2)
        self.verified_br_buyfreegame('3101')

        #打開3102遊戲測試頁面
        self.driver.switch_to.window(driver.window_handles[1])
        self.driver.get(get_gameoriginalurl('3102'))
        self.driver.implicitly_wait(30)
        time.sleep(3)
        
        #驗證3102遊戲網址
        self.verified_gamelink('3102')
        result = self.verified_gamelink('3102')
        print("打開網址是："+ result)    

        #取得token
        self.get_token('3102')
        tokena = self.get_token('3102')
        print(tokena)

        #self.driver.save_screenshot('./result/'+get_day()+'\\'+get_time()+'-3102-loading.png')
        time.sleep(5)
        #self.driver.save_screenshot('./result/'+get_day()+'\\'+get_time()+'-3102-gamepage.png')
        time.sleep(5)
        
        #進入畫布(遊戲頁面)
        canvas = driver.find_element_by_xpath("//canvas")       
        
        #spin
        gamevariable.getgameinfo.click_spin('space')

        #切換視窗
        self.driver.switch_to.window(driver.window_handles[2])

        #驗證3102是否投注成功
        self.verified_br(tokena,'3102')

        #重載3102頁面
        self.driver.switch_to.window(driver.window_handles[1])
        self.driver.get(get_gameoriginalurl('3102'))
        self.driver.implicitly_wait(30)
        time.sleep(3)
        time.sleep(5)
        time.sleep(5)
        
        #進入畫布(遊戲頁面)
        canvas = driver.find_element_by_xpath("//canvas")       
        
        #buy free game
        gamevariable.getgameinfo.click_buyfree('buy31')

        #切換投注記錄視窗
        self.driver.switch_to.window(driver.window_handles[2])

        #驗證3102 buy free game是否成功
        self.verified_br(tokena,'3102')
        time.sleep(2)
        self.verified_br_buyfreegame('3102')

    def test32slot(self):
        print_time()
        driver = self.driver
        #打開staging 商戶登陸頁面
        self.driver.get(homeurl)
        time.sleep(3)
        self.logininfo()
        self.confirmloginfo()

        #打開3200遊戲測試頁面
        self.driver.execute_script("window.open()")
        self.driver.switch_to.window(driver.window_handles[1])
        self.driver.get(get_gameoriginalurl('3200'))
        self.driver.implicitly_wait(30)
        time.sleep(3)
        
        #驗證遊戲網址
        self.verified_gamelink('3200')
        result = self.verified_gamelink('3200')
        print("打開網址是："+ result)    

        #取得token
        self.get_token('3200')
        tokena = self.get_token('3200')
        print(tokena)

        #self.driver.save_screenshot('./result/'+get_day()+'\\'+get_time()+'-3200-loading.png')
        time.sleep(5)
        #self.driver.save_screenshot('./result/'+get_day()+'\\'+get_time()+'-3200-gamepage.png')
        time.sleep(5)
        
        #進入畫布(遊戲頁面)
        canvas = driver.find_element_by_xpath("//canvas")       
        
        #spin
        gamevariable.getgameinfo.click_spin('space')

        #另開新視窗
        self.driver.execute_script("window.open()")
        self.driver.switch_to.window(driver.window_handles[2])

        #驗證3200是否投注成功
        self.verified_br(tokena,'3200')

        #重載3200頁面
        self.driver.switch_to.window(driver.window_handles[1])
        self.driver.get(get_gameoriginalurl('3200'))
        self.driver.implicitly_wait(30)
        time.sleep(3)
        time.sleep(5)
        time.sleep(5)
        
        #進入畫布(遊戲頁面)
        canvas = driver.find_element_by_xpath("//canvas")       
        
        #buy free game
        gamevariable.getgameinfo.click_buyfree('buy32')

        #切換投注記錄視窗
        self.driver.switch_to.window(driver.window_handles[2])

        #驗證3200 buy free game是否成功
        self.verified_br(tokena,'3200')
        time.sleep(2)
        self.verified_br_buyfreegame('3200')
        
        #打開3201遊戲測試頁面
        self.driver.switch_to.window(driver.window_handles[1])
        self.driver.get(get_gameoriginalurl('3201'))
        self.driver.implicitly_wait(30)
        time.sleep(3)
        
        #驗證遊戲網址
        self.verified_gamelink('3201')
        result = self.verified_gamelink('3201')
        print("打開網址是："+ result)    

        #取得token
        self.get_token('3201')
        tokena = self.get_token('3201')
        print(tokena)

        #self.driver.save_screenshot('./result/'+get_day()+'\\'+get_time()+'-3201-loading.png')
        time.sleep(5)
        #self.driver.save_screenshot('./result/'+get_day()+'\\'+get_time()+'-3201-gamepage.png')
        time.sleep(5)
        
        #進入畫布(遊戲頁面)
        canvas = driver.find_element_by_xpath("//canvas")       
        
        #spin
        gamevariable.getgameinfo.click_spin('space')

        #另開新視窗
        self.driver.switch_to.window(driver.window_handles[2])

        #驗證3201是否投注成功
        self.verified_br(tokena,'3201')

        #重載3201頁面
        self.driver.switch_to.window(driver.window_handles[1])
        self.driver.get(get_gameoriginalurl('3201'))
        self.driver.implicitly_wait(30)
        time.sleep(3)
        time.sleep(5)
        time.sleep(5)
        
        #進入畫布(遊戲頁面)
        canvas = driver.find_element_by_xpath("//canvas")       
        
        #buy free game
        gamevariable.getgameinfo.click_buyfree('buy32')

        #切換投注記錄視窗
        self.driver.switch_to.window(driver.window_handles[2])

        #驗證3201 buy free game是否成功
        self.verified_br(tokena,'3201')
        time.sleep(2)
        self.verified_br_buyfreegame('3201')

        #打開3202遊戲測試頁面
        self.driver.switch_to.window(driver.window_handles[1])
        self.driver.get(get_gameoriginalurl('3202'))
        self.driver.implicitly_wait(30)
        time.sleep(3)
        
        #驗證遊戲網址
        self.verified_gamelink('3202')
        result = self.verified_gamelink('3202')
        print("打開網址是："+ result)    

        #取得token
        self.get_token('3202')
        tokena = self.get_token('3202')
        print(tokena)

        #self.driver.save_screenshot('./result/'+get_day()+'\\'+get_time()+'-3202-loading.png')
        time.sleep(5)
        #self.driver.save_screenshot('./result/'+get_day()+'\\'+get_time()+'-3202-gamepage.png')
        time.sleep(5)
        
        #進入畫布(遊戲頁面)
        canvas = driver.find_element_by_xpath("//canvas")       
        
        #spin
        gamevariable.getgameinfo.click_spin('space')

        #另開新視窗
        self.driver.switch_to.window(driver.window_handles[2])

        #驗證3202是否投注成功
        self.verified_br(tokena,'3202')

        #重載3202頁面
        self.driver.switch_to.window(driver.window_handles[1])
        self.driver.get(get_gameoriginalurl('3202'))
        self.driver.implicitly_wait(30)
        time.sleep(3)
        time.sleep(5)
        time.sleep(5)
        
        #進入畫布(遊戲頁面)
        canvas = driver.find_element_by_xpath("//canvas")       
        
        #buy free game
        gamevariable.getgameinfo.click_buyfree('buy32')

        #切換投注記錄視窗
        self.driver.switch_to.window(driver.window_handles[2])

        #驗證3202 buy free game是否成功
        self.verified_br(tokena,'3202')
        time.sleep(2)
        self.verified_br_buyfreegame('3202')


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
    unittest.addTest(test_newuat_new_test("test21fruit"))
    unittest.addTest(test_newuat_new_test("test22slot"))
    unittest.addTest(test_newuat_new_test("test23slot"))
    unittest.addTest(test_newuat_new_test("test24slot"))
    unittest.addTest(test_newuat_new_test("test25grid"))
    unittest.addTest(test_newuat_new_test("test26slot"))
    unittest.addTest(test_newuat_new_test("test27slot"))
    unittest.addTest(test_newuat_new_test("test28fruit"))
    unittest.addTest(test_newuat_new_test("test29grid"))
    unittest.addTest(test_newuat_new_test("test30slot"))
    unittest.addTest(test_newuat_new_test("test31slot"))
    unittest.addTest(test_newuat_new_test("test32slot"))

    #将测试结果写入到result.html中
    fp=open(get_time()+"-new staging agent1 result.html",'wb')
    runner=HTMLTestRunner(stream=fp,title='NGNG Test Report',description='Result:',tester='jay')
    runner.run(unittest)
    fp.close()