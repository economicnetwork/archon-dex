"""
submit order to radar with web3py and infura
"""

from zero_ex.order_utils import generate_order_hash_hex, Order, jsdict_order_to_struct, order_to_jsdict
from zero_ex.order_utils.asset_data_utils import encode_erc20_asset_data
from pymaker.zrxv2 import ZrxExchangeV2, ZrxRelayerApiV2, ERC20Asset
import requests
from typing import cast, Dict, NamedTuple, Tuple
from pymaker.sign import eth_sign, to_vrs
from pymaker.util import bytes_to_hexstring, hexstring_to_bytes, http_response_summary
from web3 import Web3, HTTPProvider
from solc import compile_source
from eth_account.messages import defunct_hash_message
from pymaker import Wad, Address
from zero_ex.order_utils import asset_data_utils as adu
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

def sign_order(order):
    order_hash = "0x" + generate_order_hash_hex(order, exchangeAddress)
    print ("order_hash ",order_hash)
    orderhash_bytes = hexstring_to_bytes(order_hash)
    msg = orderhash_bytes
    message_hash = defunct_hash_message(primitive=msg)
    sighex = acct.signHash(message_hash).signature.hex()
    v, r, s = to_vrs(sighex)
    osig = bytes_to_hexstring(bytes([v])) + \
                              bytes_to_hexstring(r)[2:] + \
                              bytes_to_hexstring(s)[2:] + \
                              "03"  # EthSign
    print ("sig ",osig)                              
    return osig  


def submit_order():
  order = request_order()
  order['makerAddress'] = myaddr.lower()
  #sig = signature_order(order)
  order = sign_order(order)
  #order_json = order_to_json(order)
  print ("submitting !!! >>>>>> ", order_json)
  response = requests.post("https://api.radarrelay.com/v2/order", order_json, timeout=10.0)
  print (response)
  # ERROR
  #  {"code":100,"reason":"Validation failed","validationErrors":
  # [{"field":"makerAssetData","code":1001,"reason":"Incorrect format (Invalid value)"},
  # {"field":"takerAssetData","code":1001,"reason":"Incorrect format (Invalid value)"}]}
    
def submit_example():    
    example_order = {
             'makerAddress': "0x0000000000000000000000000000000000000000",
             'takerAddress': "0x0000000000000000000000000000000000000000",
             'feeRecipientAddress': "0x0000000000000000000000000000000000000000",
             'senderAddress': "0x0000000000000000000000000000000000000000",
             'makerAssetAmount': 1000000000000000000,
             'takerAssetAmount': 1000000000000000000,
             'makerFee': 0,
             'takerFee': 0,
             'expirationTimeSeconds': 12345,
             'salt': 12345,
             'makerAssetData': "0x0000000000000000000000000000000000000000",
             'takerAssetData': "0x0000000000000000000000000000000000000000",
             'exchangeAddress': "0x0000000000000000000000000000000000000000",
    }
    print (example_order)
    order_struct = jsdict_order_to_struct(example_order)    
    sig = sign_order(order_struct)
    js_order["signature"] = sig
    js_order = order_to_jsdict(order)
    print (js_order)
    #jsdict["makerAssetData"] = "0x" + order["makerAssetData"].hex()

if __name__=='__main__':
    #request_order()
    submit_example()

