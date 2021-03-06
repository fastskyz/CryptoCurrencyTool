import requests, json
from datetime import date

class CoinMarketCap():
	def __init__(self, api_key, start=1, limit=5000, convert='EUR', price_min=1, price_max=100000):
		self.api_key = api_key
		self.start = start
		self.limit = limit
		self.convert = convert
		self.price_min = price_min
		self.price_max = price_max

		self.headers = {
			'Accepts': 'application/json',
			'X-CMC_PRO_API_KEY': api_key
		}

		self.parameters = {
			'start': f'{start}',
			'limit': f'{limit}',
			'convert': f'{convert}',
			'price_min': f'{price_min}',
			'price_max': f'{price_max}',
		}

		self.url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'

		self.history = []

	def refreshPricing(self):
		response = requests.get(self.url, self.parameters, headers=self.headers)
		
		latest_data = json.loads(response.text)
		self.history.append(latest_data)

		with open(f'prices/history_{date.today().strftime("%d-%m-%Y")}_{self.convert}_{self.start}_{self.limit}.txt', 'w') as file:
			file.write(json.dumps(self.history))

		print('Done! Data saved and loaded as most recent data.\n')

	def getFullHistory(self):
		return self.history

	def getLatestData(self, refresh=False):
		if refresh:
			self.refreshPricing()
		return self.history[-1]['data']

	def getLatestDataBySymbol(self, symbol, refresh=False):
		if refresh:
			self.refreshPricing()

		for coin in self.getLatestData():
			if coin['symbol'] == symbol:
				return coin

	def getLatestPriceBySymbol(self, symbol, refresh=False):
		coin = self.getLatestDataBySymbol(symbol=symbol, refresh=refresh)
		if coin:
			return coin['quote'][self.convert]['price']
		else:
			print('No matching coin found!')

	def loadHistoryFromFile(self, file, getLatest=False):
		try:
			with open(f'prices/{file}', 'r') as f:
				self.history = json.loads(f.read())
		except IOError:
			print(f"File {file} seems inaccessible!")

		if getLatest:
			this.refreshPricing()
			print(f'Done! Loaded history from {file} and refreshed latest data from api.')
		else:
			print(f'Done! Loaded history from {file}.')

		print(f'Size of history is {len(self.history)}')

