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

def get_ethusd_map():
    """ get candle and convert to dict of daily prices """ 
    ethusdt = get_ethusdt()
    d = {}
    for x in ethusdt[-10:]:
        ts = x[0]
        binance_ts = datetime.datetime.strftime(ts,'%Y-%m-%d')
        d[binance_ts] = float(x[4])
    return d

def show_maker_fills():
    print ('volume maker analysis for ' + myaddr)
    eth_usd_map = get_ethusd_map()
    
    fills = get_fills(address = myaddr)
    maker_fills = list(filter(lambda x: x["makerAddress"]==myaddr,fills))
    print ("*** date\t eth_usd\t eth_volume\t usd_volume ***")
    for fill in maker_fills[:]:
        #print (fill)
        t = fill["timestamp"]
        ts = datetime.datetime.utcfromtimestamp(t)
        tsfd = datetime.datetime.strftime(ts,'%Y-%m-%d')
        #print (tsfd)
        eth_usd = eth_usd_map[tsfd]
        eth_volume = float(fill["filledQuoteTokenAmount"])
        usd_volume = eth_usd * eth_volume
        print (tsfd,"\t",eth_usd,"\t",eth_volume,"\t",usd_volume)
        
        

show_maker_fills()