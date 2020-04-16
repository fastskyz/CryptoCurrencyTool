# Crypto Currency Tool
A tool for doing all sorts of things regarding cryptocurrencies. \
Just for fun!

* Python 3
* Requests

### Example usage:
```python
from api import CoinMarketCap
from traders import Binance

coin_api_key = 'xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx'

binance_api_key = 'your-binace-api-key'
binance_private_key = 'your-binace-secret-key'

api = CoinMarketCap(coin_api_key, start=1, limit=10)

btc_pricing = api.getLatestPricingBySymbol("BTC", true)
btc_price = round(btc_pricing['price'], 2)

trader = Binance(binance_api_key, binance_private_key)
trader.testConnection()
trader.testOrder("BTCEUR", "BUY", btc_price, 0.0016)
```

__This code is not tested and I do not guarantee it works. Use at your own risk!__
