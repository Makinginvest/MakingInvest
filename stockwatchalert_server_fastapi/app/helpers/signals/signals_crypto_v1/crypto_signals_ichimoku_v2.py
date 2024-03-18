import asyncio
import os
from datetime import datetime

import numpy as np
import pandas as pd
import pandas_ta as pta
from dotenv import load_dotenv

from app.helpers._functions.get_validate_generate_signals_v1 import get_validate_generate_signals_v1
from app.helpers._functions.notifications_periods_v1 import handle_all_notifications_v1
from app.helpers._functions_indicators.kaufman_efficiency_ratio import kaufman_efficiency_ratio
from app.helpers._functions_mongodb.a_mongodb_client_v1 import (
    get_closed_signals_results_v1,
    get_active_signals_from_mongodb_v1,
    update_signals_aggr_open_v1,
    update_signals_by_symbol_v1,
)
from app.helpers.data.get_symbols_data import get_symbols_data_v1, get_symbols_data_details
from app.helpers.signals.a_get_dataframes_indicators import get_market_rank, get_symbols_local_by_market_v1
from app.helpers.signals.a_get_signals_helpers import calculate_results

load_dotenv()
is_production = os.getenv("PRODUCTION", "False")


async def get_crypto_signals_ichimoku_v2():
    current_time_floor = pd.Timestamp(datetime.utcnow()).floor("15min")
    backtest_mode = False
    use_old_signal = False
    force_gen_new_signals = True
    force_db_update = True

    # coll_name = "sSignalsCryptoTestV1"
    hist_coll_name = "historicalCrypto"
    nameCollection = "signalsCryptoV1"
    nameId = "signals_crypto_v3"
    nameIsActive = True
    nameIsAdminOnly = False
    nameMarket = "crypto"
    nameNotificationTitle = "Crypto - Prime"
    nameSort = 2
    nameType = "Crypto"
    nameTypeSubtitle = "Prime"
    nameVersion = "1.0.0"
    leverage = 1
    start_up_candles = 60
    max_open_trades = 25
    starting_bal = 1000

    datetime_start = datetime.utcnow() - pd.Timedelta(days=35 * 3 * 1)
    datetime_start = datetime_start - pd.Timedelta(days=10)
    datetime_start_results = datetime_start + pd.Timedelta(days=10)
    datetime_end = datetime.utcnow()
    timeframe = "4h"
    timeframe_details = "15m"

    tp1Pct = +0.025 * 2
    tp2Pct = +0.025 * 3
    tp3Pct = +0.025 * 4
    slPct = -0.025 * 4

    # -------------------------------- PRODUCTION -------------------------------- #
    if is_production == "True":
        backtest_mode = False
        use_old_signal = True
        force_gen_new_signals = False
        force_db_update = False
        nameCollection = "signalsCryptoV1"
        datetime_start = datetime.utcnow() - pd.Timedelta(days=30 * 1 * 1)
        datetime_start_results = datetime_start
        datetime_end = datetime.utcnow()

    # ---------------------------------- SYMBOLS --------------------------------- #
    symbols = await get_symbols_local_by_market_v1()
    symbols = symbols[:500]
    df = pd.DataFrame()
    df_details = pd.DataFrame()
    df_signals = pd.DataFrame()

    # ----------------------------- GENERATE SIGNALS ----------------------------- #
    gen_new_signals = get_validate_generate_signals_v1(force_gen_new_signals=force_gen_new_signals, use_old_signal=use_old_signal, floor=timeframe, floor_factor=15)
    if gen_new_signals:
        df = await get_symbols_data_v1(
            timeframe=timeframe,
            backtest_mode=backtest_mode,
            datetime_start=datetime_start,
            datetime_end=datetime_end,
            symbols=symbols,
            current_time_floor=current_time_floor,
            market=nameMarket,
            hist_coll_name=hist_coll_name,
        )
        df = df.drop_duplicates(subset=["symbol", "dateTimeUtc"]).reset_index(drop=True)
        df = df.groupby("symbol").filter(lambda x: len(x) >= start_up_candles)
        df = get_market_rank(df, timeframe=timeframe, rank=100, rolling_lookback=3)
        df = df.sort_values(by=["symbol", "dateTimeUtc"], ascending=True)
        df = df.groupby("symbol").apply(calculate_indicators).reset_index(drop=True)
        df = df.groupby("symbol").apply(calculate_signals).reset_index(drop=True)
        df = df.sort_values(by="dateTimeUtc", ascending=True)
        df_signals = df[df["entryType"].notna()]
        df_signals = df_signals[df_signals["dateTimeUtc"] >= datetime_start_results]

    active_trades_df = pd.DataFrame()
    active_trades_df = await get_active_signals_from_mongodb_v1(nameId=nameId, nameVersion=nameVersion, use_old_signal=use_old_signal, coll_name=nameCollection)
    active_trades_dict = active_trades_df.to_dict(orient="records") if len(active_trades_df) > 0 else []

    df_details = await get_symbols_data_details(
        timeframe=timeframe_details,
        backtest_mode=backtest_mode,
        datetime_start=datetime_start,
        datetime_end=datetime_end,
        df_signals=df_signals,
        df_active_trades=active_trades_df,
        current_time_floor=current_time_floor,
        market=nameMarket,
        hist_coll_name=hist_coll_name,
    )

    trading_results = calculate_results(
        df_signals=df_signals,
        df_candles=df_details,
        max_open_trades=max_open_trades,
        starting_bal=starting_bal,
        slPct=slPct,
        tp1Pct=tp1Pct,
        tp2Pct=tp2Pct,
        tp3Pct=tp3Pct,
        active_trades_dict=active_trades_dict,
        lev=leverage,
        market=nameMarket,
        current_time_floor=current_time_floor,
    )

    signalsClosed = trading_results["signalsClosed"]
    signalsActive = trading_results["signalsActive"]
    signals = signalsClosed + signalsActive
    signals_df = pd.DataFrame(signals)

    await update_signals_by_symbol_v1(
        coll_name=nameCollection,
        current_time_floor=current_time_floor,
        nameId=nameId,
        nameVersion=nameVersion,
        signals=signals,
        use_old_signal=use_old_signal,
        backtest_mode=backtest_mode,
        force_db_update=force_db_update,
    )

    closed_results = await get_closed_signals_results_v1(nameId=nameId, nameVersion=nameVersion, coll_name=nameCollection)
    active_trades_df = await get_active_signals_from_mongodb_v1(nameId=nameId, nameVersion=nameVersion, use_old_signal=True, coll_name=nameCollection)
    # sort by entryDateTimeUtc and then by symbol if dataframe is not empty
    active_trades_df = active_trades_df.sort_values(by=["entryDateTimeUtc", "symbol"], ascending=[False, True]) if len(active_trades_df) > 0 else active_trades_df
    active_trades_dict = active_trades_df.to_dict(orient="records") if len(active_trades_df) > 0 else []

    await update_signals_aggr_open_v1(
        nameId=nameId,
        nameLeverage=leverage,
        nameIsActive=nameIsActive,
        nameIsAdminOnly=nameIsAdminOnly,
        nameSort=nameSort,
        nameVersion=nameVersion,
        nameType=nameType,
        nameTypeSubtitle=nameTypeSubtitle,
        nameMarket=nameMarket,
        nameCollection=nameCollection,
        nameNotificationTitle=nameNotificationTitle,
        results=closed_results,
        signals=active_trades_dict,
    )

    asyncio.create_task(
        handle_all_notifications_v1(
            signals_df=signals_df,
            current_time_tp_sl=current_time_floor,
            noti_heading=nameNotificationTitle,
            nameId=nameId,
        )
    )
    # trades where tp1DateTimeUtc is not None and slDateTimeUtc is not None
    signalsTp1 = [trade for trade in signalsClosed if trade["tp1DateTimeUtc"] is not None]
    signalsTp2 = [trade for trade in signalsClosed if trade["tp2DateTimeUtc"] is not None]
    signalsTp3 = [trade for trade in signalsClosed if trade["tp3DateTimeUtc"] is not None]
    signalsSl = [trade for trade in signalsClosed if trade["slDateTimeUtc"] is not None]

    return {
        "nameId": nameId,
        "nameLeverage": leverage,
        "nameIsActive": nameIsActive,
        "nameIsAdminOnly": nameIsAdminOnly,
        "nameSort": nameSort,
        "nameVersion": nameVersion,
        "nameType": nameType,
        "nameTypeSubtitle": nameTypeSubtitle,
        "nameNotificationTitle": nameNotificationTitle,
        "results": closed_results,
        "signalsActive": active_trades_dict,
        "signalsClosed": signalsClosed,
        "signalsTp1Pct": len(signalsTp1) / len(signalsClosed) if len(signalsClosed) > 0 else 0,
        "signalsTp2Pct": len(signalsTp2) / len(signalsClosed) if len(signalsClosed) > 0 else 0,
        "signalsTp3Pct": len(signalsTp3) / len(signalsClosed) if len(signalsClosed) > 0 else 0,
        "signalsSlPct": len(signalsSl) / len(signalsClosed) if len(signalsClosed) > 0 else 0,
    }


def calculate_signals(dataframe: pd.DataFrame):
    dataframe.loc[
        (
            (dataframe["volume"] > 0)
            & (dataframe["close"] > dataframe["open"])
            & (dataframe["long_ichimoku_check"] == True)
            & (dataframe["close"] > dataframe["ichimoku_span_a"])
            & (dataframe["close"] > dataframe["ichimoku_span_b"])
            & (dataframe["is_top_rank"] == True)
            & (dataframe["sar_go_long"] == True)
            & (dataframe["er_go_long"] == True)
            & (dataframe["long_emas_stacked"] == True)
            # ----------------------------------- TEST ----------------------------------- #
            & (dataframe["ewo"] > 2.75)
        ),
        ["entryType", "enter_tag"],
    ] = ("long", "ewo_enter_long_high")
    dataframe.loc[
        (
            (dataframe["volume"] > 0)
            & (dataframe["close"] < dataframe["open"])
            & (dataframe["short_ichimoku_check"] == True)
            & (dataframe["close"] < dataframe["ichimoku_span_a"])
            & (dataframe["close"] < dataframe["ichimoku_span_b"])
            & (dataframe["is_top_rank"] == True)
            & (dataframe["sar_go_short"] == True)
            & (dataframe["er_go_short"] == True)
            & (dataframe["short_emas_stacked"] == True)
            # ----------------------------------- TEST ----------------------------------- #
            & (dataframe["ewo"] < -2.75)
        ),
        ["entryType", "enter_tag"],
    ] = ("short", "ewo_enter_long_high")

    return dataframe


def calculate_indicators(dataframe, lookback=2):
    dataframe = dataframe.reset_index(drop=True).copy()

    symbol = dataframe["symbol"].iloc[0]

    ha = pta.ha(open_=dataframe["open"], high=dataframe["high"], low=dataframe["low"], close=dataframe["close"])
    dataframe["ha_open"] = ha["HA_open"]
    dataframe["ha_high"] = ha["HA_high"]
    dataframe["ha_low"] = ha["HA_low"]
    dataframe["ha_close"] = ha["HA_close"]

    dataframe["isNew"] = True

    dataframe["bb_upper"] = pta.bbands(dataframe["close"], length=20, std=2.0, append=True)["BBU_20_2.0"]
    dataframe["bb_lower"] = pta.bbands(dataframe["close"], length=20, std=2.0, append=True)["BBL_20_2.0"]

    dataframe["close_prev1"] = dataframe["close"].shift(1)
    dataframe["close_prev2"] = dataframe["close"].shift(2)

    dataframe["ema13"] = pta.ema(dataframe["close"], length=13)
    dataframe["ema21"] = pta.ema(dataframe["close"], length=21)
    dataframe["ema34"] = pta.ema(dataframe["close"], length=34)

    dataframe["long_emas_stacked"] = (dataframe["ema13"] > dataframe["ema21"]) & (dataframe["ema21"] > dataframe["ema34"])
    dataframe["short_emas_stacked"] = (dataframe["ema13"] < dataframe["ema21"]) & (dataframe["ema21"] < dataframe["ema34"])

    tenkan = 10
    kijun = 30
    senkou = 60

    ichimoku1 = pta.ichimoku(high=dataframe["high"], low=dataframe["low"], close=dataframe["close"], lookahead=False, tenkan=tenkan, kijun=kijun, senkou=senkou)[0]
    ichimoku2 = pta.ichimoku(high=dataframe["high"], low=dataframe["low"], close=dataframe["close"], lookahead=False, tenkan=tenkan, kijun=kijun, senkou=senkou)[1]

    dataframe["ichimoku_span_a"] = ichimoku1[f"ISA_{tenkan}"]
    dataframe["ichimoku_span_b"] = ichimoku1[f"ISB_{kijun}"]
    dataframe["ichimoku_conversion"] = ichimoku1[f"ITS_{tenkan}"]
    dataframe["ichimoku_base"] = ichimoku1[f"IKS_{kijun}"]

    dataframe["ichimoku_span_a_prev"] = dataframe["ichimoku_span_a"].shift(1)
    dataframe["ichimoku_span_b_prev"] = dataframe["ichimoku_span_b"].shift(1)

    series_ichimoku_span_a_ahead = pd.concat([ichimoku1[f"ISA_{tenkan}"], ichimoku2[f"ISA_{tenkan}"]])
    series_ichimoku_span_b_ahead = pd.concat([ichimoku1[f"ISB_{kijun}"], ichimoku2[f"ISB_{kijun}"]])
    series_ichimoku_span_a_ahead = series_ichimoku_span_a_ahead.iloc[kijun:]
    series_ichimoku_span_b_ahead = series_ichimoku_span_b_ahead.iloc[kijun:]
    series_ichimoku_span_a_ahead.index = dataframe.index
    series_ichimoku_span_b_ahead.index = dataframe.index
    dataframe["ichimoku_span_a_ahead"] = series_ichimoku_span_a_ahead
    dataframe["ichimoku_span_b_ahead"] = series_ichimoku_span_b_ahead

    dataframe["rsi"] = pta.rsi(dataframe["close"], length=13, append=True)
    dataframe["rsi_prev"] = dataframe["rsi"].shift(1)
    dataframe["rsi_wma"] = pta.wma(dataframe["rsi"], length=5)

    dataframe["cci"] = pta.cci(dataframe["high"], dataframe["low"], dataframe["close"], length=13)
    dataframe["cci_wma"] = pta.wma(dataframe["cci"], length=5)
    dataframe["cci_wma_prev"] = dataframe["cci_wma"].shift(1)

    dataframe["high_low_pct"] = np.abs(dataframe["low"] - dataframe["high"]) / dataframe["low"]
    dataframe["high_low_pct_check"] = dataframe["high_low_pct"].rolling(lookback).apply(lambda x: all(i < 0.10 for i in x))

    dataframe["close_open_pct"] = np.abs(dataframe["close"] - dataframe["open"]) / dataframe["open"]
    dataframe["close_open_pct_check"] = dataframe["close_open_pct"].rolling(lookback).apply(lambda x: all(i < 0.10 for i in x))
    dataframe["rsi_rolling_85_check"] = dataframe["rsi"].rolling(lookback).apply(lambda x: all(i < 85 for i in x))
    dataframe["rsi_rolling_15_check"] = dataframe["rsi"].rolling(lookback).apply(lambda x: all(i > 15 for i in x))

    dataframe["sar_long"] = pta.psar(high=dataframe["high"], low=dataframe["low"], close=dataframe["close"])["PSARl_0.02_0.2"]
    dataframe["sar_short"] = pta.psar(high=dataframe["high"], low=dataframe["low"], close=dataframe["close"])["PSARs_0.02_0.2"]
    dataframe["sar"] = dataframe["sar_long"].fillna(dataframe["sar_short"])
    dataframe["sar_prev1"] = dataframe["sar"].shift(1)
    dataframe["sar_prev2"] = dataframe["sar"].shift(2)
    dataframe["sar_go_long1"] = (dataframe["sar"] < dataframe["close"]) & (dataframe["sar_prev1"] > dataframe["close_prev1"])
    dataframe["sar_go_short1"] = (dataframe["sar"] > dataframe["close"]) & (dataframe["sar_prev1"] < dataframe["close_prev1"])
    dataframe["sar_go_long2"] = (dataframe["sar"] < dataframe["close"]) & (dataframe["sar_prev2"] > dataframe["close_prev2"])
    dataframe["sar_go_short2"] = (dataframe["sar"] > dataframe["close"]) & (dataframe["sar_prev2"] < dataframe["close_prev2"])
    dataframe["sar_go_long"] = dataframe["sar_go_long1"] | dataframe["sar_go_long2"]
    dataframe["sar_go_short"] = dataframe["sar_go_short1"] | dataframe["sar_go_short2"]

    dataframe["er10"] = kaufman_efficiency_ratio(close=dataframe["ha_close"], length=10, directional=True)
    dataframe["er10_prev1"] = dataframe["er10"].shift(1)
    dataframe["er10_prev2"] = dataframe["er10"].shift(2)
    dataframe["er10_prev3"] = dataframe["er10"].shift(3)
    dataframe["er5"] = kaufman_efficiency_ratio(close=dataframe["ha_close"], length=5, directional=True)
    dataframe["er5_prev1"] = dataframe["er5"].shift(1)
    dataframe["er5_prev2"] = dataframe["er5"].shift(2)
    dataframe["er5_prev3"] = dataframe["er5"].shift(3)

    dataframe["ewo_ema1"] = pta.ema(dataframe["close"], length=20)
    dataframe["ewo_ema2"] = pta.ema(dataframe["close"], length=80)
    dataframe["ewo"] = (dataframe["ewo_ema1"] - dataframe["ewo_ema2"]) / dataframe["close"] * 100

    dataframe["er_go_long"] = (dataframe["er10"] < 0.30) & (dataframe["er5"] < 0.45)
    dataframe["er_go_short"] = (dataframe["er10"] > -0.30) & (dataframe["er5"] > -0.45)
    # dataframe["er_go_long"] = (dataframe["er10"] < 0.35) & (dataframe["er5"] > 0.55)
    # dataframe["er_go_short"] = (dataframe["er10"] > -0.35) & (dataframe["er5"] < -0.55)

    # -------------------------------- Long checks ------------------------------- #
    dataframe["check_ichimoku_span1"] = dataframe.apply(lambda x: x["ichimoku_span_a"] > x["ichimoku_span_b"], axis=1)
    dataframe["check_ichimoku_span2"] = dataframe.apply(lambda x: x["ichimoku_span_a_ahead"] > x["ichimoku_span_b_ahead"], axis=1)
    dataframe["long_ichimoku_check"] = dataframe["check_ichimoku_span2"]

    dataframe["check_ichimoku_span1"] = dataframe.apply(lambda x: x["ichimoku_span_a"] < x["ichimoku_span_b"], axis=1)
    dataframe["check_ichimoku_span2"] = dataframe.apply(lambda x: x["ichimoku_span_a_ahead"] < x["ichimoku_span_b_ahead"], axis=1)
    dataframe["short_ichimoku_check"] = dataframe["check_ichimoku_span2"]

    return dataframe
