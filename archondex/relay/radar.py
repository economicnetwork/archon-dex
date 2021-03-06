"""
radar API client
API docs https://developers.radarrelay.com/feed-api/v2/

TODO
cancel
get-orderbook

export PRIVATEKEY=""
export INFURA_KEY=""
submit order to radar with web3py and infura
"""

import os
import copy
import json
import time
import requests
from web3 import Web3, HTTPProvider
from eth_account.messages import defunct_hash_message
from eth_abi import encode_single, encode_abi, decode_single
from typing import cast, Dict, NamedTuple, Tuple

#from zero_ex.order_utils import generate_order_hash_hex, Order, jsdict_order_to_struct, order_to_jsdict
from archondex.zerox.orderutils import generate_order_hash_hex, Order, jsdict_order_to_struct, order_to_jsdict


base_url = "https://api.radarrelay.com/v2/"

exchangeAddress = "0x4f833a24e1f95d70f028921e27040ca56e09ab0b"

#public
def get_orders(address):    
    response = requests.get("%s/accounts/%s/orders"%(base_url,address))
    orders = json.loads(response.text)
    return orders

def _get_fills_page(address, page):
    params = {"perPage": 100, "page": page}
    response = requests.get("%s/accounts/%s/fills"%(base_url,address),params=params)
    #print (response.text)    
    #page perPage
    fills = json.loads(response.text)
    return fills

#public
def get_fills(address):
    fills = list()
    for i in range(0,10):
        #params = {"perPage": 100}
        fills_page = get_fills_page(address, i)
        if len(fills_page)>0:
            fills += fills_page
        else:
            break
    return fills

def bytes_to_hexstring(value) -> str:
    if isinstance(value, bytes) or isinstance(value, bytearray):
        return "0x" + "".join(map(lambda b: format(b, "02x"), value))
    elif isinstance(value, str):
        b = bytearray()
        b.extend(map(ord, value))
        return "0x" + "".join(map(lambda b: format(b, "02x"), b))
    else:
        raise AssertionError

def hexstring_to_bytes(value: str) -> bytes:
    assert(isinstance(value, str))
    assert(value.startswith("0x"))
    return Web3.toBytes(hexstr=value)


def to_vrs(signature: str) -> Tuple[int, bytes, bytes]:
    assert(isinstance(signature, str))
    assert(signature.startswith("0x"))

    signature_hex = signature[2:]
    r = bytes.fromhex(signature_hex[0:64])
    s = bytes.fromhex(signature_hex[64:128])
    v = ord(bytes.fromhex(signature_hex[128:130]))

    return v, r, s

def request_order(otype, symbol, price, qty):  
  day = 24*60*60
  exp = str(int(time.time()+day))
  
  #TODO rounding
  order_data = {"type": otype,"quantity": str(qty), "price": str(price),"expiration": exp}  
  base = "WETH"
  pair = symbol + "-" + base
  r = requests.post(base_url + "markets/" + pair + "/order/limit", json = order_data)
  order = r.json()  
  return order

def _sign_order(acct, order):
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

def prepare_order(acct, order):
    """ prepare the order for submit """
    myaddr = (acct.address).lower()
    order["makerAddress"] = myaddr
    order_struct = jsdict_order_to_struct(order)    
    sig = _sign_order(acct, order_struct)
    order_struct["signature"] = sig
    js_order = order_to_jsdict(order_struct)
    js_order["exchangeAddress"] = exchangeAddress
    return js_order

def submit_order(acct, order):
    print ("submit ",order)
    [otype, symbol, price, qty] = order
    dict_order = request_order(otype, symbol, price, qty)
    js_order = prepare_order(acct, dict_order)
    response = requests.post(base_url + "orders", js_order, timeout=10.0)
    #response is empty
    return response

"""

def cancel_order(order):
    ORDER_INFO_TYPE = '(address,address,address,address,uint256,uint256,uint256,uint256,uint256,uint256,bytes,bytes)'
    method_signature = w3.sha3(text=f"cancelOrder({ORDER_INFO_TYPE})")[0:4]
    print (method_signature)
    method_parameters = encode_single(f"({ORDER_INFO_TYPE})", [_order_tuple(order)])
    request = bytes_to_hexstring(method_signature + method_parameters)
    print (request)
"""    
