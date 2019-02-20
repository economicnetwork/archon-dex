"""
radar public API
"""
import requests

base_url = "https://api.radarrelay.com/v2/"
  
def get_markets():
    r = requests.get(base_url + "markets")
    markets = r.json()
    return markets    

def market_ticker():
    pair = "ZRX-WETH"
    endpoint = "markets/%s/ticker"%pair
    r = requests.get(base_url + endpoint)
    ticker = r.json()
    print (ticker)

def orderbook(pair): 
    endpoint = "markets/%s/book"%pair
    r = requests.get(base_url + endpoint)
    book = r.json()
    return book
    
def show_orderbook(pair):  
    book = orderbook(pair)
    bids,asks = book["bids"],book["asks"]
    print ("orderbook %s "%pair)
    for b in bids:
        print (b['price'])
    print ('****')
    for a in asks:
        print (a['price'])

def stats(pair):    
    #pair = "ZRX-WETH"
    page=str(2)
    #endpoint = "markets/%s/stats&page=%s"%(pair,page)
    endpoint = "markets/%s/stats"%(pair)
    #print (endpoint)
    r = requests.get(base_url + endpoint)
    ticker = r.json()
    #print (ticker)
    v = ticker["volume24Hour"]
    print ("%s volume %s"%(pair,v))

