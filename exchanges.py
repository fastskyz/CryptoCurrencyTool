import json, time
import hmac, hashlib
from requests import Request, Session, get
import urllib

class Binance():
	def __init__(self, api_key, secret_key):
		self.api_key = api_key
		self.secret_key = secret_key
		self.base_url = 'https://api.binance.com'

		self.headers = {
			'Accepts': 'application/json',
			'X-MBX-APIKEY': api_key,
		}

		self.current_milli_time = lambda: int(round(time.time() * 1000))

		self.connection_status = None


	def signedRequest(self, url, params, headers, request_type='GET'):
		url_params = urllib.parse.urlencode(params).encode('utf-8')
		signature = hmac.new(self.secret_key.encode('utf-8'), url_params, hashlib.sha256).hexdigest()

		signed_params = params['signature'] = signature

		return Request(request_type, url, params=params, headers=headers).prepare()

	def getBookBySymbol(self, symbol):
		params = {'symbol': symbol}
		response = get(f'{self.base_url}/api/v3/ticker/bookTicker', params=params, headers=self.headers)
		return json.loads(response.text)

	def testConnection(self):
		test_url = f'{self.base_url}/api/v3/ping'
		response = get(test_url)
		if response.status_code == 200:
			self.connection_status = True
			print('Connection to Binance established!')
		else:
			self.connection_status = False
			print('Connecting to Binance failed!')


	def testOrder(self, symbol, side, quantity, price):
		url = f'{self.base_url}/api/v3/order/test'

		params = {
			'symbol': symbol,
			'side': side,
			'type': 'limit',
			'timeInForce': 'GTC',
			'quantity': quantity,
			'price': price,
			'recvWindow': 5000,
			'timestamp': self.current_milli_time(),
		}

		s = Session()
		p = self.signedRequest(url, params, self.headers, 'POST')
		response = s.send(p)
		print(response.text)

