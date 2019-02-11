"""
export PYTHONPATH=/Users/x/0x/pymaker:/Users/x/0x/pyexchange
export PRIVATEKEY='0x';
export INFURA_KEY='...';
"""

from radar_api import *
import requests

def submit_example():
    price = 0.0008
    qty = 10
    #pair = "REP-WETH"
    symbol = "BAT"
    order = request_order(symbol, price, qty)
    js_order = prepare_order(order)    
    print ("submitting >>>> ", js_order)
    response = requests.post("https://api.radarrelay.com/v2/orders", js_order, timeout=10.0)
    #response is empty
    print (response)

    symbol = "REP"
    price = 0.08
    qty = 1
    order = request_order(symbol, price, qty)
    js_order = prepare_order(order)    
    print ("submitting >>>> ", js_order)
    response = requests.post("https://api.radarrelay.com/v2/orders", js_order, timeout=10.0)
    #response is empty
    print (response)
    

    
if __name__=='__main__':
    submit_example()
