"""
tokenmom API client
API docs https://docs.tokenmom.com
"""

import requests

base_url = "https://api.tokenmom.com/"
  
def markets():
    r = requests.get(base_url + "market/get_markets")
    j = r.json()
    markets = j["markets"]
    for m in markets[:]:
        base = m["base_token"]
        #print (m.keys())
        tokens = m["tokens"]
        print (base,":",len(tokens))
        #for t in tokens[:1]:
        #    print (t)

def list_market():    
    pair = "TM-WETH"
    endpoint = "market/get_markets?market_id=" + pair
    r = requests.get(base_url + endpoint)
    j = r.json()
    print (j)

def list_tickers():
    endpoint = "market/get_tickers"
    r = requests.get(base_url + endpoint)
    j = r.json()
    tickers = j["tickers"]
    for t in tickers:
        v = float(t['volume'])
        if v > 0:
            p = float(t["price"])
            print (p,v)
            ev = v*p
            print (t["market_id"],":",p,v)

def get_tickers():    
    pair = "TM-WETH"
    endpoint = "market/get_tickers?market_id=" + pair
    r = requests.get(base_url + endpoint)
    j = r.json()
    print (j)

def list_book(pair):    
    endpoint = "order/get_orderbook?market_id="+pair
    r = requests.get(base_url + endpoint)
    j = r.json()
    if j["status"]=='success':
        data = j["orderbook"]
        bids = data["bids"]
        asks = data["asks"]        
        key = lambda item: item["price"]
        bids = sorted(bids, key=key)
        asks = sorted(asks, key=key)
        bids.reverse()

        return [bids,asks]

def show_book():
    pair = "TM-WETH"
    [bids,asks] = list_book(pair)

    print ('** asks **')
    for a in asks:
        p,am = a["price"],a["amount"]
        print (p,am)

    print ('** bids **')
    for b in bids:
        p,am = b["price"],b["amount"]
        print (p,am)
        
def show_spread():
    pair = "TM-WETH"
    [bids,asks] = list_book(pair)
    bp,ap = float(bids[0]["price"]),float(asks[0]["price"])
    spread = (ap-bp)/ap
    print (pair,":",spread)


def post_order():
    #POST order/build_order
    pass

def trades(pair, page=0):    
    """get trades per page """
    endpoint = "market/get_trades?market_id="+pair+"&page="+str(page)
    r = requests.get(base_url + endpoint)
    trades = r.json()["trades"]
    return trades

def trades_all(pair):  
    """ get all trades """  
    trade_list = list()
    maxpage = 20
    #TODO fetch until recent day
    for page in range(0,maxpage):
        t = trades(pair, page)
        trade_list += t
    return trade_list

def trades_write():
    pair = "TM-WETH"
    trades = trades_all(pair)    
    with open('trades_' + pair + '.csv','w') as f:
        for t in trades:
            a = t["amount"]
            p = t["price"]
            u = t['updated_at']
            print (u,":",p,"  ",a)    
            f.write(str(t) + '\n')

#markets()
list_tickers()
#list_book()
#show_book()
#show_spread()
#trades_all()
#trades_write()