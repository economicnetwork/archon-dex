"""
aggressive market-maker

"""

import archondex.relay.radar_public_api as radar_public
import archondex.relay.radar as radar
import archondex.binance_avg as binance
from archondex.ethplorer import get_balance

from archondex.DEXbroker import DEXBroker
    

def book():
    print ("get book")
    pair = "REP-WETH"
    radar_public.show_orderbook(pair)

if __name__=='__main__':
    broker = DEXBroker()
    
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("action")
    args = parser.parse_args()
    print(args.action)
    if args.action == "openorders":
        broker.show_open_orders()
    elif args.action == "balances":
        broker.show_balance()
    elif args.action == "buy":
        broker.submit_all_buy()
    elif args.action == "volume":
        #TODO
        pass
    else:
        parser.print_help()
    
    