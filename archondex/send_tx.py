""" 
basic send example
export INFURA_APIKEY="8b..."
"""

from eth_account import Account
from web3 import Web3, HTTPProvider
from solc import compile_source
from pymaker.sign import eth_sign, to_vrs
from pymaker.util import bytes_to_hexstring, hexstring_to_bytes, http_response_summary
import os

privateKey = os.environ['PRIVATEKEY']
apikey = os.environ['INFURA_APIKEY']

w3 = Web3(HTTPProvider("https://mainnet.infura.io/" + apikey))
acct = w3.eth.account.privateKeyToAccount(privateKey)

myaddr = acct.address

val = w3.toWei('0.0001', 'ether') #w3.toWei(0.5,'ether')
print (val)

signed_txn = w3.eth.account.signTransaction(dict(
    nonce=w3.eth.getTransactionCount(myaddr),
    gasPrice = w3.eth.gasPrice, 
    gas = 200000,
    to=myaddr,
    value=val
  ),
  privateKey)

print (myaddr)
print (signed_txn)

#w3.eth.sendRawTransaction(signed_txn.rawTransaction)
