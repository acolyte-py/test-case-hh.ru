import ccxt
import time
import numpy as np


exchange = ccxt.binance()

symbol = "ETH/USDT"
interval = "1m"
sma_periods = 20
sma_threshold = 1.0
price = []


print("Программа запущена. Слежение за ценой ETHUSDT...")
while True:
    sma_data = exchange.fetch_ohlcv(symbol, interval, limit=sma_periods)
    close_price = np.array([x[4] for x in sma_data])
    sma = close_price.mean()

    current_price = exchange.fetch_ticker(symbol)['last']
    price.append(current_price)

    if len(price) > sma_periods:
        price.pop(0)

    price_change = (current_price - sma) / sma * 100

    direction = "Нет движения"
    if price_change > sma_threshold:
        direction = "Вверх"
    if price_change < -sma_threshold:
        direction = "Вниз"

    if abs(price_change) > sma_threshold:
        console = f'Цена ETHUSDT изменилась - {price_change:.2f}% | Статус - {direction}'
        print(console)

    time.sleep(60)
