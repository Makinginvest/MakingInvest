import ccxt.async_support as ccxt
import pandas as pd
import asyncio
from tqdm import tqdm

exchange = ccxt.binance({"rateLimit": 0, "enableRateLimit": False})


async def getUSDTSymbols():
    symbols = await exchange.fetch_tickers()

    symbols = [s for s in symbols if "USDT" in s]
    symbols = [s for s in symbols if "UP/USDT" not in s]
    symbols = [s for s in symbols if "DOWN/USDT" not in s]

    symbols_to_remove = symbols_to_be_removed()
    symbols = [s for s in symbols if s not in symbols_to_remove]

    return symbols


async def generate_clean_up_file():
    symbols = await exchange.fetch_tickers()

    symbols = [s for s in symbols if "USDT" in s]
    symbols = [s for s in symbols if "UP/USDT" not in s]
    symbols = [s for s in symbols if "DOWN/USDT" not in s]

    symbols_df = pd.DataFrame()

    for symbol in tqdm(symbols):
        bars = await exchange.fetch_ohlcv(symbol, timeframe="5m", limit=1)
        df = pd.DataFrame(bars, columns=["time", "open", "high", "low", "close", "volume"])
        df.drop(["volume"], axis=1, inplace=True)
        df["time"] = pd.to_datetime(df["time"], unit="ms")
        df.insert(0, "symbol", symbol)
        symbols_df = pd.concat([symbols_df, df], axis=0)

    # timestamp now utc time
    symbols_df.insert(0, "time_now", pd.Timestamp.utcnow().tz_convert(None))
    print(symbols_df)
    symbols_df["time_diff"] = symbols_df["time_now"] - symbols_df["time"]
    symbols_df.set_index("time", inplace=True)
    symbols_df.reset_index(inplace=True)

    symbols_df = symbols_df[symbols_df["time_diff"] > pd.Timedelta(days=1)]

    symbols_for_deletion = symbols_df["symbol"].tolist()
    symbols_for_deletion_additional = [
        "USDP/USDT",
        "TUSD/USDT",
        "USDC/USDT",
        "BUSD/USDT",
        "EUR/USDT",
        "GBP/USDT",
        "USDT/RUB",
        "AUD/USDT",
        "USDT/NGN",
        "CNY/USDT",
        "DKK/USDT",
        "HKD/USDT",
        "IDR/USDT",
        "ILS/USDT",
        "INR/USDT",
        "KRW/USDT",
        "MXN/USDT",
        "MYR/USDT",
        "NOK/USDT",
        "NZD/USDT",
        "PHP/USDT",
        "RUB/USDT",
        "SEK/USDT",
        "SGD/USDT",
        "THB/USDT",
        "TRY/USDT",
        "ZAR/USDT",
        "TOMO/USDT",
    ]

    symbols_for_deletion += symbols_for_deletion_additional

    symbols_df = pd.DataFrame(symbols_for_deletion, columns=["symbol"])
    symbols_df.to_csv("_datasets/data/_data_symbols_crypto_delete.csv")


def symbols_to_be_removed():
    df = pd.read_csv("_datasets/data/_data_symbols_crypto_delete.csv")
    return df["symbol"].tolist()


# # asyncio.run(generate_clean_up_file())
# r = asyncio.run(getUSDTSymbols())
# print(len(r))
