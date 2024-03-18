import pandas as pd
import ccxt.async_support as ccxt


exchange = ccxt.binance({"rateLimit": 0, "enableRateLimit": False})


async def get_symbols_by_value_v1(path="_project/datasets/data/_data_symbols_crypto_usdt_busd.csv"):
    symbols = pd.read_csv(path)
    symbols = symbols["symbol"].tolist()
    return symbols
