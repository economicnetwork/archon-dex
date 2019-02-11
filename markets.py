"""
"""

from radar_public_api import *

markets = get_markets()
print (len(markets))
for m in markets[:]:
    #print (m)
    mid = m["id"]
    stats(mid)

#market_ticker()
#stats()