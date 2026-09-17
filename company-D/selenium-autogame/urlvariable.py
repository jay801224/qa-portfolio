tTag="20230322"

stagingold =  {
     "homeurl" : "http://example.internal/" ,
     "gamedomain" : "https://example.internal" ,
     "betrecordurl" : "https://example.internal" ,
     "serverurl" : "example.internal" ,
     "gameoriginalurl" : "http://example.internal/play/is_"
}

stagingnew =  {
     "homeurl" : "http://example.internal/" ,
     "gamedomain" : "https://example.internal" ,
     "betrecordurl" : "https://example.internal" ,
     "serverurl" : "example.internal" ,
     "gameoriginalurl" : "http://example.internal/id/<PRODUCT>/lobby/is_"
}

demo = {
    "homepage" : "https://example.internal" ,
    "gamedomain" : "https://example.internal" ,
    "betrecordurl" : "https://example.internal" ,
    "serverurl" : "example.internal&t="+f'{tTag}'+"&b=<ACCOUNT>", 
    "otherpara" : "&t="+f'{tTag}'+"&b=<ACCOUNT>"
    }

demotrunk = {
    "homepage" : "https://example.internal" ,
    "gamedomain" : "http://example.internal:18120" ,
    "betrecordurl" : "http://example.internal:18120" ,
    "serverurl" : "example.internal&t="+f'{tTag}'+"&b=<ACCOUNT>",
    "otherpara" : "&t="+f'{tTag}'+"&b=<ACCOUNT>"
    }

demophptrunk = {
    "homepage" : "https://example.internal" ,
    "gamedomain" : "http://example.internal:18120" ,
    "betrecordurl" : "http://example.internal:18120" ,
    "serverurl" : "example.internal"
    }
demokotrunk = {
    "homepage" : "https://example.internal" ,
    "gamedomain" : "" ,
    "betrecordurl" : "" ,
    "serverurl" : ""
    }
btocCDN = {
    "homepage" : "https://example.internal" ,
    "gamedomain" : "https://example.internal" ,
    "betrecordurl" : "https://example.internal" ,
    "serverurl" : "example.internal"
    }

btobCDN = {
    "homepage" : "https://example.internal" ,
    "gamedomain" : "https://example.internal" ,
    "betrecordurl" : "https://example.internal" ,
    "serverurl" : "example.internal"
    }

phCDN = {
    "homepage" : "https://example.internal" ,
    "gamedomain" : "http://example.internal" ,
    "betrecordurl" : "http://example.internal" ,
    "serverurl" : "example.internal"
    }

prod_account01 = {
    "homepage" : "https://example.internal/our-games" ,
    "gamedomain" : "https://example.internal" ,
    "betrecordurl" : "https://example.internal" ,
    "serverurl" : "https%3A%2F%2Fexample.internal",
    "gameoriginalurl" : "https://example.internal/play/is_"
        }
#有換cdn就要改

#跳轉前網址+遊戲ID
def get_gameoriginalurl(game_id, gameoriginalurl):
    return gameoriginalurl + game_id

def get_prodhomeurl(agent_id):
    
    urllist = [
        ["agent-01", "https://example.internal/slots/<PRODUCT>"],
        ["agent-02", "http://example.internal/home.php"],
        ["agent-03", "http://example.internal/"],
        ["agent-04", "https://example.internal/Main.aspx"],
        ["agent-05", "https://example.internal/our-games"],
        ["agent-06", "https://example.internal/id/db/slot/<PRODUCT>-<PRODUCT>"],
        ["agent-07", "https://example.internal/game/slots?category=<PRODUCT>-<PRODUCT>"],
        ["agent-08", "https://example.internal/"]
        ]

    sorted(urllist, key=lambda x:x[0])

    for (agentid, homeurl) in urllist:
        try :
            if agentid == agent_id :
                return homeurl
        except: 
            print("cannot get the agent_id and link")
            pass


if __name__ == "__main__":
    print(get_prodhomeurl('agent-06'))
