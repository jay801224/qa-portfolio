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


class test_newuattest(unittest.TestCase):

#gameid 位置順序

    br_gamelist = ["1601","1602","1603","1604","1605","1606","1607",
                   "1700","1701","1811","1812",
                   "1817","1820","2000","2001",
                   "1813","1815","1816","1818","1819","1822",
                   "1900","1901","1902","1903","1904","1905","1906","1907","1908",
                   "2100","2101","2102","2103",
                   "2200","2201","2202","2203",
                   "2300","2301","2302",
                   "2400","2401","2402","2403",
                   "2500","2501","2502","2503","2504",
                   "2600","2601","2602","2603",
                   "2700","2701","2702",
                   "2800","2801","2802","2803",
                   "2900","2901",
                   "3000",
                   "3100"]

    br_en_gamename = ["Royal777","Florid Sushi","Pirates of Malacca","Master Cook","Aztec Treasure","Cocktail Party","Tales of Malin Kundang",
                      "Lucky Girl","Golden Shark","The Legend of Hanoman","Tropical Fruits",
                      "Punakawan 777","Food Court","Anti Drugs","90's Toys",
                      "The Legend of Gatotkaca","Djakarta","BALI","Friday Kliwon","Forest Ranger","Dreamy Komodo",
                      "Garudaman","Dangdut Concert","Axe Warrior","Security Post","History of Independence","Bartender","Lutung Kasarung & Princess Purbasari","Beautiful Civil Servant","Beauty of Raja Ampat",
                      "The Curse of Medusa","Happy New Year","On Air Radio","Golden Vishnu",
                      "Crazy Circus","Fantasy Park","Night Market","Blind Warrior",
                      "Lion Dance 888","Juanda Forest","Indonesian Worker",
                      "Phoenix Rises","Ethnical Music Ensemble","90's Snack","Quiz Contest",
                      "Candy Mania","Archipelago Tribes","Harbor of the Queen","Kartini's Story","School Pop",
                      "Dragon Gold","Anti Corruption","Getting Around Jakarta","Anti Drugs Heroes",
                      "Cash Gold","Proclamation of Independence","DominoQQ Big Wins",
                      "Medusa Multiplier","Ganesha Treasure","Aztec Lucky Gems","Lucky Mooncake Festival",
                      "Ultra Gatotkaca",
                      "Aladdin's Fortune"]

    br_cn_gamename = ["Royal777","花漾寿司屋","马六甲奇航","星厨当道","勇闯阿兹特克","鸡尾酒之夜","马林昆当传",
                      "淘金女郎","金鲨银鲨","哈奴曼传奇","欢乐水果秀",
                      "幸运精灵777","爪哇食堂","勇敢拒毒","90 玩具城",
                      "勇者传说","雅加达狂欢","峇里风情","战栗星期五","丛林大冒险","梦幻科摩多",
                      "超能鹰侠","当杜特音乐节","鬼斧战士","安全保卫站","独立荣耀","古典酒吧","爪哇公主与堕落神猿","俏丽公仆","潜进拉贾安帕特",
                      "梅杜莎魔咒","新年快乐","电台好声音","幻惑天王",
                      "疯狂马戏团","奇幻游乐园","夜市好好玩","盲眼战士",
                      "舞狮发发发","朱安达森林","劳工总动员",
                      "凤凰传奇","民族音乐会","90 点心铺","智慧小学堂",
                      "糖果嘉年华","岛屿部落趣","悠游皇后港","民族英雄卡蒂妮","青春萌学院",
                      "神龙秘宝","反对贪腐","雅加达之旅","反毒联盟",
                      "王牌大亨","光荣独立","王牌99",
                      "梅杜莎豪华版","富贵象神","阿兹特克宝石","圆月中秋节",
                      "终极战神",
                      "阿拉丁宝藏"]  
        
    br_ko_gamename = ["Royal777","화려한 초밥","믈라카의 해적","스타 셰프","탐험하다 아즈텍","칵테일 나이트","마린 쿤당 레전드",
                      "행운 소녀","골든 샤크","하누만 전설","열대 과일 쇼",
                      "행운 요정777","자와 식당","용감하게 마약을 거부","90 토이 타운",
                      "가토가챠 전설","자카르타 파티","발리 풍경","무서운 금요일","숲 모험","로맨스 코모도",
                      "슈퍼 호크 맨","돈 더트 콘서트","도끼 전사","보안 스테이션","독립적 인 영광","클래식 바","자바 공주와 타락한 원숭이","아름다운 공무원","라자 암팟의 아름다움",
                      "메두사의 저주","새해 복 많이 받으세요","방송 라디오","비슈누",
                      "미친 서커스","드림 유원지","야시장","눈먼 전사",
                      "사자 춤 888","주안다 숲","노동자 스토리",
                      "피닉스 전설","에스닉 콘서트","90 딤섬 상점","퀴즈 콘테스트",
                      "캔디 카니발","군도 부족","여왕의 항구","카 티니 의 이야기","청춘의 학교",
                      "드래곤 골드","부패 반대","자카르타 투어","마약 방지 연합",
                      "에이스 타이쿤","독립 선언","에이스 99",
                      "메두사 디럭스","코끼리 보물","아즈텍 보석","럭키 중추절",
                      "가토가챠",
                      "알라딘의 보물"]  

    br_id_gamename = ["Royal777","Sushi Sakura","Bajak Laut Malaka","Koki Bintang","Harta Aztec","Pesta Koktail","Kisah Malin Kundang",
                      "Penggali Emas","Hiu Emas","Legenda Hanoman","Buah Tropis",
                      "Punakawan 777","Pujasera","Anti Narkoba","Mainan 90'an",
                      "Legenda Gatotkaca","Djakarta","BALI","Jumat Kliwon","Jagawana 777","Komodo Romantis",
                      "Garudaman","Konser Dangdut","Pendekar Kapak","Poskamling","Sejarah Kemerdekaan","Bartender","Lutung Kasarung & Putri Purbasari","PNS Cantik","Keindahan Raja Ampat",
                      "Kutukan Medusa","Tahun Baruan","On Air Radio","Wisnu Emas",
                      "Sirkus Gila","Taman Fantasi","Pasar Malam","Pendekar Buta",
                      "Lion Dance 888","Hutan Juanda","Nusantara Berkarya",
                      "Phoenix Rises","Karawitan","Jajanan 90'an","Kuis Cerdas Cermat",
                      "Pesta Permen","Adat Nusantara","Pelabuhan Ratu","Kisah Kartini","School Pop",
                      "Naga Emas","Anti Korupsi","Keliling Jakarta","Pahlawan Anti Narkoba",
                      "Cash Gold","Proklamasi Kemerdekaan","DominoQQ Menang Besar",
                      "Medusa Multiplier","Harta Ganesha","Permata Keberuntungan Aztec","Festival Kue Bulan Keberuntungan",
                      "Ultra Gatotkaca",
                      "Aladdin's Fortune"]


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
        elif 2700 <= intgameid and 2702 >= intgameid :
            return gamedomain+"/27slot/?gameid="+game_id
        elif 2800 <= intgameid and 2803 >= intgameid :
            return gamedomain+"/28fruit/?gameid="+game_id
        elif ( intgameid == 2900 ) or ( intgameid == 2901 ) :
            return gamedomain+"/29grid/?gameid="+game_id
        elif intgameid == 3000 :
            return gamedomain+"/30slot/?gameid="+game_id
        elif intgameid == 3100 :
            return gamedomain+"/31slot/?gameid="+game_id
        else :
            return None

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
    
    def get_brgamename(self,game_id,language): 

        location = self.br_gamelist.index(game_id)

        if language == "id" :
            return self.br_id_gamename[location]
        elif language == "en" :
            return self.br_en_gamename[location]
        elif language == "ko" :
            return self.br_ko_gamename[location]
        elif language == "cn" :
            return self.br_cn_gamename[location]
        else :
            print ("語系不正確")
    
    #betrecord total bet 
    def get_brgametotalbet(self,game_id):

        br_totalbet = ["2,000","2,000","2,000","2,000","2,000","2,000","2,000",
                       "3,500","3,500","3,500","3,500",
                       "2,000","2,000","2,000","2,000",
                       "2,250","2,500","2,000","2,250","2,000","2,500",
                       "2,250","2,500","2,000","2,250","2,000","1,875","2,000","2,250","1,875",
                       "2,000","2,000","2,000","2,000",
                       "2,000","2,000","2,000","2,000",
                       "2,000","2,000","2,000",
                       "1,800","1,800","1,800","1,800",
                       "2,000","2,000","2,000","2,000","2,000",
                       "2,000","2,000","2,000","2,000",
                       "2,000","2,000","2,000",
                       "2,000","2,000","2,000","2,000",
                       "2,000",
                       "4,000",]

        # br_totalbet = ["1,000","1,000","1,000","1,000","1,000","1,000","1,000",
        #               "3,500","3,500","3,500","3,500",
        #               "400","400","200","400",
        #               "750","1,250","2,000","450","1,000","1,250",
        #               "225","1,250","500","450","1,000","375","1,000","750","625",
        #               "500","500","250",
        #               "500","500","250","500",
        #               "1,000","1,000","500",
        #               "900","900",
        #               "1,000","1,000","500","1,000",
        #               "1,000"]
        #              #預設最小注

        totalbet = self.br_gamelist.index(game_id)
        return br_totalbet[totalbet]  
    
    #betrecord buy free game
    def get_brbuyfree(self,game_id):
        driver = self.driver
        br_buyfree = [
            ["2400","90,000"],
            ["2600","200,000"],["2601","200,000"],["2602","200,000"],["2603","200,000"],
            ["2700","100,000"],["2701","100,000"],["2702","100,000"],
            ["2900","100,000"],
            ["3000","200,000"]
        ]
        print (game_id)
        for idgame,buyfree in br_buyfree :
            print(idgame, buyfree)
            if idgame == game_id:
                print(buyfree)
                return buyfree
            else :
                print (idgame)


    #betrecord gamename verified
    def verified_br_gamename(self,game_id,language):
        driver = self.driver
        get_brgamename = self.get_brgamename(game_id,language)

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
        get_brgametotalbet = self.get_brgametotalbet(game_id)

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
    
    #betrecord buy free game verified
    def verified_br_buyfreegame(self,game_id):
        driver = self.driver
        get_brbuyfree = self.get_brbuyfree(game_id)

        for i in range(60):
            try:
                if self.is_element_present(By.XPATH, brgamebuyfree): 
                    break
            except: 
                pass
                self.driver.implicitly_wait(30)
            else: 
                self.fail("time out")
        try: 
            self.assertEqual(get_brbuyfree, driver.find_element_by_xpath(brgamebuyfree).text)
            print ("購買免費遊戲驗證結束")
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

    def test16slot(self):
        print_time()
        driver = self.driver
        #打開staging 商戶登陸頁面
        self.driver.get("http://example.internal/")
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
        pyautogui.click(x=1680, y=880)
        time.sleep(5)

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
        pyautogui.click(x=1680, y=880)
        time.sleep(5)

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
        pyautogui.click(x=1680, y=880)
        time.sleep(5)

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
        pyautogui.click(x=1680, y=880)
        time.sleep(5)

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
        pyautogui.click(x=1680, y=880)
        time.sleep(5)

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
        pyautogui.click(x=1680, y=880)
        time.sleep(5)

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
        pyautogui.click(x=1680, y=880)
        time.sleep(5)

        #切換到投注記錄
        self.driver.switch_to.window(driver.window_handles[2])

        #驗證1607是否投注成功
        self.verified_br(tokena,'1607')
    
    def testscratch(self):
        print_time()
        driver = self.driver
        #打開staging 商戶登陸頁面
        self.driver.get("http://example.internal/")
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
        # ActionChains(driver).move_by_offset(1075, 900).click()
        pyautogui.click(x=1420, y=1000)
        #刮刮卡坐標
        # can work on chrome
        time.sleep(5)
        #刮開刮刮卡
        pyautogui.click(x=1420, y=1000)
        # ActionChains(driver).move_to_element_with_offset(canvas, 1075, 900).click().perform()
        # work on firefox
        #ActionChains(driver).move_by_offset(-1075, -900).perform() # 将鼠标位置恢复到移动前 
        #self.driver.save_screenshot('./result/'+get_day()+'\\'+get_time()+'1700-spin.png')
        #time.sleep(3)

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
        # ActionChains(driver).move_by_offset(1075, 900).click()
        pyautogui.click(x=1420, y=1000)
        #刮刮卡坐標
        # can work on chrome
        time.sleep(5)
        #刮開刮刮卡
        pyautogui.click(x=1420, y=1000)
        # ActionChains(driver).move_to_element_with_offset(canvas, 1075, 900).click().perform()
        # work on firefox
        #ActionChains(driver).move_by_offset(-1075, -900).perform() # 将鼠标位置恢复到移动前 
        #self.driver.save_screenshot('./result/'+get_day()+'\\'+get_time()+'1700-spin.png')
        #time.sleep(3)

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
        # ActionChains(driver).move_by_offset(1075, 900).click()
        pyautogui.click(x=1420, y=1000)
        #刮刮卡坐標
        # can work on chrome
        time.sleep(5)
        #刮開刮刮卡
        pyautogui.click(x=1420, y=1000)
        # ActionChains(driver).move_to_element_with_offset(canvas, 1075, 900).click().perform()
        # work on firefox
        #ActionChains(driver).move_by_offset(-1075, -900).perform() # 将鼠标位置恢复到移动前 
        #self.driver.save_screenshot('./result/'+get_day()+'\\'+get_time()+'1700-spin.png')
        #time.sleep(3)

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
        # ActionChains(driver).move_by_offset(1075, 900).click()
        pyautogui.click(x=1420, y=1000)
        #刮刮卡坐標
        # can work on chrome
        time.sleep(5)
        #刮開刮刮卡
        pyautogui.click(x=1420, y=1000)
        # ActionChains(driver).move_to_element_with_offset(canvas, 1075, 900).click().perform()
        # work on firefox
        #ActionChains(driver).move_by_offset(-1075, -900).perform() # 将鼠标位置恢复到移动前 
        #self.driver.save_screenshot('./result/'+get_day()+'\\'+get_time()+'1812-spin.png')
        #time.sleep(3)

        #切換至投注記錄視窗
        self.driver.switch_to.window(driver.window_handles[2])

        #驗證1812是否投注成功
        self.verified_br(tokena,'1812')
    
    def testfruit(self):
        print_time()
        driver = self.driver
        #打開staging 商戶登陸頁面
        self.driver.get("http://example.internal/")
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
        pyautogui.click(x=1680, y=880)
        time.sleep(5)

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
        pyautogui.click(x=1680, y=880)
        time.sleep(5)

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
        pyautogui.click(x=1680, y=880)
        time.sleep(5)

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
        pyautogui.click(x=1680, y=880)
        time.sleep(5)

        #切換至投注記錄視窗
        self.driver.switch_to.window(driver.window_handles[2])

        #驗證2001是否投注成功
        self.verified_br(tokena,'2001')
        
    def test18slot(self):
        print_time()
        driver = self.driver
        #打開staging 商戶登陸頁面
        self.driver.get("http://example.internal/")
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
        pyautogui.click(x=1680, y=880)
        time.sleep(5)

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
        pyautogui.click(x=1680, y=880)
        time.sleep(5)

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
        pyautogui.click(x=1680, y=880)
        time.sleep(5)

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
        pyautogui.click(x=1680, y=880)
        time.sleep(5)

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
        pyautogui.click(x=1680, y=880)
        time.sleep(5)

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
        pyautogui.click(x=1680, y=880)
        time.sleep(5)

        #切換到投注記錄
        self.driver.switch_to.window(driver.window_handles[2])

        #驗證1822是否投注成功
        self.verified_br(tokena,'1822')
    
    def test19slot(self):
        print_time()
        driver = self.driver
        #打開staging 商戶登陸頁面
        self.driver.get("http://example.internal/")
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
        pyautogui.click(x=1680, y=880)
        time.sleep(5)

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
        pyautogui.click(x=1680, y=880)
        time.sleep(5)

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
        pyautogui.click(x=1680, y=880)
        time.sleep(5)

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
        pyautogui.click(x=1680, y=880)
        time.sleep(5)

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
        pyautogui.click(x=1680, y=880)
        time.sleep(5)

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
        pyautogui.click(x=1680, y=880)
        time.sleep(5)

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
        pyautogui.click(x=1680, y=880)
        time.sleep(5)

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
        pyautogui.click(x=1680, y=880)
        time.sleep(5)

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
        pyautogui.click(x=1680, y=880)
        time.sleep(5)

        #切換到投注記錄
        self.driver.switch_to.window(driver.window_handles[2])

        #驗證1908是否投注成功
        self.verified_br(tokena,'1908')
    
    def test21fruit(self):
        print_time()
        driver = self.driver
        #打開staging 商戶登陸頁面
        self.driver.get("http://example.internal/")
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
        pyautogui.click(x=1680, y=880)
        time.sleep(5)

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
        pyautogui.click(x=1680, y=880)
        time.sleep(5)

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
        pyautogui.click(x=1680, y=880)
        time.sleep(5)

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
        pyautogui.click(x=1680, y=880)
        time.sleep(5)

        #切換到投注記錄
        self.driver.switch_to.window(driver.window_handles[2])

        #驗證2103是否投注成功
        self.verified_br(tokena,'2103')
    
    def test22slot(self):
        print_time()
        driver = self.driver
        #打開staging 商戶登陸頁面
        self.driver.get("http://example.internal/")
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
        pyautogui.click(x=1680, y=880)
        time.sleep(5)

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
        pyautogui.click(x=1680, y=880)
        time.sleep(5)

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
        pyautogui.click(x=1680, y=880)
        time.sleep(5)

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
        pyautogui.click(x=1680, y=880)
        time.sleep(5)

        #切換到投注記錄
        self.driver.switch_to.window(driver.window_handles[2])

        #驗證2203是否投注成功
        self.verified_br(tokena,'2203')

    def test23slot(self):
        print_time()
        driver = self.driver
        #打開staging 商戶登陸頁面
        self.driver.get("http://example.internal/")
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
        pyautogui.click(x=1680, y=880)
        time.sleep(5)

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
        pyautogui.click(x=1680, y=880)
        time.sleep(5)

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
        pyautogui.click(x=1680, y=880)
        time.sleep(5)

        #切換到投注記錄
        self.driver.switch_to.window(driver.window_handles[2])

        #驗證2302是否投注成功
        self.verified_br(tokena,'2302')
    
    def test24slot(self):
        print_time()
        driver = self.driver
        #打開staging 商戶登陸頁面
        self.driver.get("http://example.internal/")
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
        pyautogui.click(x=1680, y=880)
        time.sleep(5)

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
        pyautogui.click(x=230, y=540)
        time.sleep(2)
        pyautogui.click(x=1140, y=780)
        time.sleep(5)

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
        pyautogui.click(x=1680, y=880)
        time.sleep(5)

        #切換到投注記錄
        self.driver.switch_to.window(driver.window_handles[2])

        #驗證2401是否投注成功
        self.verified_br(tokena,'2401')

        #打開2402遊戲測試頁面
        self.driver.switch_to.window(driver.window_handles[1])
        self.driver.get(get_gameoriginalurl('2402'))
        self.driver.implicitly_wait(30)
        time.sleep(3)
        
        #驗證2401遊戲網址
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
        pyautogui.click(x=1680, y=880)
        time.sleep(5)

        #切換到投注記錄
        self.driver.switch_to.window(driver.window_handles[2])

        #驗證2402是否投注成功
        self.verified_br(tokena,'2402')

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
        pyautogui.click(x=1680, y=880)
        time.sleep(5)

        #切換到投注記錄
        self.driver.switch_to.window(driver.window_handles[2])

        #驗證2403是否投注成功
        self.verified_br(tokena,'2403')

    def test25grid(self):
        print_time()
        driver = self.driver
        #打開staging 商戶登陸頁面
        self.driver.get("http://example.internal/")
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
        pyautogui.click(x=1680, y=880)
        time.sleep(5)

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
        pyautogui.click(x=1680, y=880)
        time.sleep(5)

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
        pyautogui.click(x=1680, y=880)
        time.sleep(5)

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
        pyautogui.click(x=1680, y=880)
        time.sleep(5)

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
        pyautogui.click(x=1680, y=880)
        time.sleep(5)

        #切換到投注記錄
        self.driver.switch_to.window(driver.window_handles[2])

        #驗證2504是否投注成功
        self.verified_br(tokena,'2504')

    def test26slot(self):
        print_time()
        driver = self.driver
        #打開staging 商戶登陸頁面
        self.driver.get("http://example.internal/")
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
        pyautogui.click(x=1680, y=880)
        time.sleep(5)

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
        pyautogui.click(x=180, y=560)
        time.sleep(2)
        pyautogui.click(x=1090, y=765)
        time.sleep(5)

        #切換投注記錄視窗
        self.driver.switch_to.window(driver.window_handles[2])

        #驗證2600 buy free game是否成功
        self.verified_br(tokena,'2600')
        time.sleep(2)
        self.verified_br_buyfreegame('2600')

        #打開2601遊戲測試頁面
        self.driver.execute_script("window.open()")
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
        pyautogui.click(x=1680, y=880)
        time.sleep(5)

        #另開新視窗
        self.driver.execute_script("window.open()")
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
        pyautogui.click(x=180, y=560)
        time.sleep(2)
        pyautogui.click(x=1090, y=765)
        time.sleep(5)

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
        pyautogui.click(x=1680, y=880)
        time.sleep(5)

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
        pyautogui.click(x=180, y=560)
        time.sleep(2)
        pyautogui.click(x=1090, y=765)
        time.sleep(5)

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
        pyautogui.click(x=1680, y=880)
        time.sleep(5)

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
        pyautogui.click(x=180, y=560)
        time.sleep(2)
        pyautogui.click(x=1090, y=765)
        time.sleep(5)

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
        self.driver.get("http://example.internal/")
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
        pyautogui.click(x=1680, y=880)
        time.sleep(5)

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
        pyautogui.click(x=180, y=600)
        time.sleep(2)
        pyautogui.click(x=1130, y=780)
        time.sleep(5)

        #切換投注記錄視窗
        self.driver.switch_to.window(driver.window_handles[2])

        #驗證2700 buy free game是否成功
        self.verified_br(tokena,'2700')
        time.sleep(2)
        self.verified_br_buyfreegame('2700')

        #打開2701遊戲測試頁面
        self.driver.execute_script("window.open()")
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
        pyautogui.click(x=1680, y=880)
        time.sleep(5)

        #另開新視窗
        self.driver.execute_script("window.open()")
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
        pyautogui.click(x=180, y=600)
        time.sleep(2)
        pyautogui.click(x=1150, y=770)
        time.sleep(5)

        #切換投注記錄視窗
        self.driver.switch_to.window(driver.window_handles[2])

        #驗證2701 buy free game是否成功
        self.verified_br(tokena,'2701')
        time.sleep(2)
        self.verified_br_buyfreegame('2701')

        #打開2702遊戲測試頁面
        self.driver.execute_script("window.open()")
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
        pyautogui.click(x=1680, y=880)
        time.sleep(5)

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
        pyautogui.click(x=180, y=600)
        time.sleep(2)
        pyautogui.click(x=1150, y=770)
        time.sleep(5)

        #切換投注記錄視窗
        self.driver.switch_to.window(driver.window_handles[2])

        #驗證2702 buy free game是否成功
        self.verified_br(tokena,'2702')
        time.sleep(2)
        self.verified_br_buyfreegame('2702')

    def test28fruit(self):
        print_time()
        driver = self.driver
        #打開staging 商戶登陸頁面
        self.driver.get("http://example.internal/")
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
        pyautogui.click(x=920, y=990)
        time.sleep(5)

        #另開新視窗
        self.driver.execute_script("window.open()")
        self.driver.switch_to.window(driver.window_handles[2])

        #驗證2800是否投注成功
        self.verified_br(tokena,'2800')

        #打開2801遊戲測試頁面
        self.driver.execute_script("window.open()")
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
        pyautogui.click(x=920, y=990)
        time.sleep(5)

        #另開新視窗
        self.driver.execute_script("window.open()")
        self.driver.switch_to.window(driver.window_handles[2])

        #驗證2801是否投注成功
        self.verified_br(tokena,'2801')

    def test29grid(self):
        print_time()
        driver = self.driver
        #打開staging 商戶登陸頁面
        self.driver.get("http://example.internal/")
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
        pyautogui.click(x=920, y=990)
        time.sleep(5)

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
        pyautogui.click(x=1130, y=790)
        time.sleep(2)
        pyautogui.click(x=1030, y=640)
        time.sleep(5)

        #切換投注記錄視窗
        self.driver.switch_to.window(driver.window_handles[2])

        #驗證2900 buy free game是否成功
        self.verified_br(tokena,'2900')
        time.sleep(2)
        self.verified_br_buyfreegame('2900')
    
    def test30slot(self):
        print_time()
        driver = self.driver
        #打開staging 商戶登陸頁面
        self.driver.get("http://example.internal/")
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
        pyautogui.click(x=920, y=990)
        time.sleep(5)

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
        pyautogui.click(x=925, y=820)
        time.sleep(2)
        pyautogui.click(x=920, y=660)
        time.sleep(5)

        #切換投注記錄視窗
        self.driver.switch_to.window(driver.window_handles[2])

        #驗證3000 buy free game是否成功
        self.verified_br(tokena,'3000')
        time.sleep(2)
        self.verified_br_buyfreegame('3000')


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
    unittest.addTest(test_newuattest("test16slot"))
    unittest.addTest(test_newuattest("testscratch"))
    unittest.addTest(test_newuattest("testfruit"))
    unittest.addTest(test_newuattest("test18slot"))
    unittest.addTest(test_newuattest("test19slot"))
    unittest.addTest(test_newuattest("test21fruit"))
    unittest.addTest(test_newuattest("test22slot"))
    unittest.addTest(test_newuattest("test23slot"))
    unittest.addTest(test_newuattest("test24slot"))
    unittest.addTest(test_newuattest("test25grid"))
    unittest.addTest(test_newuattest("test26slot"))
    unittest.addTest(test_newuattest("test27slot"))
    unittest.addTest(test_newuattest("test28fruit"))
    unittest.addTest(test_newuattest("test29grid"))
    unittest.addTest(test_newuattest("test30slot"))

    #将测试结果写入到result.html中
    fp=open(get_time()+"-new staging result.html",'wb')
    runner=HTMLTestRunner(stream=fp,title='all by type Test Report',description='Result:',tester='jay')
    runner.run(unittest)
    fp.close()