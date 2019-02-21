"""
0x marketmaker
basic functions. the Marketmaker should be subclassed to perform strategy functions

"""

import archondex.relay.radar_public_api as radar_public
import archondex.relay.radar as radar
import archondex.binance_avg as binance
from archondex.ethplorer import get_balance
from tokens import *
from config_assets import asset_syms

import requests
import json
from web3 import Web3, HTTPProvider
import pymongo
import os


class Marketmaker:

    def __init__(self):
        privateKey = os.environ['PRIVATEKEY']
        INFURA_KEY = os.environ['INFURA_KEY']

        self.w3 = Web3(HTTPProvider("https://mainnet.infura.io/" + INFURA_KEY))
        self.acct = self.w3.eth.account.privateKeyToAccount(privateKey)
        self.myaddr = (self.acct.address).lower()
        print (self.myaddr)

    def submit_order(self, order): 
        print ("submit order ",order)
        [otype, symbol, price, qty] = order
        order = radar.request_order(otype, symbol, price, qty)
        js_order = radar.prepare_order(self.acct, order)    
        print ("submitting >>>> ", js_order)
        response = requests.post("https://api.radarrelay.com/v2/orders", js_order, timeout=10.0)
        #response is empty
        print (response)
        
    def show_maker_fills(self):
        fills = radar.get_fills(address = self.myaddr)
        maker_fills = list(filter(lambda x: x["makerAddress"]==self.myaddr,fills))
        for fill in maker_fills:
            print (fill)
    
    def show_bal(self):
        bal = get_balance(self.myaddr)        
        for k,v in bal.items():
            print (k,":",v)         

    def show_open_orders(self):
        print ("show_open_orders")
        orders = radar.get_orders(address = self.myaddr)
        #print (orders)
        open_orders = list(filter(lambda x: x["state"]=='OPEN',orders))
        #print (open_orders)
        print ('symbol\ttype\tprice\tquantity')
        for o in open_orders:
            #veth = o["remainingQuoteTokenAmount"]
            bt = o["baseTokenAddress"]
            s = tokens[bt]
            qty = round(float(o["remainingBaseTokenAmount"]),0)
            p = round(float(o["price"]),6)
            #print (o)
            print (s," ",o["type"],p," ",qty) #," ",veth)                  


