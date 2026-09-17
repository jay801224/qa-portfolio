import  pyautogui, time
import  urlvariable
from selenium import webdriver


# gameid 位置順序

br_gamelist = ["1601", "1602", "1603", "1604", "1605", "1606", "1607",
               "1700", "1701", "1811", "1812",
               "1817", "1820", "2000", "2001",
               "1813", "1815", "1816", "1818", "1819", "1822",
               "1900", "1901", "1902", "1903", "1904", "1905", "1906", "1907", "1908",
               "1001",
               "2100", "2101", "2102", "2103", "2104",
               "2200", "2201", "2202", "2203",
               "2300", "2301", "2302",
               "2400", "2401", "2402", "2403",
               "2500", "2501", "2502", "2503", "2504",
               "2600", "2601", "2602", "2603",
               "2700", "2701", "2702", "2703",
               "2800", "2801", "2802", "2803", "2804",
               "2900", "2901", "2902",
               "3000", "3001", "3002",
               "3100", "3101", "3102",
               "3200", "3201", "3202",
               "3300", "3301", "3302",
               "3400", "3401", "3402",
               "3500", "3501", "3502",
               "3600",
               "3700"
               ]

br_en_gamename = ["Game 01", "Game 02", "Game 03", "Game 04", "Game 05", "Game 06", "Game 07",
                  "Game 08", "Game 09", "Game 10", "Game 11",
                  "Game 12", "Game 13", "Game 14", "Game 15",
                  "Game 16", "Game 17", "Game 18", "Game 19", "Game 20", "Game 21",
                  "Game 22", "Game 23", "Game 24", "Game 25", "Game 26", "Game 27", "Game 28", "Game 29", "Game 30",
                  "Game 31",
                  "Game 32", "Game 33", "Game 34", "Game 35", "Game 36", 
                  "Game 37", "Game 38", "Game 39", "Game 40",
                  "Game 41", "Game 42", "Game 43",
                  "Game 44", "Game 45", "Game 46", "Game 47",
                  "Game 48", "Game 49", "Game 50", "Game 51", "Game 52",
                  "Game 53", "Game 54", "Game 55", "Game 56",
                  "Game 57", "Game 58", "Game 59", "Game 60",
                  "Game 61", "Game 62", "Game 63", "Game 64", "Game 65",
                  "Game 66", "Game 67", "Game 68",
                  "Game 69", "Game 70", "Game 71", 
                  "Game 72", "Game 73", "Game 74",
                  "Game 75", "Game 76", "Game 77",
                  "Game 78", "Game 79", "Game 80", 
                  "Game 81", "Game 82", "Game 83",
                  "Game 84", "Game 85", "Game 86",
                  "Game 87",
                  "Game 88"
                  ]

br_cn_gamename = ["Game 01", "Game 02", "Game 03", "Game 04", "Game 05", "Game 06", "Game 07",
                  "Game 08", "Game 09", "Game 10", "Game 11",
                  "Game 12", "Game 13", "Game 14", "Game 15",
                  "Game 16", "Game 17", "Game 18", "Game 19", "Game 20", "Game 21",
                  "Game 22", "Game 23", "Game 24", "Game 25", "Game 26", "Game 27", "Game 28", "Game 29", "Game 30",
                  "Game 31",
                  "Game 32", "Game 33", "Game 34", "Game 35", "Game 36",
                  "Game 37", "Game 38", "Game 39", "Game 40",
                  "Game 41", "Game 42", "Game 43",
                  "Game 44", "Game 45", "Game 46", "Game 47",
                  "Game 48", "Game 49", "Game 50", "Game 51", "Game 52",
                  "Game 53", "Game 54", "Game 55", "Game 56",
                  "Game 57", "Game 58", "Game 59", "Game 60",
                  "Game 61", "Game 62", "Game 63", "Game 64", "Game 65",
                  "Game 66", "Game 67", "Game 68",
                  "Game 69", "Game 70", "Game 71", 
                  "Game 72", "Game 73", "Game 74",
                  "Game 75", "Game 76", "Game 77",
                  "Game 78", "Game 79", "Game 80", 
                  "Game 81", "Game 82", "Game 83",
                  "Game 84", "Game 85", "Game 86",
                  "Game 87",
                  "Game 88"
                  ]

br_ko_gamename = ["Game 01", "Game 02", "Game 03", "Game 04", "Game 05", "Game 06", "Game 07",
                  "Game 08", "Game 09", "Game 10", "Game 11",
                  "Game 12", "Game 13", "Game 14", "Game 15",
                  "Game 16", "Game 17", "Game 18", "Game 19", "Game 20", "Game 21",
                  "Game 22", "Game 23", "Game 24", "Game 25", "Game 26", "Game 27", "Game 28", "Game 29", "Game 30",
                  "Game 31",
                  "Game 32", "Game 33", "Game 34", "Game 35", "Game 36",
                  "Game 37", "Game 38", "Game 39", "Game 40",
                  "Game 41", "Game 42", "Game 43",
                  "Game 44", "Game 45", "Game 46", "Game 47",
                  "Game 48", "Game 49", "Game 50", "Game 51", "Game 52",
                  "Game 53", "Game 54", "Game 55", "Game 56",
                  "Game 57", "Game 58", "Game 59", "Game 60",
                  "Game 61", "Game 62", "Game 63", "Game 64", "Game 65",
                  "Game 66", "Game 67", "Game 68",
                  "Game 69", "Game 70", "Game 71",
                  "Game 72", "Game 73", "Game 74", 
                  "Game 75", "Game 76", "Game 77",
                  "Game 78", "Game 79", "Game 80", 
                  "Game 81", "Game 82", "Game 83",
                  "Game 84", "Game 85", "Game 86",
                  "Game 87",
                  "Game 88"
                  ]

br_id_gamename = ["Game 01", "Game 02", "Game 03", "Game 04", "Game 05", "Game 06", "Game 07",
                  "Game 08", "Game 09", "Game 10", "Game 11",
                  "Game 12", "Game 13", "Game 14", "Game 15",
                  "Game 16", "Game 17", "Game 18", "Game 19", "Game 20", "Game 21",
                  "Game 22", "Game 23", "Game 24", "Game 25", "Game 26", "Game 27", "Game 28", "Game 29", "Game 30",
                  "Game 31",
                  "Game 32", "Game 33", "Game 34", "Game 35", "Game 36",
                  "Game 37", "Game 38", "Game 39", "Game 40",
                  "Game 41", "Game 42", "Game 43",
                  "Game 44", "Game 45", "Game 46", "Game 47",
                  "Game 48", "Game 49", "Game 50", "Game 51", "Game 52",
                  "Game 53", "Game 54", "Game 55", "Game 56",
                  "Game 57", "Game 58", "Game 59", "Game 60",
                  "Game 61", "Game 62", "Game 63", "Game 64", "Game 65", 
                  "Game 66", "Game 67", "Game 68",
                  "Game 69", "Game 70", "Game 71",
                  "Game 72", "Game 73", "Game 74", 
                  "Game 75", "Game 76", "Game 77",
                  "Game 78", "Game 79", "Game 80", 
                  "Game 81","Game 82", "Game 83",
                  "Game 84", "Game 85", "Game 86",
                  "Game 87",
                  "Game 88"
                  ]

br_totalbet = ["1,000", "1,000", "1,000", "1,000", "1,000", "1,000", "1,000",
               "1,000", "1,000", "1,000", "1,000",
               "1,000", "1,000", "1,000", "1,000",
               "1,000", "1,000", "1,000", "1,000", "1,000", "1,000",
               "1,000", "1,000", "1,000", "1,000", "1,000", "1,000", "1,000", "1,000", "1,000",
               "1,000",
               "1,000", "1,000", "1,000", "1,000", "1,000",
               "1,000", "1,000", "1,000", "1,000",
               "1,000", "1,000", "1,000",
               "1,000", "1,000", "1,000", "1,000",
               "1,000", "1,000", "1,000", "1,000", "1,000",
               "1,000", "1,000", "1,000", "1,000",
               "1,000", "1,000", "1,000", "1,000",
               "1,000", "1,000", "1,000", "1,000", "1,000",
               "1,000", "1,000", "1,000",
               "1,000", "1,000", "1,000",
               "1,000", "1,000", "1,000",
               "1,000", "1,000", "1,000",
               "1,000", "1,000", "1,000",
               "1,000", "1,000", "1,000",
               "1,000", "1,000", "1,000",
               "1,000",
               "1,000"
               ]

br_php_totalbet = ["1.00", "1.00", "1.00", "1.00", "1.00", "1.00", "",
               "1.00", "1.00", "1.00", "1.00",
               "", "", "", "",
               "", "", "", "", "", "",
               "", "", "", "", "", "", "", "", "",
               "",
               "1.00", "1.00", "1.00", "1.00", "1.00",
               "1.00", "1.00", "1.00", "1.00",
               "1.00", "1.00", "1.00",
               "1.00", "1.00", "1.00", "1.00",
               "1.00", "1.00", "1.00", "", "1.00",
               "1.00", "", "1.00", "",
               "1.00", "", "1.00", "1.00",
               "1.00", "1.00", "1.00", "1.00", "1.00",
               "1.00", "1.00", "1.00",
               "1.00", "1.00", "1.00",
               "1.00", "1.00", "1.00",
               "1.00", "1.00", "1.00",
               "1.00", "1.00", "1.00",
               "1.00", "1.00", "1.00",
               "1.00", "1.00", "1.00",
               "1.00",
               ""
               ]

class getgameinfo ():
    
    def setUp(self):
       
        options = webdriver.ChromeOptions()
        options.add_argument("--incognito")
        options.add_argument('--no-sandbox')
        options.add_argument("--window-position=0,0")
        options.add_argument('--window-size=1024,768')
        
        self.driver = webdriver.Chrome(options=options)
        self.driver.implicitly_wait(30)
        self.base_url = "https://www.google.com/"
        self.verificationErrors = []
        self.accept_next_alert = True

    # get gamename
    def get_gamename(game_id, language):
        location = br_gamelist.index(game_id)

        if language == "id":
            return br_id_gamename[location]
        elif language == "en":
            return br_en_gamename[location]
        elif language == "ko":
            return br_ko_gamename[location]
        elif language == "cn":
            return br_cn_gamename[location]
        elif language == "vi":
            return br_vi_gamename[location]
        else:
            print("語系不正確")
    
    # get game totalbet
    def get_gametotalbet(game_id):

        location = br_gamelist.index(game_id)
        return br_totalbet[location]

    # get game buy free totalbet
    def get_gamebuyfree(game_id):
        game_buyfree = [
            ["2400", "100,000"],  ["2401", "100,000"], ["2402", "100,000"], ["2403", "100,000"],
            ["2600", "100,000"], ["2601", "100,000"], ["2602", "100,000"], ["2603", "100,000"],
            ["2700", "100,000"], ["2701", "100,000"], ["2702", "100,000"], ["2703", "100,000"],
            ["2900", "100,000"], ["2901", "100,000"], ["2902", "100,000"],
            ["3000", "100,000"], ["3001", "100,000"], ["3002", "100,000"],
            ["3100", "100,000"], ["3101", "100,000"], ["3102", "100,000"],
            ["3200", "100,000"], ["3201", "100,000"], ["3202", "100,000"],
            ["3300", "100,000"], ["3301", "100,000"], ["3302", "100,000"],
            ["3400", "100,000"], ["3401", "100,000"], ["3402", "100,000"],
            ["3500", "100,000"], ["3501", "100,000"], ["3502", "100,000"]
        ]
        for idgame, buyfree in game_buyfree:
            try :
                if idgame == game_id:
                    return buyfree
            except: 
                print(game_id + "has something wrong")
                pass
    

# 取得 staging / prod 跳轉後網址+遊戲ID
    def get_gameurln(self, game_id, gamedomain):   

        intgameid = int(game_id)
        
        e8slot = {1813,1815,1816,1818,1819,1822}
        frameworkslot = {3300,3301,3302,3400,3401,3402,3500,3501,3502,3600}
   
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
        elif 3000 <= intgameid and 3002 >= intgameid :
            return gamedomain+"/30slot/?gameid="+game_id
        elif 3100 <= intgameid and 3102 >= intgameid :
            return gamedomain+"/31slot/?gameid="+game_id
        elif 3200 <= intgameid and 3202 >= intgameid :
            return gamedomain+"/32slot/?gameid="+game_id
        elif intgameid in frameworkslot :
            return gamedomain+"/framework/?gameid="+game_id
        elif intgameid == 3700 :
            return gamedomain+"/37slot/?gameid="+game_id
        else :
            return None

# 取得 demo 跳轉後網址+遊戲ID
    def get_gameurlnd(self, game_id, gamedomain, betrecordurl, serverurl):   
        
        testtoken = "<REDACTED>"
        # <ACCOUNT> for ID
        # <ACCOUNT> for PHP
        intgameid = int(game_id)

        e8slot = {1813, 1815, 1816, 1818, 1819, 1822}
        frameworkslot = {3300,3301,3302,3400,3401,3402,3500,3501,3502,3600}
        otherlink = "&betrecordurl=" + betrecordurl +"&lang=en&homeurl=https://localhost&mode=0&serverurl=https://"+ serverurl

        if intgameid == 1001:
            return gamedomain+"/10fruit/?gameid="+game_id+"&token="+testtoken+game_id+otherlink
        elif 1601 <= intgameid and 1607 >= intgameid:
            return gamedomain+"/16slot/?gameid="+game_id+"&token="+testtoken+game_id+otherlink
        elif (intgameid == 1700) or (intgameid == 1701):
            return gamedomain+"/17scratch/?gameid="+game_id+"&token="+testtoken+game_id+otherlink
        elif (intgameid == 1811) or (intgameid == 1812):
            return gamedomain+"/18scratch/?gameid="+game_id+"&token="+testtoken+game_id+otherlink
        elif intgameid in e8slot:
            return gamedomain+"/18slot/?gameid="+game_id+"&token="+testtoken+game_id+otherlink
        elif (intgameid == 1817) or (intgameid == 1820):
            return gamedomain+"/18fruit/?gameid="+game_id+"&token="+testtoken+game_id+otherlink
        elif 2000 <= intgameid and 2001 >= intgameid:
            return gamedomain+"/20fruit/?gameid="+game_id+"&token="+testtoken+game_id+otherlink
        elif 1900 <= intgameid and 1908 >= intgameid:
            return gamedomain+"/19slot/?gameid="+game_id+"&token="+testtoken+game_id+otherlink
        elif 2100 <= intgameid and 2104 >= intgameid:
            return gamedomain+"/21fruit/?gameid="+game_id+"&token="+testtoken+game_id+otherlink
        elif 2200 <= intgameid and 2203 >= intgameid:
            return gamedomain+"/22slot/?gameid="+game_id+"&token="+testtoken+game_id+otherlink
        elif 2300 <= intgameid and 2302 >= intgameid:
            return gamedomain+"/23slot/?gameid="+game_id+"&token="+testtoken+game_id+otherlink
        elif 2400 <= intgameid and 2403 >= intgameid:
            return gamedomain+"/24slot/?gameid="+game_id+"&token="+testtoken+game_id+otherlink
        elif 2500 <= intgameid and 2504 >= intgameid:
            return gamedomain+"/25grid/?gameid="+game_id+"&token="+testtoken+game_id+otherlink
        elif 2600 <= intgameid and 2603 >= intgameid:
            return gamedomain+"/26slot/?gameid="+game_id+"&token="+testtoken+game_id+otherlink
        elif 2700 <= intgameid and 2703 >= intgameid:
            return gamedomain+"/27slot/?gameid="+game_id+"&token="+testtoken+game_id+otherlink
        elif 2800 <= intgameid and 2804 >= intgameid:
            return gamedomain+"/28fruit/?gameid="+game_id+"&token="+testtoken+game_id+otherlink
        elif 2900 <= intgameid and 2902 >= intgameid:
            return gamedomain+"/29grid/?gameid="+game_id+"&token="+testtoken+game_id+otherlink
        elif 3000 <= intgameid and 3002 >= intgameid:
            return gamedomain+"/30slot/?gameid="+game_id+"&token="+testtoken+game_id+otherlink
        elif 3100 <= intgameid and 3102 >= intgameid:
            return gamedomain+"/31slot/?gameid="+game_id+"&token="+testtoken+game_id+otherlink
        elif 3200 <= intgameid and 3202 >= intgameid:
            return gamedomain+"/32slot/?gameid="+game_id+"&token="+testtoken+game_id+otherlink
        elif intgameid in frameworkslot:
            return gamedomain+"/framework/?gameid="+game_id+"&token="+testtoken+game_id+otherlink 
        elif intgameid == 3700 :
            return gamedomain+"/37slot/?gameid="+game_id+"&token="+testtoken+game_id+otherlink
        else:
            return None

#staging / prod 走這裡
    def verified_gamelink(self, game_id, gamedomain):

        driver = self.driver
        currentPageUrl = driver.current_url
        #現在的網址命名變數

        gamelink = currentPageUrl.split('&token=')[0]
        #取token之前的網址
        
        gameexpecturl = getgameinfo.get_gameurln(self, game_id, gamedomain)
        
        assert gamelink == gameexpecturl, "当前遊戲网址非预期！"
        #驗證網址是否正確

        return gamelink

    # demo用   
    def get_demotoken(self, game_id):

        driver = self.driver
        currentPageUrl = driver.current_url
        # 現在的網址命名變數

        urltoken = currentPageUrl.split("&")[1]
        # 取&token整串
        
        return urltoken

    # max 狀態下spin的座標 
    def click_spin_max(spinmodule):
        if spinmodule == 'spin10':
        # 1001 電竟直版按鈕座標
            pyautogui.click(x=960, y=720)
            time.sleep(5)
        elif spinmodule == 'spinlottery':
        # 17/18 刮刮卡按鈕座標
            pyautogui.click(x=1420, y=1000)
            time.sleep(3)
            pyautogui.click(x=1420, y=1000)
            time.sleep(5)
        elif spinmodule == 'spin21':
        # 16/18/19/20/21系列 slot + fruit spin 按鈕座標
            pyautogui.click(x=1680, y=880)
            time.sleep(5)
        elif spinmodule == 'spin24':
        # 22/23/24/25/26/27系列 spin按鈕座標    
            pyautogui.click(x=1680, y=880)
            time.sleep(5)
        elif spinmodule == 'space':
        # 空白鍵spin按紐座標，2100之後有效
            pyautogui.press('space')
            time.sleep(5)
        else :
        #沒有此spin按鈕座標
            print ("找不到此spin座標")

    # max 狀態下buy free的座標        
    def click_buyfree_max(buymodule):
        if buymodule == 'buy24':
        # 24 系列購買免費遊戲按這裡
            pyautogui.click(x=230, y=540)
            time.sleep(3)
            pyautogui.click(x=1140, y=780)
            time.sleep(5)
        elif buymodule == 'buy26':
        # 26 系列購買免費遊戲按這裡 
            pyautogui.click(x=180, y=560)
            time.sleep(3)
            pyautogui.click(x=1090, y=765)
            time.sleep(5)
        elif buymodule == 'buy27':
        # 27 系列購買免費遊戲按這裡 
            pyautogui.click(x=180, y=600)
            time.sleep(3)
            pyautogui.click(x=1130, y=780)
            time.sleep(5)
        elif buymodule == 'buy29':
        # 29 系列購買免費遊戲按這裡    
            pyautogui.click(x=1130, y=790)
            time.sleep(3)
            pyautogui.click(x=1030, y=640)
            time.sleep(5)
        elif buymodule == 'buy30':
        # 30 系列購買免費遊戲按這裡  
            pyautogui.click(x=925, y=820)
            time.sleep(3)
            pyautogui.click(x=920, y=660)
            time.sleep(5)
        elif buymodule == 'buy31':
        # 31 系列購買免費遊戲按這裡  
            pyautogui.click(x=925, y=820)
            time.sleep(3)
            pyautogui.click(x=920, y=660)
            time.sleep(5)
        elif buymodule == 'buy32':
        # 32 系列購買免費遊戲按這裡  
            pyautogui.click(x=960, y=780)
            time.sleep(3)
            pyautogui.click(x=960, y=630)
            time.sleep(5)
        else :
        # 購買免費遊戲壞掉的按這裡
            print ("no this function")

    # 1024*768 狀態下的座標 
    def click_spin(spinmodule):
        if spinmodule == 'spin10':
        # 1001 電竟直版按鈕座標
            pyautogui.click(x=510, y=540)
            time.sleep(5)
        elif spinmodule == 'spinlottery':
        # 17/18 刮刮卡按鈕座標
            pyautogui.click(x=875, y=675)
            time.sleep(3)
            pyautogui.click(x=825, y=675)
            time.sleep(5)
        elif spinmodule == 'spin21':
        # 16/18/19/20/21系列 slot + fruit spin 按鈕座標
            pyautogui.click(x=900, y=590)
            time.sleep(5)
        elif spinmodule == 'spin24':
        # 22/23/24/25/26/27系列 spin按鈕座標    
            pyautogui.click(x=945, y=570)
            time.sleep(5)
        elif spinmodule == 'space':
        # 空白鍵spin按紐座標，2100之後有效
            pyautogui.press('space')
            time.sleep(5)
        else :
        #沒有此spin按鈕座標
            print ("找不到此spin座標")

    # 1024*768 狀態下的座標        
    def click_buyfree(buymodule):
        if buymodule == 'buy24':
        # 24 系列購買免費遊戲按這裡
            pyautogui.click(x=130, y=400)
            time.sleep(3)
            pyautogui.click(x=630, y=540)
            time.sleep(5)
        elif buymodule == 'buy27':
        # 26 / 27 系列購買免費遊戲按這裡 
            pyautogui.click(x=140, y=440)
            time.sleep(3)
            pyautogui.click(x=605, y=540)
            time.sleep(5)
        elif buymodule == 'buy29':
        # 29 系列購買免費遊戲按這裡    
            pyautogui.click(x=640, y=575)
            time.sleep(3)
            pyautogui.click(x=580, y=470)
            time.sleep(5)
        elif buymodule == 'buy30':
        # 30 系列購買免費遊戲按這裡  
            pyautogui.click(x=510, y=590)
            time.sleep(3)
            pyautogui.click(x=510, y=480)
            time.sleep(5)
        elif buymodule == 'buy31':
        # 31 系列購買免費遊戲按這裡  
            pyautogui.click(x=510, y=590)
            time.sleep(3)
            pyautogui.click(x=525, y=515)
            time.sleep(5)
        elif buymodule == 'buy32':
        # 32 系列購買免費遊戲按這裡  
            pyautogui.click(x=510, y=580)
            time.sleep(3)
            pyautogui.click(x=510, y=480)
            time.sleep(5)
        elif buymodule == 'buy33':
        # 33 系列購買免費遊戲按這裡  
            pyautogui.click(x=510, y=580)
            time.sleep(3)
        # 舊版位置    
        #    pyautogui.click(x=510, y=510)
        #    time.sleep(5)
        # 新版位置
            pyautogui.click(x=510, y=450)
            time.sleep(5)
        elif buymodule == 'buy34':
        # 34 系列購買免費遊戲按這裡  
            pyautogui.click(x=510, y=580)
            time.sleep(3)
        #舊版位置
        #    pyautogui.click(x=580, y=430)
        #    time.sleep(5)
        #新版位置
            pyautogui.click(x=580, y=365)
            time.sleep(5)
        elif buymodule == 'buy35':
            pyautogui.click(x=510, y=580)
            time.sleep(3)
            pyautogui.click(x=575, y=385)
            time.sleep(5)

        else :
        # 購買免費遊戲壞掉的按這裡
            print ("no this function")
           

if __name__ == '__main__':
    p1601name = getgameinfo.get_gamename("1601", "en")
    p3700name = getgameinfo.get_gamename("3700", "en")
    print(p1601name)
    print(p3700name)
    p1601bet = getgameinfo.get_gametotalbet("1601")
    p3500bet = getgameinfo.get_gametotalbet("3500")
    print(p1601bet)
    print(p3500bet)
    p2400buy = getgameinfo.get_gamebuyfree("2400")
    p3500buy = getgameinfo.get_gamebuyfree("3500")
    print(p2400buy)
    print(p3500buy)
    # getgameinfo.click_buyfree('buy31')
    # getgameinfo.click_buyfree('buy32')