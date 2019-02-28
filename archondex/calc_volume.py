"""
utility to analyse maker-transactions on 0x
"""

import archondex.relay.radar import radar
from archondex.binance_utils import *
import requests
import json
from web3 import Web3, HTTPProvider
import datetime

privateKey = os.environ['PRIVATEKEY']
INFURA_KEY = os.environ['INFURA_KEY']

w3 = Web3(HTTPProvider("https://mainnet.infura.io/" + INFURA_KEY))
acct = w3.eth.account.privateKeyToAccount(privateKey)
myaddr = (acct.address).lower()

tokens = {
"0x1985365e9f78359a9b6ad760e32412f4a445e862":"REP",
"0x0d8775f648430679a709e98d2b0cb6250d2887ef":"BAT",
"0x0f5d2fb29fb7d3cfee444a200298f468908cc942":"MANA",
"0xa4e8c3ec456107ea67d3075bf9e3df3a75823db0":"LOOM",
"0x0abdace70d3790235af448c88547603b945604ea":"DNT",
"0x41e5560054824ea6b0732e656e3ad64e20e94e45":"CVC",
"0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48":"USDC"
}

def get_ethusd_map():
    """ get candle and convert to dict of daily prices """ 
    ethusdt = get_ethusdt()
    #print (ethusdt)
    d = {}
    for x in ethusdt[-10:]:
        ts = x[0]
        binance_ts = datetime.datetime.strftime(ts,'%Y-%m-%d')
        d[binance_ts] = float(x[4])
    return d

def get_maker_fills_volume(address):
    print ('volume maker analysis for ' + address)
    eth_usd_map = get_ethusd_map()
    
    fills = radar.get_fills(address = address)
    maker_fills = list(filter(lambda x: x["makerAddress"]==address,fills))
    print (len(maker_fills))
    
    #print ("*** date\tusd_volume \t eth_usd\t eth_volume\t volume\t filltype \t symbol***")
    #print ("*** date\tusd_volume \tfilltype \t symbol***")
    total_usd = 0
    by_date = {}
    for fill in maker_fills[:]:        
        #print (fill)
        
        fill_type = fill["type"]
        z = lambda x: "BUY" if x=="SELL" else "SELL"
        maker_type = z(fill_type)
        t = fill["timestamp"]
        bt = fill["baseTokenAddress"]
        sym = tokens[bt]
        ts = datetime.datetime.utcfromtimestamp(t)
        date_day = datetime.datetime.strftime(ts,'%Y-%m-%d')
        try:
            eth_usd = eth_usd_map[date_day]
        except:
            eth_usd = 100
        eth_volume = float(fill["filledQuoteTokenAmount"])
        v = float(fill["filledBaseTokenAmount"])
        usd_volume = eth_usd * eth_volume
        
        #print (date_day,"\t",round(usd_volume,2),"\t",maker_type,"\t",sym)
        
        total_usd += usd_volume

        if date_day in by_date.keys(): 
            #print (date_day,"\t",round(usd_volume,2),"\t",maker_type,"\t",sym)
            by_date[date_day].append(usd_volume)
        else:
            by_date[date_day] = [usd_volume]
        
    
    return by_date

def get_sum_volume_date():
    volume_by_date = get_maker_fills_volume(myaddr)
    #print (volume_by_date)
    from functools import reduce
    #print (by_date)
    total = 0
    sum_volume_by_date = {}
    print ("*** date\tusd_volume ***")
    for k,v in volume_by_date.items():
        #print (v)
        #tv = reduce((lambda x, y: x + x), v)
        sum_volume_by_date[k] = sum(v)
        #print (k,round(sum(v),2))
    return sum_volume_by_date

def show_maker_fills_volume():
    print (myaddr)
    sum_volume_by_date = get_sum_volume_date()
    total = 0
    for k,v in sum_volume_by_date.items():
        print (k,v)
        #total += v
    #print (round(total,2))    

        
if __name__=='__main__':            
    #taker_fills = list(filter(lambda x: x["makerAddress"]!=myaddr,fills))
    show_maker_fills_volume()

#fills = get_fills(address = myaddr)
#for x in fills: print(x)