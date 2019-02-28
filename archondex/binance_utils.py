import archon.broker as broker
import archon.exchange.exchanges as exc
import archon.model.models as models

a = broker.Broker()
a.set_keys_exchange_file()
client = a.afacade.get_client(exc.BINANCE)

def get_ethusdt():
    """ get daily candles and append last price as current day """
    market = models.market_from("ETH","USDT")
    x = a.afacade.get_candles_daily(market,exc.BINANCE)
    y = a.afacade.get_candles_minute(market,exc.BINANCE)
    x.append(y[-1])
    return x
    
