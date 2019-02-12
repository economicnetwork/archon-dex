import archon.broker as broker
import archon.exchange.exchanges as exc
import archon.model.models as models
from archon.util import *

a = broker.Broker()
a.set_keys_exchange_file()
client = a.afacade.get_client(exc.BINANCE)

def get_ethusdt():
    market = models.market_from("ETH","USDT")
    x = a.afacade.get_candles_daily(market,exc.BINANCE)
    return x
    
