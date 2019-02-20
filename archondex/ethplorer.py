import requests
import json

ethplorer = "http://api.ethplorer.io"

def get_balance(address):    
    url = "%s/getAddressInfo/%s?apiKey=freekey"%(ethplorer,address)
    r = requests.get(url)
    j = json.loads(r.text)
    tokens = j["tokens"]

    balances = {}
    for t in tokens:
        s = t["tokenInfo"]["symbol"]
        b = float(t["balance"])/10**18

        #TODO more generic
        if s == "USDC" or s == "CVC":
            balances[s] = b*10**12
        else:
            balances[s] = b
    
    return balances

