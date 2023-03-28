import time
import os

from binance.client import Client
from dotenv import load_dotenv
from datetime import datetime


load_dotenv()

api_key = os.getenv('API_KEY')
api_secret = os.getenv('API_SECRET')

client = Client(api_key, api_secret)
symbol = 'ETHUSDT'
interval = Client.KLINE_INTERVAL_1MINUTE


def get_price():
    futures_data = client.futures_klines(symbol=symbol, interval=interval, limit=60)
    close_prices = [float(x[4]) for x in futures_data]
    moving_average = sum(close_prices) / len(close_prices)
    current_price = float(client.futures_symbol_ticker(symbol=symbol)['price'])

    return current_price, moving_average


while True:
    current_price, moving_average = get_price()

    if current_price > moving_average * 1.01 or current_price < moving_average * 0.99:
        print(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}: Цена изменилась на 1% за последние 60 минут')

    time.sleep(1)
