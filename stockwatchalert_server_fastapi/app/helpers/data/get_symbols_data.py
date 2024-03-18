import asyncio
from datetime import datetime
from os import dup
import numpy as np
import pandas as pd
from app.helpers._functions.dev_print_v1 import dev_print
from app.helpers._functions.get_minutes_v1 import get_minutes_v1

from app.helpers.signals.a_get_dataframes_indicators import get_symbol_data_mongodb_by_market_v1, get_symbols_local_by_market_v1


async def get_symbols_data_v1(
    timeframe: str = "1d",
    backtest_mode: bool = False,
    data_length: int = 10000,
    datetime_start: str = "2021-01-01",
    datetime_end: str = "2021-12-31",
    symbols: list = [],
    current_time_floor: pd.Timestamp = pd.Timestamp(datetime.utcnow()).floor("15min"),
    market: str = "crypto",
    hist_coll_name: str = "historicalCrypto",
):
    # Main dataframe
    dev_print("backtest_mode", backtest_mode)
    dataframe = pd.DataFrame()
    start_time = asyncio.get_event_loop().time()
    if backtest_mode:
        dataframe = pd.read_csv(f"_project/data/data_{market}_{timeframe}.csv")
        dataframe["dateTimeUtc"] = pd.to_datetime(dataframe["dateTimeUtc"])
        dataframe["dateTimeEst"] = pd.to_datetime(dataframe["dateTimeEst"])
        dataframe = dataframe[dataframe["dateTimeUtc"] >= datetime_start]
        dataframe = dataframe[dataframe["symbol"].isin(symbols)]
    else:
        tasks = [get_symbol_data_mongodb_by_market_v1(symbol, timeframe, data_length, datetime_start, datetime_end, hist_coll_name) for symbol in symbols]
        data_frames = await asyncio.gather(*tasks)
        dataframe = pd.concat(data_frames, axis=0)
    dataframe["dateTimeUtc"] = dataframe["dateTimeUtc"] + pd.Timedelta(minutes=get_minutes_v1(timeframe))
    dataframe["dateTimeEst"] = dataframe["dateTimeEst"] + pd.Timedelta(minutes=get_minutes_v1(timeframe))
    # ensure dateTimeUtc is not in the future
    # print(dataframe.tail(1))
    dataframe = dataframe[dataframe["dateTimeUtc"] <= current_time_floor]
    # print(dataframe.tail(1))
    end_time = asyncio.get_event_loop().time()
    dev_print(f"Time df: {end_time - start_time} seconds")

    return dataframe


async def get_symbols_data_details(
    timeframe: str = "1d",
    backtest_mode: bool = False,
    data_length: int = 10000,
    datetime_start: str = "2021-01-01",
    datetime_end: str = "2021-12-31",
    df_signals: pd.DataFrame = pd.DataFrame(),
    df_active_trades=pd.DataFrame(),
    current_time_floor: pd.Timestamp = pd.Timestamp(datetime.utcnow()).floor("15min"),
    market: str = "crypto",
    hist_coll_name: str = "historicalCrypto",
):

    dataframe_details = pd.DataFrame()
    symbols = df_signals["symbol"].unique() if df_signals.shape[0] > 0 else []
    start_time = asyncio.get_event_loop().time()
    first_df_signal_datetime = df_signals["dateTimeUtc"].min() if df_signals.shape[0] > 0 else datetime_start

    # ----------------------------- BACKTESTING MODE ----------------------------- #
    if backtest_mode and df_signals.shape[0] > 0:
        dataframe_details = pd.read_csv(f"_project/data/data_{market}_{timeframe}.csv")
        dataframe_details["dateTimeUtc"] = pd.to_datetime(dataframe_details["dateTimeUtc"])
        dataframe_details["dateTimeEst"] = pd.to_datetime(dataframe_details["dateTimeEst"])
        dataframe_details = dataframe_details[dataframe_details["dateTimeUtc"] >= first_df_signal_datetime]
        dataframe_details = dataframe_details[dataframe_details["symbol"].isin(symbols)]
        dataframe_details = dataframe_details.sort_values(by=["symbol", "dateTimeUtc"], ascending=True)

    if backtest_mode and not df_signals.shape[0] > 0:
        dataframe_details = pd.read_csv(f"_project/data/data_{market}_{timeframe}.csv")
        dataframe_details["dateTimeUtc"] = pd.to_datetime(dataframe_details["dateTimeUtc"])
        dataframe_details["dateTimeEst"] = pd.to_datetime(dataframe_details["dateTimeEst"])
        dataframe_details = dataframe_details[dataframe_details["dateTimeUtc"] >= first_df_signal_datetime]
        dataframe_details = dataframe_details.sort_values(by=["symbol", "dateTimeUtc"], ascending=True)

    # -------------------------------- NEW TRADES -------------------------------- #
    if not backtest_mode and df_signals.shape[0] > 0:
        rows = [df_signals[df_signals["symbol"] == symbol].iloc[0] for symbol in df_signals["symbol"].unique()]
        tasks = []
        for row in rows:
            symbol = row["symbol"]
            start = row["dateTimeUtc"] - pd.Timedelta(days=1)
            tasks.append(get_symbol_data_mongodb_by_market_v1(symbol, timeframe, data_length, start, datetime_end, hist_coll_name))
        data_frames_details = await asyncio.gather(*tasks)
        dataframe_details = pd.concat(data_frames_details, axis=0)
        dataframe_details = dataframe_details.sort_values(by=["symbol", "dateTimeUtc"], ascending=True)

    # -------------------------------- OLD TRADES -------------------------------- #
    if not backtest_mode and len(df_active_trades) > 0:
        # if not backtest_mode and active_trades.shape[0] > 0:
        rows = [df_active_trades[df_active_trades["symbol"] == symbol].iloc[0] for symbol in df_active_trades["symbol"].unique()]
        tasks = []
        for row in rows:
            symbol = row["symbol"]
            # these come from the db, so they dont have dateTimeUtc
            start = row["entryDateTimeUtc"] - pd.Timedelta(days=1)
            tasks.append(get_symbol_data_mongodb_by_market_v1(symbol, timeframe, data_length, start, datetime_end, hist_coll_name))
        data_frames_details = await asyncio.gather(*tasks)
        dataframe_details = pd.concat(data_frames_details, axis=0)
        dataframe_details = dataframe_details.sort_values(by=["symbol", "dateTimeUtc"], ascending=True)

    # ----- Delete duplicates by symbol and dateTimeUtc and keep the last one ---- #
    if len(dataframe_details) > 0:
        dataframe_details = dataframe_details.drop_duplicates(subset=["symbol", "dateTimeUtc"], keep="last")
        dataframe_details["dateTimeUtc"] = dataframe_details["dateTimeUtc"] + pd.Timedelta(minutes=get_minutes_v1(timeframe))
        dataframe_details["dateTimeEst"] = dataframe_details["dateTimeEst"] + pd.Timedelta(minutes=get_minutes_v1(timeframe))
        dataframe_details = dataframe_details[dataframe_details["dateTimeUtc"] <= current_time_floor]
    end_time = asyncio.get_event_loop().time()
    dev_print(f"Time df details: {end_time - start_time} seconds")

    return dataframe_details
