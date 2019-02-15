"""
utility to analyse maker-transactions on 0x
"""

from radar_api import *
from binance_utils import *
import requests
import json
from web3 import Web3, HTTPProvider
import datetime

privateKey = os.environ['PRIVATEKEY']
INFURA_KEY = os.environ['INFURA_KEY']

w3 = Web3(HTTPProvider("https://mainnet.infura.io/" + INFURA_KEY))
acct = w3.eth.account.privateKeyToAccount(privateKey)
myaddr = (acct.address).lower()
#print (myaddr)

tokens = {"0x1985365e9f78359a9b6ad760e32412f4a445e862":"REP",
"0x0d8775f648430679a709e98d2b0cb6250d2887ef":"BAT",
"0x0f5d2fb29fb7d3cfee444a200298f468908cc942":"MANA",
"0xa4e8c3ec456107ea67d3075bf9e3df3a75823db0":"LOOM",
"0x0abdace70d3790235af448c88547603b945604ea":"DNT",
"0x41e5560054824ea6b0732e656e3ad64e20e94e45":"CVC"}

def get_ethusd_map():
    """ get candle and convert to dict of daily prices """ 
    ethusdt = get_ethusdt()
    d = {}
    for x in ethusdt[-10:]:
        ts = x[0]
        binance_ts = datetime.datetime.strftime(ts,'%Y-%m-%d')
        d[binance_ts] = float(x[4])
    d["2019-02-12"] = 120.55
    print (d)
    return d

def show_maker_fills():
    print ('volume maker analysis for ' + myaddr)
    eth_usd_map = get_ethusd_map()
    
    fills = get_fills(address = myaddr)
    maker_fills = list(filter(lambda x: x["makerAddress"]==myaddr,fills))
    
    #print ("*** date\tusd_volume \t eth_usd\t eth_volume\t volume\t filltype \t symbol***")
    print ("*** date\tusd_volume \tfilltype \t symbol***")
    total_usd = 0
    for fill in maker_fills[:]:
        fill_type = fill["type"]
        #print (fill)
        t = fill["timestamp"]
        bt = fill["baseTokenAddress"]
        sym = tokens[bt]
        ts = datetime.datetime.utcfromtimestamp(t)
        tsfd = datetime.datetime.strftime(ts,'%Y-%m-%d')
        #print (tsfd)
        eth_usd = eth_usd_map[tsfd]
        #print (fill)
        eth_volume = float(fill["filledQuoteTokenAmount"])
        v = float(fill["filledBaseTokenAmount"])
        usd_volume = eth_usd * eth_volume
        #print (tsfd,"\t",v,"\t",eth_usd,"\t",round(eth_volume,3),"\t",round(usd_volume,2),"\t",fill_type,"\t",sym)
        print (tsfd,"\t",round(usd_volume,2),"\t",fill_type,"\t",sym)
        total_usd += usd_volume
    print ("total_usd ",round(total_usd,0))

    #print (taker_fills)
    #taker_fills = list(filter(lambda x: x["makerAddress"]!=myaddr,fills))

        
        

show_maker_fills()