"""
export PYTHONPATH=/Users/x/0x/pyexchange
export PRIVATEKEY='0x';
export INFURA_KEY='...';
"""

from radar_api import *
import requests
import json
from web3 import Web3, HTTPProvider

privateKey = os.environ['PRIVATEKEY']
INFURA_KEY = os.environ['INFURA_KEY']

w3 = Web3(HTTPProvider("https://mainnet.infura.io/" + INFURA_KEY))
acct = w3.eth.account.privateKeyToAccount(privateKey)
myaddr = (acct.address).lower()
print (myaddr)

tokens = {"0x1985365e9f78359a9b6ad760e32412f4a445e862":"REP","0x0d8775f648430679a709e98d2b0cb6250d2887ef":"BAT"}

def show_maker_fills():
    fills = get_fills(address = myaddr)
    maker_fills = list(filter(lambda x: x["makerAddress"]==myaddr,fills))
    for fill in maker_fills:
        print (fill)

def show_open_orders():
    orders = get_orders(address = myaddr)
    open_orders = list(filter(lambda x: x["state"]=='OPEN',orders))

    for o in open_orders:
        bt = o["baseTokenAddress"]
        s = tokens[bt]
        print (s,":",o["type"],o["price"])


def submit_example():
    price = 0.0008042
    qty = 10
    #pair = "REP-WETH"
    symbol = "BAT"
    order = request_order(symbol, price, qty)
    js_order = prepare_order(acct, order)    
    print ("submitting >>>> ", js_order)
    response = requests.post("https://api.radarrelay.com/v2/orders", js_order, timeout=10.0)
    #response is empty
    print (response)
        
    
    symbol = "REP"
    price = 0.09042
    qty = 1
    order = request_order(symbol, price, qty)
    js_order = prepare_order(acct, order)    
    print ("submitting >>>> ", js_order)
    response = requests.post("https://api.radarrelay.com/v2/orders", js_order, timeout=10.0)
    #response is empty
    print (response)
    
    

    
if __name__=='__main__':
    #submit_example()
    show_open_orders()
    #show_maker_fills()
