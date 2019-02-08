"""
submit order to radar with web3py and infura
"""

from zero_ex.order_utils import generate_order_hash_hex
from pymaker.zrxv2 import ZrxExchangeV2, ZrxRelayerApiV2, ERC20Asset
import requests
from pymaker.sign import eth_sign, to_vrs
from pymaker.util import bytes_to_hexstring, hexstring_to_bytes, http_response_summary
from web3 import Web3, HTTPProvider
from solc import compile_source
from eth_account.messages import defunct_hash_message
from pymaker import Wad, Address
#from eth_account import Account

import os
import copy
import json

privateKey = os.environ['PRIVATEKEY']
INFURA_KEY = os.environ['INFURA_KEY']

w3 = Web3(HTTPProvider("https://mainnet.infura.io/" + INFURA_KEY))
acct = w3.eth.account.privateKeyToAccount(privateKey)

base_url = "https://api.radarrelay.com/v2/"

exchangeAddress = "0x4f833a24e1f95d70f028921e27040ca56e09ab0b"

def request_order():
  import time
  day = 24*60*60
  exp = str(int(time.time()+day))
  r = requests.post(base_url + "markets/REP-WETH/order/limit", json = {"type": "BUY","quantity": "1","price": "0.055","expiration": exp})
  order = r.json()
  print (order)
  myaddr = (acct.address).lower()
  order["makerAddress"] = myaddr
  #print ("order ",order)
  return order

def signature_order(order):  
    print (order['makerAssetData'])
    print (order['takerAssetData'])
    #order['makerAssetData'] = hexstring_to_bytes(order['makerAssetData'])
    #order['takerAssetData'] = hexstring_to_bytes(order['takerAssetData'])
    order['makerAssetData'] = hexstring_to_bytes("0xf47261b0000000000000000000000000c02aaa39b223fe8d0a0e5c4f27ead9083c756cc2")
    order["takerAssetData"] = hexstring_to_bytes("0xf47261b00000000000000000000000001985365e9f78359a9b6ad760e32412f4a445e862")
    exchangeAddress = order["exchangeAddress"]
    #order['makerAssetData'] = order['makerAssetData'].to_bytes(1, byteorder='big') * 20

    order_hash = "0x" + generate_order_hash_hex(order, exchangeAddress)
    print ("order_hash ",order_hash)
    orderhash_bytes = hexstring_to_bytes(order_hash)
    msg = orderhash_bytes
    message_hash = defunct_hash_message(primitive=msg)
    sighex = acct.signHash(message_hash).signature.hex()
    v, r, s = to_vrs(sighex)
    #signed_order = copy.copy(order)
    #print (signed_order)
    osig = bytes_to_hexstring(bytes([v])) + \
                              bytes_to_hexstring(r)[2:] + \
                              bytes_to_hexstring(s)[2:] + \
                              "03"  # EthSign
    print ("sig ",osig)                              
    return osig  

def sign_order(order):
    #self.get_order_hash(order)
    #exchange_address=exchangeAddress
    exchangeAddress = order["exchangeAddress"]
    order_hash = "0x" + generate_order_hash_hex(order, exchange_address)
    #print ("order_hash ",order_hash)
    orderhash_bytes = hexstring_to_bytes(order_hash)
    msg = orderhash_bytes
    message_hash = defunct_hash_message(primitive=msg)
    sighex = acct.signHash(message_hash).signature.hex()
    v, r, s = to_vrs(sighex)
    #signed_order = copy.copy(order)
    #print (signed_order)
    osig = bytes_to_hexstring(bytes([v])) + \
                              bytes_to_hexstring(r)[2:] + \
                              bytes_to_hexstring(s)[2:] + \
                              "03"  # EthSign
    #print (osig)
    order["signature"] = osig
    return order
    

def submit_order():
  order = request_order()
  order['makerAddress'] = myaddr.lower()
  #TODO fix
  order['makerAssetData'] = (0).to_bytes(1, byteorder='big') * 20
  order['takerAssetData'] = (0).to_bytes(1, byteorder='big') * 20
  order = sign_order(order)
  order_json = order_to_json(order)
  print (order_json)
  response = requests.post("https://api.radarrelay.com/v2/order", order_json, timeout=10.0)
  print (response)
  # ERROR
  #  {"code":100,"reason":"Validation failed","validationErrors":
  # [{"field":"makerAssetData","code":1001,"reason":"Incorrect format (Invalid value)"},
  # {"field":"takerAssetData","code":1001,"reason":"Incorrect format (Invalid value)"}]}

def try_submit():    
    #maker_create()
    order = request_order()
    
    sig = signature_order(order)
    order["signature"] = sig
    print (order)
    print ("signature ",sig)
    response = requests.post("https://api.radarrelay.com/v2/orders", order, timeout=10.0)
    print (response.text)
    

if __name__=='__main__':
    try_submit()





