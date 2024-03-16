import pandas as pd
import ccxt.async_support as ccxt


exchange = ccxt.binance({"rateLimit": 0, "enableRateLimit": False})


def symbols_to_be_removed():
    df = pd.read_csv("_project/datasets/data/_data_symbols_crypto_delete.csv")
    return df["symbol"].tolist()


async def get_USDT_symbols_binance_api():
    symbols = await exchange.fetch_tickers()

    symbols = [s for s in symbols if "USDT" in s]
    symbols = [s for s in symbols if "UP/USDT" not in s]
    symbols = [s for s in symbols if "DOWN/USDT" not in s]
    # delete if start with "USDT"
    symbols = [s for s in symbols if not s.startswith("USDT")]

    symbols_to_remove = symbols_to_be_removed()
    symbols = [s for s in symbols if s not in symbols_to_remove]

    return symbols


async def get_USDT_symbols_by_value(path="_project/datasets/data/_data_symbols_crypto_usdt_busd.csv"):
    symbols = pd.read_csv(path)
    symbols = symbols["symbol"].tolist()
    # remove all symbols which contains BUSD
    symbols = [s for s in symbols if "BUSD" not in s]
    return symbols


def get_crypto_symbols_with_futures(path="_project/datasets/data/_data_symbols_crypto_futures.csv"):
    symbols = pd.read_csv(path)
    symbols = symbols["symbol"].tolist()
    # remove /
    symbols = [s.replace("/", "") for s in symbols]
    return symbols


async def get_USDT_symbols_by_value_by_df(path="_project/datasets/data/_data_symbols_crypto_usdt_busd.csv"):
    symbols = pd.read_csv(path)
    symbols["rank"] = range(1, len(symbols) + 1)
    return symbols