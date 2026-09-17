import requests
import time

# gsurl = "http://example.internal"
thbgsurl = "https://example.internal"
phpgsurl = "https://example.internal"
gsurl = "https://example.internal"

gameid = 3900
gamedata = {"game_id": gameid, "line_bet": 50, "line_num": 20, "coin_value": 2, "bet_credit": 2000, "buy_spin": 0}
phpgamedata = {"game_id": gameid, "line_bet": 50, "line_num": 20, "coin_value": 0.004, "bet_credit": 4, "buy_spin": 0}
thbgamedata = {"game_id": gameid, "line_bet": 25, "line_num": 20, "coin_value": 0.1, "bet_credit": 50, "buy_spin": 0}
# “<ACCOUNT>%d” % gameidnum

def requestpost (gsurl, gameid, gamedata):
    
    # spin 1次
           gamespin = requests.post(gsurl, json={"command":"spin","token":"<ACCOUNT>"+str(gameid),"data":gamedata})
           print (gamespin)
           
    # 確認 error_code 值  
           getgamespin = gamespin.json()['error_code']
           print (getgamespin)
           
           if getgamespin != 0 :
             return getgamespin
           
def requestpostmore (gsurl, gameid, gamedata, spintimes):
    
    # spin 多次
    for i in range(spintimes):
        gamespin = requests.post(gsurl, json={"command":"spin","token":"<ACCOUNT>"+str(gameid),"data":gamedata})
        time.sleep(1.2)
    
    print(gamespin.text.encode('utf8'))    
           
             
           

def tradrequest (spintimes):        
  url = "https://example.internal/"
  body = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":3900,\"line_bet\":50,\"line_num\":20,\"coin_value\":2,\"bet_credit\":2000}}"
  headers  = {
  'Host': 'example.internal',
  'Accept': '*/*',
  'Content-Type': 'text/plain;charset=UTF-8',
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36'
  }
  
  for i in range(spintimes):
    r = requests.request("POST", url, headers = headers, data = body)
    time.sleep(1.2)
    
  print(r.text.encode('utf8'))

if __name__ == "__main__":
  print("腳本開始")    
  #requestpost(gsurl, gameid, gamedata)
  requestpostmore(gsurl, gameid, thbgamedata, 1000)
  print("腳本結束")