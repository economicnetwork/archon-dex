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
        balances[s] = b
    
    return balances

