import asyncio
import pandas as pd
from app.helpers.a_functions_mongodb.forex__functions import get_forex_symbols_oanda, get_onada_forex_ohlcv_data


async def getPricesForex():
    try:
        symbols = get_forex_symbols_oanda(path="_project/datasets/data/_data_symbols_forex_oanda.csv")
        symbols = [
            s.replace(
                "/",
                "_",
            )
            for s in symbols
        ]

        df = pd.DataFrame()

        for i in range(0, len(symbols), 5):
            symbols_batch = symbols[i : i + 5]
            val = await asyncio.gather(
                *[
                    get_ohlcv_data(
                        symbol,
                        granularity="M1",
                    )
                    for symbol in symbols_batch
                ]
            )
            df = df.append(val) if val is not None else df

        data = df.to_dict("records")

        return data
    except Exception as e:
        print("Error:ws pulling data", e)
        return []


async def get_ohlcv_data(symbol, granularity="M1") -> pd.DataFrame:
    try:
        df = await get_onada_forex_ohlcv_data(symbol=symbol, granularity=granularity)
        df["timeframe"] = "5m"
        df["symbol"] = symbol
        df["symbol"] = df["symbol"].str.replace("_", "")

        df = df.replace({pd.NaT: None})
        df = df.astype(
            {
                "open": float,
                "high": float,
                "low": float,
                "close": float,
                "volume": float,
            }
        )

        # conver to datetime
        df["dateTimeUtc"] = pd.to_datetime(df["dateTimeUtc"])
        df["dateTimeEst"] = pd.to_datetime(df["dateTimeEst"])
        df["s"] = df["symbol"]
        df["p"] = df["close"]

        # keep s and p only
        df = df[
            [
                "s",
                "p",
            ]
        ]

        # return the last row of the dataframe if it is not empty
        return df.iloc[-1:] if not df.empty else None

    except Exception as e:
        print("Error:ws pulling data", e)
        return None
