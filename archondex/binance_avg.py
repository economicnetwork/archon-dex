import redis
import archon.broker as broker
import archon.exchange.exchanges as exc
import archon.exchange.binance as b
import archon.model.models as models

import numpy as np
import json

from datetime import datetime

a = broker.Broker()
a.set_keys_exchange_file()
client = a.afacade.get_client(exc.BINANCE)

import redis
r = redis.Redis(host='localhost', port=6379, db=0)

def get_average(token):
    market = models.market_from(token,"ETH")
    candles = a.afacade.get_candles_minute(market,exc.BINANCE)
    closes = [float(x[4]) for x in candles]
    avg = round(np.mean(closes),6)
    #print (closes)
    k = market + "_avg"
    print (token,":",avg)

    #return avg
    #r.set(token, json.dumps({"avg":avg}))
    r.set(token, json.dumps(avg))
    return avg

#get_average("REP")
syms = ["USDC", "TUSD", "BAT", "CVC", "DNT", "LOOM", "MANA", "REP"]
avgs = {}
for s in syms:
    try:
        avg = get_average(s)
        avgs[avg] = avg
    except:
        pass

print (avgs)