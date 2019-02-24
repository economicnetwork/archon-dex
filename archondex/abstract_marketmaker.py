"""
0x marketmaker
basic functions. the Marketmaker should be subclassed to perform strategy functions

"""

import archondex.relay.radar_public_api as radar_public
import archondex.relay.radar as radar
import archondex.binance_avg as binance
from archondex.ethplorer import get_balance
from archondex.tokens import *
from archondex.config_assets import asset_syms

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
        print ("using address ",self.myaddr)

        self.open_orders = list()
        self.balances = None

    def submit_order(self, order): 
        print ("submit order ",order)
        [otype, symbol, price, qty] = order
        response = radar.submit_order(self.acct, order)
        print (response)

    def submit_buy(self, symbol, pair, target_price, qty):
        otype = "BUY"
        order = [otype, symbol, target_price, qty]
        print (order)
        self.submit_order(order)

    def submit_sell(self, symbol, pair, target_price, qty):
        otype = "SELL"
        order = [otype, symbol, target_price, qty]
        print (order)
        self.submit_order(order)


    def submit_buy_band(self, symbol, pair, zq, bin_avg_price, binance_band, target_bal_eth, max_bal = 1.0):
        """ submit bid based on midprice, but check band on CEX (binance) in case midprice is out of place """
        print ("submit_buy")

        sym_bal = self.balances[symbol]
        
        #from midprice        
        
        book = radar_public.orderbook(pair)
        topbid = float(book["bids"][0]['price'])
        topask = float(book["asks"][0]['price'])
        midprice = (topbid+topask)/2
        print ("best bid",topbid)
        print ("best ask", topask)
        print ("midprice ",midprice)

        eth_bal = sym_bal * bin_avg_price
        print ("balance ",symbol,sym_bal,"  ",eth_bal)

        
        if eth_bal > max_bal:
            print ("high inventory. don't submit")
            return
        
        #pip = 0.000001
        #target_price = topask - pip
        
        target_price = midprice * (1 - zq)
        from_bin = target_price/bin_avg_price -1
        print ("binance avg ",symbol,":",bin_avg_price)
        print ("midrice ",midprice)
        print (" >> target: ",target_price)
        if from_bin > binance_band:
            print ("bid too high")
            newzq = 0.1
            #target_price = bin_avg_price * (1 - zq)
            #print ("new ",target_price)

        elif from_bin < -binance_band:
            print ("bid too low from binance. midprice not indicative",from_bin)
            #target now 
            #newzq = 0.1
            #target_price = bin_avg_price * (1 - newzq)
            #print ("new ",target_price)

        else:
            #print ("from_bin ",from_bin)
            #avg_price * (1-zq)
            
            qty = round(target_bal_eth/target_price,0)
            otype = "BUY"
            order = [otype, symbol, target_price, qty]
            print (order)
            #self.submit_order(order)

    def submit_sell_band(self, symbol, pair, zq, bin_avg_price, binance_band):
        """ submit ask based on midprice, but check band on CEX (binance) in case midprice is out of place """
        print ("submit sell")

        sym_bal = self.balances[symbol]
        
        #from midprice        
        
        book = radar_public.orderbook(pair)
        topbid = float(book["bids"][0]['price'])
        topask = float(book["asks"][0]['price'])
        midprice = (topbid+topask)/2
        print ("best bid",topbid)
        print ("best ask", topask)
        print ("midprice ",midprice)

        eth_bal = sym_bal * bin_avg_price
        print ("balance ",symbol,sym_bal,"  ",eth_bal)

        #pip = 0.000001
        #target_price = topask - pip
        
        target_price = midprice * (1 + zq)
        from_bin = target_price/bin_avg_price -1
        print ("binance avg ",symbol,":",bin_avg_price)
        print ("midrice ",midprice)
        print (" >> target: ",target_price)
        if from_bin > binance_band:
            print ("bid too high")
            target_price = bin_avg_price * (1 + zq)
            qty = (1 - 0.01) * sym_bal
            otype = "SELL"
            order = [otype, symbol, target_price, qty]
            print (order)
            self.submit_order(order)            

        elif from_bin < -binance_band:
            print ("bid too low from binance. midprice not indicative",from_bin)
            target_price = bin_avg_price * (1 + zq)
            qty = (1 - 0.01) * sym_bal
            otype = "SELL"
            order = [otype, symbol, target_price, qty]
            print (order)
            self.submit_order(order)            

        else:
            #print ("from_bin ",from_bin)
            #avg_price * (1-zq)
            
            qty = sym_bal
            otype = "SELL"
            order = [otype, symbol, target_price, qty]
            print (order)
            self.submit_order(order)            

        
    def show_maker_fills(self):
        fills = radar.get_fills(address = self.myaddr)
        maker_fills = list(filter(lambda x: x["makerAddress"]==self.myaddr,fills))
        for fill in maker_fills:
            print (fill)
    
    def fetch_balances(self):
        self.balances = get_balance(self.myaddr)        

    def fetch_order(self):
        orders = radar.get_orders(address = self.myaddr)
        #print (orders)
        self.open_orders = list(filter(lambda x: x["state"]=='OPEN',orders))
         

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


