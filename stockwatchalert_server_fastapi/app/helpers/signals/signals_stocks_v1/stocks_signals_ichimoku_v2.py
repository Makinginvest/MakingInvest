import asyncio
import os
from datetime import datetime

import numpy as np
import pandas as pd
import pandas_ta as pta
from dotenv import load_dotenv

from app.helpers._functions.get_validate_generate_signals_v1 import get_validate_generate_signals_v1
from app.helpers._functions.notifications_periods_v1 import handle_all_notifications_v1
from app.helpers._indicators.kaufman_efficiency_ratio import kaufman_efficiency_ratio
from app.helpers._mongodb.a_mongodb_client import (
    get_closed_signals_results_v1,
    get_active_signals_from_mongodb_v1,
    update_signals_aggr_open_v1,
    update_signals_by_symbol_v1,
)
from app.helpers.api.symbols_data import get_symbols_data_v1, get_symbols_data_details
from app.helpers.signals.a_get_dataframes_indicators import get_market_rank, get_symbols_local_by_market_v1
from app.helpers.signals.a_get_signals_helpers import calculate_results

load_dotenv()
is_production = os.getenv("PRODUCTION", "False")


async def get_stocks_signals_ichimoku_v2():
    current_time_floor = pd.Timestamp(datetime.utcnow()).floor("15min")
    backtest_mode = True
    use_old_signal = False
    force_gen_new_signals = True
    force_db_update = True

    hist_coll_name = "historicalStocks"
    nameCollection = "signalsStocksV1"
    nameId = "signals_stocks_v2"
    nameIsActive = True
    nameIsAdminOnly = False
    nameMarket = "stocks"
    nameNotificationTitle = "Stocks - High Risk"
    nameSort = 2
    nameType = "Stocks"
    nameTypeSubtitle = "High Risk"
    nameVersion = "1.0.0"
    nameInfo = "High Risk High Returns"
    leverage = 1
    start_up_candles = 60
    max_open_trades = 50
    starting_bal = 1000

    datetime_start = datetime.utcnow() - pd.Timedelta(days=35 * 12 * 1)
    datetime_start_inf = datetime_start - pd.Timedelta(days=10)
    datetime_start = datetime_start - pd.Timedelta(days=10)
    datetime_start_results = datetime_start + pd.Timedelta(days=10)
    datetime_end = datetime.utcnow()
    timeframe = "1d"
    timeframe_inf = "1d"
    timeframe_details = "1h"
    use_information_data = False
    use_df_details = True

    tp1Pct = +0.15 * 1
    tp2Pct = +0.15 * 2
    tp3Pct = +0.15 * 3
    slPct = -0.15 * 1

    # -------------------------------- PRODUCTION -------------------------------- #
    if is_production == "True":
        backtest_mode = False
        use_old_signal = True
        force_gen_new_signals = False
        force_db_update = False
        nameCollection = "signalsStocksV1"
        datetime_start = datetime.utcnow() - pd.Timedelta(days=30 * 1 * 1)
        datetime_start_inf = datetime_start - pd.Timedelta(days=10)
        datetime_start_results = datetime_start
        datetime_end = datetime.utcnow()

    # ---------------------------------- SYMBOLS --------------------------------- #
    symbols = await get_symbols_local_by_market_v1(market="stocks")
    rank_length = len(symbols) * 1
    symbols = symbols[:10000]
    symbols = [
        "AAPL",
        "TSLA",
        "MARA",
        "RIOT",
        "NIO",
        "AMZN",
        "MSFT",
        "GOOGL",
        "FB",
        "NFLX",
        "SPY",
        "QQQ",
        "IWM",
        "DIA",
        "GLD",
        "SLV",
        "GDX",
        "XLF",
        "XLE",
        "XLU",
        "XLI",
        "XLV",
        "XLY",
        "XLK",
        "XLC",
        "XLP",
        "XLB",
        "XBI",
        "XME",
        "XRT",
        "XOP",
        "XHB",
        "XIT",
    ]
    df_timeframe = pd.DataFrame()
    df_details = pd.DataFrame()
    df_candles_signals = pd.DataFrame()

    # ----------------------------- GENERATE SIGNALS ----------------------------- #
    gen_new_signals = get_validate_generate_signals_v1(force_gen_new_signals=force_gen_new_signals, use_old_signal=use_old_signal, floor=timeframe, floor_factor=15)
    if gen_new_signals:

        # --------------------------- informative timeframe -------------------------- #
        if use_information_data:
            df_inf = await get_symbols_data_v1(
                timeframe=timeframe_inf,
                backtest_mode=backtest_mode,
                datetime_start=datetime_start_inf,
                datetime_end=datetime_end,
                symbols=symbols,
                current_time_floor=current_time_floor,
                market=nameMarket,
                hist_coll_name=hist_coll_name,
            )
            # floor to timeframe_inf
            df_inf["dateTimeUtc"] = pd.to_datetime(df_inf["dateTimeUtc"]).dt.floor(timeframe_inf)
            df_inf = df_inf.drop_duplicates(subset=["symbol", "dateTimeUtc"]).reset_index(drop=True)
            df_inf = df_inf.sort_values(by=["symbol", "dateTimeUtc"], ascending=True)
            df_inf = df_inf.groupby("symbol").filter(lambda x: len(x) >= 35)
            df_inf = get_market_rank(df_inf, timeframe=timeframe_inf, rank=rank_length, rolling_lookback=3)
            df_inf: pd.DataFrame = df_inf.groupby("symbol").apply(calculate_indicators_inf).reset_index(drop=True)
            df_inf.columns = [f"{col}_{timeframe_inf}" for col in df_inf.columns]

        # ------------------------------ Main timeframe ------------------------------ #
        df_timeframe = await get_symbols_data_v1(
            timeframe=timeframe,
            backtest_mode=backtest_mode,
            datetime_start=datetime_start,
            datetime_end=datetime_end,
            symbols=symbols,
            current_time_floor=current_time_floor,
            market=nameMarket,
            hist_coll_name=hist_coll_name,
        )
        # ----------------------------- Merge timeframes ----------------------------- #
        if use_information_data:
            df_timeframe[f"dateTimeUtc_{timeframe_inf}"] = pd.to_datetime(df_timeframe["dateTimeUtc"]).dt.floor(timeframe_inf)
            df_timeframe = pd.merge(
                df_timeframe, df_inf, how="left", left_on=["symbol", f"dateTimeUtc_{timeframe_inf}"], right_on=[f"symbol_{timeframe_inf}", f"dateTimeUtc_{timeframe_inf}"]
            )

        if timeframe_inf == "1d":
            df_timeframe["dateTimeUtc"] = pd.to_datetime(df_timeframe["dateTimeUtc"]).dt.floor(timeframe_inf)
            df_timeframe["dateTimeEst"] = pd.to_datetime(df_timeframe["dateTimeEst"]).dt.floor(timeframe_inf)

        df_timeframe = df_timeframe[df_timeframe["dateTimeUtc"] >= datetime_start_results]
        df_timeframe = df_timeframe.drop_duplicates(subset=["symbol", "dateTimeUtc"]).reset_index(drop=True)
        df_timeframe = df_timeframe.groupby("symbol").filter(lambda x: len(x) >= start_up_candles)
        df_timeframe = get_market_rank(df_timeframe, timeframe=timeframe, rank=rank_length, rolling_lookback=6)
        df_timeframe = df_timeframe.sort_values(by=["symbol", "dateTimeUtc"], ascending=True)
        df_timeframe = df_timeframe.groupby("symbol").apply(calculate_indicators).reset_index(drop=True)
        df_timeframe = df_timeframe.groupby("symbol").apply(calculate_signals, timeframe_inf=timeframe_inf).reset_index(drop=True)
        df_timeframe = df_timeframe.groupby("symbol").apply(calculate_signals_exits, timeframe_inf=timeframe_inf).reset_index(drop=True)
        df_candles_signals = df_timeframe[df_timeframe["entryType"].notna()]
        df_candles_signals = df_candles_signals[df_candles_signals["dateTimeUtc"] >= datetime_start_results]
        df_candles_signals_exits = df_timeframe[df_timeframe["exitType"].notna()]
        print(f"df_candles_signals: {len(df_candles_signals)}")

    active_trades_df = pd.DataFrame()
    active_trades_df = await get_active_signals_from_mongodb_v1(nameId=nameId, nameVersion=nameVersion, use_old_signal=use_old_signal, coll_name=nameCollection)
    active_trades_dict = active_trades_df.to_dict(orient="records") if len(active_trades_df) > 0 else []

    if use_df_details:
        df_details = await get_symbols_data_details(
            timeframe=timeframe_details,
            backtest_mode=backtest_mode,
            datetime_start=datetime_start,
            datetime_end=datetime_end,
            df_signals=df_candles_signals,
            df_active_trades=active_trades_df,
            current_time_floor=current_time_floor,
            market=nameMarket,
            hist_coll_name=hist_coll_name,
        )

    trading_results = calculate_results(
        df_candles_entries=df_candles_signals,
        df_candles_targets=df_details,
        df_candles_exits=df_candles_signals_exits,
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
    signals_df_no_duplicates = signals_df.drop_duplicates(subset=["symbol", "entryDateTimeUtc"], keep="last") if len(signals_df) > 0 else signals_df

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
        nameInfo=nameInfo,
        nameTypeSubtitle=nameTypeSubtitle,
        nameNotificationTitle=nameNotificationTitle,
        nameMarket=nameMarket,
        nameCollection=nameCollection,
        results=closed_results,
        signals=active_trades_dict,
    )

    asyncio.create_task(
        handle_all_notifications_v1(
            signals_df=signals_df_no_duplicates,
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
        "nameInfo": nameInfo,
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


def calculate_signals(dataframe: pd.DataFrame, timeframe_inf: str):
    dataframe.loc[
        (
            (dataframe["volume"] > 0)
            & (dataframe["close"] > dataframe["open"])
            & (dataframe["long_cci_check"] == True)
            & (dataframe["long_ichimoku_check"] == True)
            & (dataframe["close"] > dataframe["ichimoku_span_a"])
            & (dataframe["close"] > dataframe["ichimoku_span_b"])
            & (dataframe["high_low_pct_check"] == True)
            & (dataframe["close_open_pct_check"] == True)
            & (dataframe["long_er_check"] == True)
            & (dataframe["adx"] > 15)
            & (dataframe["long_emas_stacked"] == True)
            & (dataframe["no_gap_prev1"] == True)
            # & (dataframe["close"] < 10)
            & (dataframe["volume"] > 500000)
        ),
        ["entryType", "enter_tag"],
    ] = ("long", "ewo_enter_long_high")

    return dataframe


def calculate_signals_exits(dataframe: pd.DataFrame, timeframe_inf: str):
    dataframe.loc[
        ((dataframe["volume"] > 0) & (dataframe["close"] < dataframe["open"]) & (dataframe["sar"] > dataframe["close"])),
        ["exitType", "exit_tag"],
    ] = ("long", "ewo_exit_long_high")

    return dataframe


def calculate_indicators(dataframe, lookback=2):
    dataframe = dataframe.reset_index(drop=True).copy()

    dataframe["close_prev1"] = dataframe["close"].shift(1)
    dataframe["no_gap_prev1"] = np.abs(dataframe["close_prev1"] - dataframe["open"]) / dataframe["close_prev1"] < 0.05

    ha = pta.ha(open_=dataframe["open"], high=dataframe["high"], low=dataframe["low"], close=dataframe["close"])
    dataframe["ha_open"] = ha["HA_open"]
    dataframe["ha_high"] = ha["HA_high"]
    dataframe["ha_low"] = ha["HA_low"]
    dataframe["ha_close"] = ha["HA_close"]

    dataframe["isNew"] = True

    dataframe["macd"] = pta.macd(close=dataframe["close"])[f"MACD_12_26_9"]
    dataframe["macd_signal"] = pta.macd(close=dataframe["close"])[f"MACDs_12_26_9"]
    dataframe["macd_hist"] = pta.macd(close=dataframe["close"])[f"MACDh_12_26_9"]
    dataframe["macd_prev1"] = dataframe["macd"].shift(1)
    dataframe["macd_signal_prev1"] = dataframe["macd_signal"].shift(1)
    dataframe["macd_hist_prev1"] = dataframe["macd_hist"].shift(1)

    dataframe["bb_upper"] = pta.bbands(dataframe["close"], length=20, std=2.0, append=True)["BBU_20_2.0"]
    dataframe["bb_lower"] = pta.bbands(dataframe["close"], length=20, std=2.0, append=True)["BBL_20_2.0"]

    dataframe["kama"] = pta.kama(close=dataframe["ha_close"], length=13, fast=2, slow=30)
    dataframe["kama_prev10"] = dataframe["kama"].shift(10)
    dataframe["kama_pct"] = np.abs(dataframe["kama"] - dataframe["kama_prev10"]) / dataframe["kama_prev10"]

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

    dataframe["rsi"] = pta.rsi(dataframe["ha_close"], length=13, append=True)
    dataframe["rsi_prev"] = dataframe["rsi"].shift(1)
    dataframe["rsi_wma"] = pta.wma(dataframe["rsi"], length=5)

    dataframe["cci"] = pta.cci(dataframe["ha_high"], dataframe["ha_low"], dataframe["ha_close"], length=13)
    dataframe["cci_wma"] = pta.wma(dataframe["cci"], length=5)
    dataframe["cci_wma_prev"] = dataframe["cci_wma"].shift(1)

    dataframe["high_low_pct"] = np.abs(dataframe["low"] - dataframe["high"]) / dataframe["low"]
    dataframe["high_low_pct_check"] = dataframe["high_low_pct"].rolling(lookback).apply(lambda x: all(i < 0.10 for i in x))

    dataframe["close_open_pct"] = np.abs(dataframe["close"] - dataframe["open"]) / dataframe["open"]
    dataframe["close_open_pct_check"] = dataframe["close_open_pct"].rolling(lookback).apply(lambda x: all(i < 0.10 for i in x))
    dataframe["rsi_rolling_85_check"] = dataframe["rsi"].rolling(lookback).apply(lambda x: all(i < 85 for i in x))
    dataframe["rsi_rolling_15_check"] = dataframe["rsi"].rolling(lookback).apply(lambda x: all(i > 15 for i in x))

    dataframe["adx"] = pta.adx(dataframe["ha_high"], dataframe["ha_low"], dataframe["ha_close"], length=13, lensig=13, mamode="rma")["ADX_13"]

    dataframe["tsi"] = pta.tsi(close=dataframe["ha_close"], fast=13, slow=25, signal=13)[f"TSI_13_25_13"]
    dataframe["tsi_signal"] = pta.tsi(close=dataframe["ha_close"], fast=13, slow=25, signal=13)[f"TSIs_13_25_13"]

    dataframe["close_prev2"] = dataframe["close"].shift(2)
    dataframe["sar_long"] = pta.psar(high=dataframe["high"], low=dataframe["low"], close=dataframe["close"], af=0.002, af0=0.002)["PSARl_0.002_0.2"]
    dataframe["sar_short"] = pta.psar(high=dataframe["high"], low=dataframe["low"], close=dataframe["close"], af=0.002, af0=0.002)["PSARs_0.002_0.2"]
    dataframe["sar"] = dataframe["sar_long"].fillna(dataframe["sar_short"])
    dataframe["sar_prev1"] = dataframe["sar"].shift(1)
    dataframe["sar_prev2"] = dataframe["sar"].shift(2)
    dataframe["sar_go_long1"] = (dataframe["sar"] < dataframe["close"]) & (dataframe["sar_prev1"] > dataframe["close_prev1"])
    dataframe["sar_go_short1"] = (dataframe["sar"] > dataframe["close"]) & (dataframe["sar_prev1"] < dataframe["close_prev1"])
    dataframe["sar_go_long2"] = (dataframe["sar"] < dataframe["close"]) & (dataframe["sar_prev2"] > dataframe["close_prev2"])
    dataframe["sar_go_short2"] = (dataframe["sar"] > dataframe["close"]) & (dataframe["sar_prev2"] < dataframe["close_prev2"])
    dataframe["sar_go_long"] = dataframe["sar_go_long1"] | dataframe["sar_go_long2"]
    dataframe["sar_go_short"] = dataframe["sar_go_short1"] | dataframe["sar_go_short2"]

    dataframe["er"] = kaufman_efficiency_ratio(close=dataframe["ha_close"], length=8, directional=True)
    dataframe["er_prev1"] = dataframe["er"].shift(1)
    dataframe["er_prev2"] = dataframe["er"].shift(2)
    dataframe["er_prev3"] = dataframe["er"].shift(3)

    dataframe["er_max_8"] = dataframe["er_prev1"].rolling(8).max()
    dataframe["er_min_8"] = dataframe["er_prev1"].rolling(8).min()

    # -------------------------------- Long checks ------------------------------- #
    dataframe["long_er_check_1"] = dataframe.apply(lambda x: x["er"] > 0.50 and x["er_prev1"] > 0.50 and x["er"] > x["er_prev1"], axis=1)
    dataframe["long_er_check_2"] = dataframe.apply(lambda x: x["er"] > 0.60 and x["er_prev1"] > 0.50, axis=1)
    dataframe["long_er_check_3"] = dataframe.apply(lambda x: x["er_prev2"] < 0.95 or x["er_prev3"] < 0.95, axis=1)
    dataframe["long_er_check"] = (dataframe["long_er_check_1"] | dataframe["long_er_check_2"]) & dataframe["long_er_check_3"]

    dataframe["check_ichimoku_span1"] = dataframe.apply(lambda x: x["ichimoku_span_a"] > x["ichimoku_span_b"], axis=1)
    dataframe["check_ichimoku_span2"] = dataframe.apply(lambda x: x["ichimoku_span_a_ahead"] > x["ichimoku_span_b_ahead"], axis=1)
    # dataframe["long_ichimoku_check"] = dataframe["check_ichimoku_span1"] | dataframe["check_ichimoku_span2"]
    dataframe["long_ichimoku_check"] = dataframe["check_ichimoku_span2"]

    dataframe["long_cci_check"] = dataframe.apply(lambda x: x["cci_wma"] < 150, axis=1)

    dataframe["long_kama_check1"] = dataframe.apply(lambda x: x["close"] > x["kama"], axis=1)
    dataframe["long_kama_check2"] = dataframe.apply(lambda x: x["kama"] > x["kama_prev10"], axis=1)
    dataframe["long_kama_check3"] = dataframe.apply(lambda x: x["kama_pct"] > 0.0 and x["kama_pct"] < 0.1225, axis=1)
    dataframe["long_kama_check4"] = dataframe.apply(lambda x: x["kama"] > x["ichimoku_span_a"] and x["kama"] > x["ichimoku_span_b"], axis=1)
    dataframe["long_kama_check"] = dataframe["long_kama_check1"] & dataframe["long_kama_check2"] & dataframe["long_kama_check3"] & dataframe["long_kama_check4"]

    dataframe["long_check_tsi"] = dataframe.apply(lambda x: x["tsi"] > x["tsi_signal"] and x["tsi"] > 0, axis=1)

    # ------------------------------- Short checks ------------------------------- #
    dataframe["short_er_check_1"] = dataframe.apply(lambda x: x["er"] < -0.50 and x["er_prev1"] < -0.50 and x["er"] < x["er_prev1"], axis=1)
    dataframe["short_er_check_2"] = dataframe.apply(lambda x: x["er"] < -0.60 and x["er_prev1"] < -0.50, axis=1)
    dataframe["short_er_check_3"] = dataframe.apply(lambda x: x["er_prev2"] > -0.95 or x["er_prev3"] > -0.95, axis=1)
    dataframe["short_er_check"] = (dataframe["short_er_check_1"] | dataframe["short_er_check_2"]) & dataframe["short_er_check_3"]

    dataframe["check_ichimoku_span1"] = dataframe.apply(lambda x: x["ichimoku_span_a"] < x["ichimoku_span_b"], axis=1)
    dataframe["check_ichimoku_span2"] = dataframe.apply(lambda x: x["ichimoku_span_a_ahead"] < x["ichimoku_span_b_ahead"], axis=1)
    # dataframe["short_ichimoku_check"] = dataframe["check_ichimoku_span1"] | dataframe["check_ichimoku_span2"]
    dataframe["short_ichimoku_check"] = dataframe["check_ichimoku_span2"]

    dataframe["short_cci_check"] = dataframe.apply(lambda x: x["cci_wma"] > -150, axis=1)

    dataframe["short_kama_check1"] = dataframe.apply(lambda x: x["close"] < x["kama"], axis=1)
    dataframe["short_kama_check2"] = dataframe.apply(lambda x: x["kama"] < x["kama_prev10"], axis=1)
    dataframe["short_kama_check3"] = dataframe.apply(lambda x: x["kama_pct"] > 0.0 and x["kama_pct"] < 0.1225, axis=1)
    dataframe["short_kama_check4"] = dataframe.apply(lambda x: x["kama"] < x["ichimoku_span_a"] and x["kama"] < x["ichimoku_span_b"], axis=1)
    dataframe["short_kama_check"] = dataframe["short_kama_check1"] & dataframe["short_kama_check2"] & dataframe["short_kama_check3"] & dataframe["short_kama_check4"]

    dataframe["short_check_tsi"] = dataframe.apply(lambda x: x["tsi"] < x["tsi_signal"] and x["tsi"] < 0, axis=1)

    dataframe["ewo_ema1"] = pta.ema(dataframe["close"], length=20)
    dataframe["ewo_ema2"] = pta.ema(dataframe["close"], length=60)
    dataframe["ewo"] = (dataframe["ewo_ema1"] - dataframe["ewo_ema2"]) / dataframe["close"] * 100

    return dataframe


def calculate_indicators_inf(dataframe, lookback=2):
    dataframe = dataframe.reset_index(drop=True).copy()
    ha = pta.ha(open_=dataframe["open"], high=dataframe["high"], low=dataframe["low"], close=dataframe["close"])
    dataframe["ha_open"] = ha["HA_open"]
    dataframe["ha_high"] = ha["HA_high"]
    dataframe["ha_low"] = ha["HA_low"]
    dataframe["ha_close"] = ha["HA_close"]

    dataframe["ema13"] = pta.ema(dataframe["close"], length=13)
    dataframe["ema21"] = pta.ema(dataframe["close"], length=21)
    dataframe["ema34"] = pta.ema(dataframe["close"], length=34)

    dataframe["long_emas_stacked"] = (dataframe["ema13"] > dataframe["ema21"]) & (dataframe["ema21"] > dataframe["ema34"])
    dataframe["short_emas_stacked"] = (dataframe["ema13"] < dataframe["ema21"]) & (dataframe["ema21"] < dataframe["ema34"])

    dataframe["ewo_ema1"] = pta.ema(dataframe["close"], length=5)
    dataframe["ewo_ema2"] = pta.ema(dataframe["close"], length=35)
    # dataframe["ewo_ema1"] = pta.ema(dataframe["close"], length=15)
    # dataframe["ewo_ema2"] = pta.ema(dataframe["close"], length=45)
    dataframe["ewo"] = (dataframe["ewo_ema1"] - dataframe["ewo_ema2"]) / dataframe["close"] * 100

    return dataframe
