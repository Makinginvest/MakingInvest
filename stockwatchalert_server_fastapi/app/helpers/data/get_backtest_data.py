import asyncio
import numpy as np
import pandas as pd

from app.helpers.signals.a_get_dataframes_indicators import get_symbol_data_mongodb_by_market_v1, get_symbols_local_by_market_v1


async def get_backtesting_data_crypto(
    timeframe: str = "1d",
    data_length: int = 10000,
    start_datetime: str = "2021-01-01",
    end_datetime: str = "2021-12-31",
):
    # convert datetime_start and datetime_end to datetime
    start_datetime = pd.to_datetime(start_datetime)
    end_datetime = pd.to_datetime(end_datetime)

    symbols = await get_symbols_local_by_market_v1(market="crypto")
    tasks = [get_symbol_data_mongodb_by_market_v1(symbol, timeframe, data_length, start_datetime, end_datetime, "historicalCrypto") for symbol in symbols]
    data_frames = await asyncio.gather(*tasks)
    dataframe = pd.concat(data_frames, axis=0)
    dataframe.to_csv(f"_project/data/data_crypto_{timeframe}.csv", index=False)
    return "done"


async def get_backtesting_data_stocks(
    timeframe: str = "1d",
    data_length: int = 10000,
    start_datetime: str = "2021-01-01",
    end_datetime: str = "2021-12-31",
):
    # convert datetime_start and datetime_end to datetime
    start_datetime = pd.to_datetime(start_datetime)
    end_datetime = pd.to_datetime(end_datetime)

    symbols = await get_symbols_local_by_market_v1(market="stocks")
    symbols = symbols[:250]
    tasks = [get_symbol_data_mongodb_by_market_v1(symbol, timeframe, data_length, start_datetime, end_datetime, "historicalStocks") for symbol in symbols]
    data_frames = await asyncio.gather(*tasks)
    dataframe = pd.concat(data_frames, axis=0)
    dataframe.to_csv(f"_project/data/data_stocks_{timeframe}.csv", index=False)
    return "done"


async def get_backtesting_data_forex(
    timeframe: str = "1d",
    data_length: int = 10000,
    start_datetime: str = "2021-01-01",
    end_datetime: str = "2021-12-31",
):
    # convert datetime_start and datetime_end to datetime
    start_datetime = pd.to_datetime(start_datetime)
    end_datetime = pd.to_datetime(end_datetime)

    symbols = await get_symbols_local_by_market_v1(market="forex")
    tasks = [get_symbol_data_mongodb_by_market_v1(symbol, timeframe, data_length, start_datetime, end_datetime, "historicalForex") for symbol in symbols]
    data_frames = await asyncio.gather(*tasks)
    dataframe = pd.concat(data_frames, axis=0)
    dataframe.to_csv(f"_project/data/data_forex_{timeframe}.csv", index=False)
    return "done"
