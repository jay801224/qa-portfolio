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
#staging測試腳本

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
    return "http://example.internal/play/is_"+game_id
#跳轉前網址+遊戲ID

def get_gameurl(game_id):
    return gamedomain+"/16slot/?gameid="+game_id
#跳轉後網址+遊戲ID



class test_16gamespin(unittest.TestCase):

    def setUp(self):
        # self.driver = webdriver.Chrome()
        options = webdriver.ChromeOptions()
        # options.add_argument('blink-settings=imagesEnabled=false') 
        options.add_argument("--incognito")
        options.add_argument('--no-sandbox')
        # options.add_argument('--window-size=1024,768')
        options.add_argument("--start-maximized")
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
        self.driver.find_element_by_id("form_login").submit()
        time.sleep(3)

    def test1601(self):
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
        #打開1601遊戲測試頁面
        self.driver.execute_script("window.open()")
        self.driver.switch_to.window(driver.window_handles[1])
        self.driver.get(get_gameoriginalurl('1601'))
        self.driver.implicitly_wait(30)
        time.sleep(3)
        currentPageUrl = driver.current_url
        print("打開網址是：", currentPageUrl)
        newcurrenturl = currentPageUrl.split('&token=')[0]
        tokenpara = currentPageUrl.split('&token=')[1]
        urltoken = tokenpara.split('&betrecordurl')[0]
        print("跳轉網址前半段是：", newcurrenturl)
        assert newcurrenturl == get_gameurl('1601'), "当前遊戲网址非预期！"
        pic_path = './result/'+get_day()+'\\'
        self.driver.save_screenshot('./result/'+get_day()+'\\'+get_time()+'-1601-loading.png')
        time.sleep(5)
        self.driver.save_screenshot('./result/'+get_day()+'\\'+get_time()+'-1601-gamepage.png')
        time.sleep(5)

        canvas = driver.find_element_by_xpath("//canvas")       
        # ActionChains(driver).move_by_offset(1075, 900).click()

        pyautogui.click(x=1680, y=880)
        time.sleep(5)
        # can work on chrome
        # ActionChains(driver).move_to_element(canvas).move_by(1075, 900).click().perform()
        # ActionChains(driver).move_to_element(canvas)..click(canvas).perform()
        # work on firefox
        #ActionChains(driver).move_by_offset(-1075, -900).perform() 
        # 将鼠标位置恢复到移动前

        self.driver.save_screenshot('./result/'+get_day()+'\\'+get_time()+'-1601-spin.png')
        time.sleep(3)
        #打開投注記錄頁面
        self.driver.execute_script("window.open()")
        self.driver.switch_to.window(driver.window_handles[2])
        recordurl = betrecordurl+"/?token="+ urltoken +"&lang=id&serverurl=https%3A%2F%2Fexample.internal"
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
            self.assertEqual("Royal777", driver.find_element_by_xpath("//table[@id='__BVID__11']/tbody/tr/td[3]").text)
        except AssertionError as e: 
            self.verificationErrors.append(str(e))
    
    def test1602(self):
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
        #打開1602遊戲測試頁面
        self.driver.execute_script("window.open()")
        self.driver.switch_to.window(driver.window_handles[1])
        self.driver.get(get_gameoriginalurl('1602'))
        self.driver.implicitly_wait(30)
        time.sleep(3)
        currentPageUrl = driver.current_url
        print("打開網址是：", currentPageUrl)
        newcurrenturl = currentPageUrl.split('&token=')[0]
        tokenpara = currentPageUrl.split('&token=')[1]
        urltoken = tokenpara.split('&betrecordurl')[0]
        print("跳轉網址前半段是：", newcurrenturl)
        assert newcurrenturl == get_gameurl('1602'), "当前遊戲网址非预期！"
        pic_path = './result/'+get_day()+'\\'
        self.driver.save_screenshot('./result/'+get_day()+'\\'+get_time()+'-1602-loading.png')
        time.sleep(5)
        self.driver.save_screenshot('./result/'+get_day()+'\\'+get_time()+'-1602-gamepage.png')
        time.sleep(5)

        canvas = driver.find_element_by_xpath("//canvas")       
        # ActionChains(driver).move_by_offset(1075, 900).click()

        pyautogui.click(x=1680, y=880)
        time.sleep(5)
        # can work on chrome
        # ActionChains(driver).move_to_element_with_offset(canvas, 1075, 900).click().perform()
        # work on firefox
        #ActionChains(driver).move_by_offset(-1075, -900).perform() 
        # 将鼠标位置恢复到移动前 

        self.driver.save_screenshot('./result/'+get_day()+'\\'+get_time()+'-1602-spin.png')
        time.sleep(3)
        #打開投注記錄頁面
        self.driver.execute_script("window.open()")
        self.driver.switch_to.window(driver.window_handles[2])
        recordurl = betrecordurl+"/?token="+ urltoken +"&lang=id&serverurl=https%3A%2F%2Fexample.internal"
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
            self.assertEqual("Sushi Sakura", driver.find_element_by_xpath("//table[@id='__BVID__11']/tbody/tr/td[3]").text)
        except AssertionError as e: 
            self.verificationErrors.append(str(e))

    def test1603(self):
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
        #打開1603遊戲測試頁面
        self.driver.execute_script("window.open()")
        self.driver.switch_to.window(driver.window_handles[1])
        self.driver.get(get_gameoriginalurl('1603'))
        self.driver.implicitly_wait(30)
        time.sleep(3)
        currentPageUrl = driver.current_url
        print("打開網址是：", currentPageUrl)
        newcurrenturl = currentPageUrl.split('&token=')[0]
        tokenpara = currentPageUrl.split('&token=')[1]
        urltoken = tokenpara.split('&betrecordurl')[0]
        print("跳轉網址前半段是：", newcurrenturl)
        assert newcurrenturl == get_gameurl('1603'), "当前遊戲网址非预期！"
        pic_path = './result/'+get_day()+'\\'
        self.driver.save_screenshot('./result/'+get_day()+'\\'+get_time()+'-1603-loading.png')
        time.sleep(5)
        self.driver.save_screenshot('./result/'+get_day()+'\\'+get_time()+'-1603-gamepage.png')
        time.sleep(5)
        #x=870  #840+30
        #y=605  #640-35
        canvas = driver.find_element_by_xpath("//canvas")       
        # ActionChains(driver).move_by_offset(1075, 900).click()
        
        pyautogui.click(x=1680, y=880)
        time.sleep(5)
        # can work on chrome
        # ActionChains(driver).move_to_element_with_offset(canvas, 1075, 900).click().perform()
        # work on firefox
        #ActionChains(driver).move_by_offset(-1075, -900).perform() 
        # 将鼠标位置恢复到移动前

        self.driver.save_screenshot('./result/'+get_day()+'\\'+get_time()+'-1603-spin.png')
        time.sleep(3)
        #打開投注記錄頁面
        self.driver.execute_script("window.open()")
        self.driver.switch_to.window(driver.window_handles[2])
        recordurl = betrecordurl+"/?token="+ urltoken +"&lang=id&serverurl=https%3A%2F%2Fexample.internal"
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
            self.assertEqual("Bajak Laut Malaka", driver.find_element_by_xpath("//table[@id='__BVID__11']/tbody/tr/td[3]").text)
        except AssertionError as e: 
            self.verificationErrors.append(str(e))

    def test1604(self):
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
        #打開1604遊戲測試頁面
        self.driver.execute_script("window.open()")
        self.driver.switch_to.window(driver.window_handles[1])
        self.driver.get(get_gameoriginalurl('1604'))
        self.driver.implicitly_wait(30)
        time.sleep(3)
        currentPageUrl = driver.current_url
        print("打開網址是：", currentPageUrl)
        newcurrenturl = currentPageUrl.split('&token=')[0]
        tokenpara = currentPageUrl.split('&token=')[1]
        urltoken = tokenpara.split('&betrecordurl')[0]
        print("跳轉網址前半段是：", newcurrenturl)
        assert newcurrenturl == get_gameurl('1604'), "当前遊戲网址非预期！"
        pic_path = './result/'+get_day()+'\\'
        self.driver.save_screenshot('./result/'+get_day()+'\\'+get_time()+'-1604-loading.png')
        time.sleep(5)
        self.driver.save_screenshot('./result/'+get_day()+'\\'+get_time()+'-1604-gamepage.png')
        time.sleep(5)
        #x=870  #840+30
        #y=605  #640-35
        canvas = driver.find_element_by_xpath("//canvas")       
        # ActionChains(driver).move_by_offset(1075, 900).click()
        
        pyautogui.click(x=1680, y=880)
        time.sleep(5)
        # can work on chrome
        # ActionChains(driver).move_to_element_with_offset(canvas, 1075, 900).click().perform()
        # work on firefox
        #ActionChains(driver).move_by_offset(-1075, -900).perform() 
        # 将鼠标位置恢复到移动前 

        self.driver.save_screenshot('./result/'+get_day()+'\\'+get_time()+'-1604-spin.png')
        time.sleep(3)
        #打開投注記錄頁面
        self.driver.execute_script("window.open()")
        self.driver.switch_to.window(driver.window_handles[2])
        recordurl = betrecordurl+"/?token="+ urltoken +"&lang=id&serverurl=https%3A%2F%2Fexample.internal"
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
            self.assertEqual("Koki Bintang", driver.find_element_by_xpath("//table[@id='__BVID__11']/tbody/tr/td[3]").text)
        except AssertionError as e: 
            self.verificationErrors.append(str(e))

    def test1605(self):
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
        #打開1605遊戲測試頁面
        self.driver.execute_script("window.open()")
        self.driver.switch_to.window(driver.window_handles[1])
        self.driver.get(get_gameoriginalurl('1605'))
        self.driver.implicitly_wait(30)
        time.sleep(3)
        currentPageUrl = driver.current_url
        print("打開網址是：", currentPageUrl)
        newcurrenturl = currentPageUrl.split('&token=')[0]
        tokenpara = currentPageUrl.split('&token=')[1]
        urltoken = tokenpara.split('&betrecordurl')[0]
        print("跳轉網址前半段是：", newcurrenturl)
        assert newcurrenturl == get_gameurl('1605'), "当前遊戲网址非预期！"
        pic_path = './result/'+get_day()+'\\'
        self.driver.save_screenshot('./result/'+get_day()+'\\'+get_time()+'-1605-loading.png')
        time.sleep(5)
        self.driver.save_screenshot('./result/'+get_day()+'\\'+get_time()+'-1605-gamepage.png')
        time.sleep(5)
        #x=870  #840+30
        #y=605  #640-35
        canvas = driver.find_element_by_xpath("//canvas")       
        # ActionChains(driver).move_by_offset(1075, 900).click()

        pyautogui.click(x=1680, y=880)
        time.sleep(5)
        # can work on chrome
        # ActionChains(driver).move_to_element_with_offset(canvas, 1075, 900).click().perform()
        # work on firefox
        #ActionChains(driver).move_by_offset(-1075, -900).perform() 
        # 将鼠标位置恢复到移动前 

        self.driver.save_screenshot('./result/'+get_day()+'\\'+get_time()+'-1605-spin.png')
        time.sleep(3)
        #打開投注記錄頁面
        self.driver.execute_script("window.open()")
        self.driver.switch_to.window(driver.window_handles[2])
        recordurl = betrecordurl+"/?token="+ urltoken +"&lang=id&serverurl=https%3A%2F%2Fexample.internal"
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
            self.assertEqual("Sushi Sakura", driver.find_element_by_xpath("//table[@id='__BVID__11']/tbody/tr/td[3]").text)
        except AssertionError as e: 
            self.verificationErrors.append(str(e))

    def test1606(self):
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
        #打開1606遊戲測試頁面
        self.driver.execute_script("window.open()")
        self.driver.switch_to.window(driver.window_handles[1])
        self.driver.get(get_gameoriginalurl('1606'))
        self.driver.implicitly_wait(30)
        time.sleep(3)
        currentPageUrl = driver.current_url
        print("打開網址是：", currentPageUrl)
        newcurrenturl = currentPageUrl.split('&token=')[0]
        tokenpara = currentPageUrl.split('&token=')[1]
        urltoken = tokenpara.split('&betrecordurl')[0]
        print("跳轉網址前半段是：", newcurrenturl)
        assert newcurrenturl == get_gameurl('1606'), "当前遊戲网址非预期！"
        pic_path = './result/'+get_day()+'\\'
        self.driver.save_screenshot('./result/'+get_day()+'\\'+get_time()+'-1606-loading.png')
        time.sleep(5)
        self.driver.save_screenshot('./result/'+get_day()+'\\'+get_time()+'-1606-gamepage.png')
        time.sleep(5)
        #x=870  #840+30
        #y=605  #640-35
        canvas = driver.find_element_by_xpath("//canvas")       
        # ActionChains(driver).move_by_offset(1075, 900).click()
        
        pyautogui.click(x=1680, y=880)
        time.sleep(5)
        # can work on chrome
        # ActionChains(driver).move_to_element_with_offset(canvas, 1075, 900).click().perform()
        # work on firefox
        #ActionChains(driver).move_by_offset(-1075, -900).perform() 
        # 将鼠标位置恢复到移动前 

        self.driver.save_screenshot('./result/'+get_day()+'\\'+get_time()+'-1606-spin.png')
        time.sleep(3)
        #打開投注記錄頁面
        self.driver.execute_script("window.open()")
        self.driver.switch_to.window(driver.window_handles[2])
        recordurl = betrecordurl+"/?token="+ urltoken +"&lang=id&serverurl=https%3A%2F%2Fexample.internal"
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
            self.assertEqual("Pesta Koktail", driver.find_element_by_xpath("//table[@id='__BVID__11']/tbody/tr/td[3]").text)
        except AssertionError as e: 
            self.verificationErrors.append(str(e))
    
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
    unittest.addTest(test_16gamespin("test1601")) 
    unittest.addTest(test_16gamespin("test1602"))
    unittest.addTest(test_16gamespin("test1603"))
    unittest.addTest(test_16gamespin("test1604"))
    # unittest.addTest(test_16gamespin("test1605"))
    unittest.addTest(test_16gamespin("test1606"))

    #将测试结果写入到result.html中
    fp=open(get_time()+"-16 result.html",'wb')
    runner=HTMLTestRunner(stream=fp,title='16 slot Test Report',description='Result:',tester='jay')
    runner.run(unittest)
    fp.close()