import threading, time

class Trader():
	def __init__(self, exchange, coin, trade_amount, converted_currency='EUR', check_interval=60, min_raise=4, max_drop=2):
		self.exchange = exchange

		self.coin = coin
		self.converted_currency = converted_currency
		self.trade_amount = trade_amount

		self.min_raise = min_raise
		self.max_drop = max_drop
		self.check_interval = check_interval

		self.watching = False
		self.iteration = 0

		self.book_history = []


	def buy(self):
		bidPrice = float(self.book_history[0]['bidPrice'])
		print('Buying {} {} at {} a piece.'.format(self.trade_amount, self.coin, bidPrice))
		if self.exchange.testOrder(symbol=self.coin, side="BUY", quantity=self.trade_amount, price=askPrice):
			print('Order placed!')

	def check(self):
		self.iteration += 1
		symbol = self.coin + self.converted_currency
		current_book = self.exchange.getBookBySymbol(symbol)

		self.book_history.insert(0, current_book)

		if ( self.trade_amount * float(self.book_history[0]['bidPrice']) ) < 10:
			print('You need to use at least 10 {} to trade with Binance!'.format(self.converted_currency))
			self.watching = False
			return

		if len(self.book_history) > self.min_raise:
			up_count = 0
			for index, book in enumerate(self.book_history[:self.min_raise]):
				bidPrice = float(book['bidPrice'])
				prev_bidPrice = float(self.book_history[index+1]['bidPrice'])
				change = prev_bidPrice / bidPrice
				if change > 1:
					up_count += 1

			if up_count >= self.min_raise:
				print('{} is going up for {} checks in a row! Buying!'.format(self.coin, up_count))
				self.watching = False
				self.buy()

		else:
			print('Waiting...')
			print('Current bid price of {} is {}'.format(self.coin, current_book['bidPrice']))

	def watch(self):
		self.watching = True
		while self.watching:
			self.check()
			time.sleep(self.check_interval)
