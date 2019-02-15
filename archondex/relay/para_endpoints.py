import requests
import os

apikey = os.environ['PARA_APIKEY']

h = {'API-KEY' : apikey}

base_url = "http://api.paradex.io/api/v1/"

def ticker():
    endpoint = "ticker"

    r = requests.get(base_url + endpoint)
    tickers = r.json()
    for t in tickers:
        v = t["baseVolume24"]
        print (t)

def nonce():
    r = requests.get(base_url + "nonce",headers=h)
    print (r.text)

def markets():
    r = requests.get(base_url + "markets",headers=h)
    print (r.text)

def bal():
    #r = requests.post(base_url + "/v1/get_balances",params={},headers=h)
    #v0??
    r = requests.post(base_url + "/v0/balances",{},headers=h)
    print (r.text)
    
if __name__=='__main__':    
    #markets()
    bal()