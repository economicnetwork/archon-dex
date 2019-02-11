"""
TODO
cancel
get-orderbook

export PRIVATEKEY=""
export INFURA_KEY=""
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

import os
import copy
import json
import time

privateKey = os.environ['PRIVATEKEY']
INFURA_KEY = os.environ['INFURA_KEY']

w3 = Web3(HTTPProvider("https://mainnet.infura.io/" + INFURA_KEY))
acct = w3.eth.account.privateKeyToAccount(privateKey)

base_url = "https://api.radarrelay.com/v2/"

exchangeAddress = "0x4f833a24e1f95d70f028921e27040ca56e09ab0b"

def request_order(symbol, price, qty):  
  day = 24*60*60
  exp = str(int(time.time()+day))
  
  #TODO rounding
  order_data = {"type": "BUY","quantity": str(qty), "price": str(price),"expiration": exp}  
  base = "WETH"
  pair = symbol + "-" + base
  r = requests.post(base_url + "markets/" + pair + "/order/limit", json = order_data)
  order = r.json()  
  return order

def sign_order(order):
    """ create order hash and sign it """
    order_hash = "0x" + generate_order_hash_hex(order, exchangeAddress)
    orderhash_bytes = hexstring_to_bytes(order_hash)
    msg = orderhash_bytes
    message_hash = defunct_hash_message(primitive=msg)
    sighex = acct.signHash(message_hash).signature.hex()
    v, r, s = to_vrs(sighex)
    osig = bytes_to_hexstring(bytes([v])) + \
                              bytes_to_hexstring(r)[2:] + \
                              bytes_to_hexstring(s)[2:] + \
                              "03"  # EthSign
    return osig  

def prepare_order(order):
    """ prepare the order for submit """
    myaddr = (acct.address).lower()
    order["makerAddress"] = myaddr
    order_struct = jsdict_order_to_struct(order)    
    sig = sign_order(order_struct)
    order_struct["signature"] = sig
    js_order = order_to_jsdict(order_struct)
    js_order["exchangeAddress"] = exchangeAddress
    return js_order

