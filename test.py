import ccxt

binance = ccxt.binance({
    'apiKey': 'YnsLUQkfzmBE0SrkNE3IOVwR1VSxZjS6lOAkYlkgBUlup4idTgfN552ZkVHKU9LM',
    'secret': '7lJezp8ba6EARqEokzBxTgxOwUVz5gUmg9UeVSsjpoltTk40HuWOGmzJEolnRjkb'
})

try:
    ticker = binance.fetch_ticker('BTC/USDT')
    print("API有效，BTC/USDT最新价格：", ticker['last'])
except Exception as e:
    print("API无效，错误信息：", e)