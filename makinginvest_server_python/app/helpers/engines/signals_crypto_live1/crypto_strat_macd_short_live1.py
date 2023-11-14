import asyncio
import warnings
from datetime import datetime

import numpy as np
import pandas as pd
import pandas_ta as pta

from app.helpers.a_functions.dev_print import dev_print
from app.helpers.a_functions.get_minutes import get_df_minute, get_minutes
from app.helpers.a_functions.get_stop_loss import get_stop_loss_pct
from app.helpers.a_functions.get_take_profit_pct import get_take_profit_pct
from app.helpers.a_functions_indicators.kaufman_efficiency_ratio import kaufman_efficiency_ratio
from app.helpers.a_functions_mongodb.a_mongodb_data import get_mongodb_data_historical
from app.models.signal_model import add_required_columns, get_columns_signals

pd.options.display.float_format = "{:.8f}".format
warnings.filterwarnings("ignore")


def get_signal(df, lookback=7):
    df["r_close"] = df["close"]

    df["bb_upper"] = pta.bbands(df["close"], length=20, std=2.0, append=True)["BBU_20_2.0"]
    df["bb_lower"] = pta.bbands(df["close"], length=20, std=2.0, append=True)["BBL_20_2.0"]

    ha = pta.ha(open_=df["open"], high=df["high"], low=df["low"], close=df["close"])
    df["ha_open"] = ha["HA_open"]
    df["ha_high"] = ha["HA_high"]
    df["ha_low"] = ha["HA_low"]
    df["ha_close"] = ha["HA_close"]

    df["kama"] = pta.kama(close=df["ha_close"], length=13, fast=2, slow=30)
    df["kama_prev10"] = df["kama"].shift(10)
    df["kama_pct"] = np.abs(df["kama"] - df["kama_prev10"]) / df["kama_prev10"]

    df["er"] = kaufman_efficiency_ratio(close=df["ha_close"], length=10, directional=True)
    df["er_prev"] = df["er"].shift(1)

    ichimoku1 = pta.ichimoku(high=df["ha_high"], low=df["ha_low"], close=df["ha_close"], lookahead=False)[0]
    ichimoku2 = pta.ichimoku(high=df["ha_high"], low=df["ha_low"], close=df["ha_close"], lookahead=False)[1]

    df["ichimoku_span_a"] = ichimoku1["ISA_9"]
    df["ichimoku_span_b"] = ichimoku1["ISB_26"]
    df["ichimoku_conversion"] = ichimoku1["ITS_9"]
    df["ichimoku_base"] = ichimoku1["IKS_26"]

    df["ichimoku_span_a_prev"] = df["ichimoku_span_a"].shift(1)
    df["ichimoku_span_b_prev"] = df["ichimoku_span_b"].shift(1)

    series_ichimoku_ahead_span_a = pd.concat([ichimoku1["ISA_9"], ichimoku2["ISA_9"]])
    series_ichimoku_ahead_span_b = pd.concat([ichimoku1["ISB_26"], ichimoku2["ISB_26"]])
    series_ichimoku_ahead_span_a = series_ichimoku_ahead_span_a.iloc[26:]
    series_ichimoku_ahead_span_b = series_ichimoku_ahead_span_b.iloc[26:]
    series_ichimoku_ahead_span_a.index = df.index
    series_ichimoku_ahead_span_b.index = df.index
    df["ichimoku_ahead_span_a"] = series_ichimoku_ahead_span_a
    df["ichimoku_ahead_span_b"] = series_ichimoku_ahead_span_b

    df["rsi"] = pta.rsi(df["ha_close"], length=13, append=True)
    df["rsi_prev"] = df["rsi"].shift(1)
    df["rsi_wma"] = pta.wma(df["rsi"], length=5)

    df["cci"] = pta.cci(df["ha_high"], df["ha_low"], df["ha_close"], length=13)
    df["cci_wma"] = pta.wma(df["cci"], length=5)
    df["cci_wma_prev"] = df["cci_wma"].shift(1)

    # high vs low pct diff less than 6.0%
    df["high_low_pct"] = np.abs(df["low"] - df["high"]) / df["low"]
    df["high_low_pct_check"] = df["high_low_pct"].rolling(lookback).apply(lambda x: all(i < 0.08 for i in x))

    df["close_open_pct"] = np.abs(df["close"] - df["open"]) / df["open"]
    df["close_open_pct_check"] = df["close_open_pct"].rolling(lookback).apply(lambda x: all(i < 0.06 for i in x))
    df["rsi_rolling_15_check"] = df["rsi"].rolling(lookback).apply(lambda x: all(i > 15 for i in x))

    df["adx"] = pta.adx(df["ha_high"], df["ha_low"], df["ha_close"], length=13, lensig=13, mamode="rma")["ADX_13"]

    df["tsi"] = pta.tsi(close=df["ha_close"], fast=13, slow=25, signal=13)[f"TSI_13_25_13"]
    df["tsi_signal"] = pta.tsi(close=df["ha_close"], fast=13, slow=25, signal=13)[f"TSIs_13_25_13"]

    df["macd"] = pta.macd(close=df["ha_close"])[f"MACD_12_26_9"]
    df["macd_signal"] = pta.macd(close=df["ha_close"])[f"MACDs_12_26_9"]
    df["macd_hist"] = pta.macd(close=df["ha_close"])[f"MACDh_12_26_9"]
    df["macd_prev1"] = df["macd"].shift(1)
    df["macd_signal_prev1"] = df["macd_signal"].shift(1)
    df["macd_hist_prev1"] = df["macd_hist"].shift(1)

    df["sar_long"] = pta.psar(high=df["ha_high"], low=df["ha_low"], close=df["ha_close"])["PSARl_0.02_0.2"]
    df["sar_long_prev1"] = df["sar_long"].shift(1)
    df["sar_short"] = pta.psar(high=df["ha_high"], low=df["ha_low"], close=df["ha_close"])["PSARs_0.02_0.2"]
    df["sar_short_prev1"] = df["sar_short"].shift(1)

    def signal(row):
        er_check1 = row.er < -0.50 and row.er_prev < -0.45 and row.er < row.er_prev
        er_check2 = row.er < -0.60 and row.er_prev < -0.40
        er_check = er_check1 or er_check2

        check_ichimoku_span1 = row.ichimoku_span_a < row.ichimoku_span_b
        check_ichimoku_span2 = row.ichimoku_ahead_span_a < row.ichimoku_ahead_span_b
        check_ichimoku_span = check_ichimoku_span1 or check_ichimoku_span2

        cci_check = row.cci_wma > -125

        kama_check1 = row.close < row.kama
        kama_check2 = row.kama < row.kama_prev10
        kama_check3 = row.kama_pct > 0.0 and row.kama_pct < 0.1225
        kama_check4 = row.kama < row.ichimoku_span_a and row.kama < row.ichimoku_span_b
        kama_check = kama_check1 and kama_check2 and kama_check3 and kama_check4

        check_tsi = row.tsi < row.tsi_signal and row.tsi < 0

        short = (
            row.ha_close < row.ha_open
            and row.close < row.open
            and row.open > row.bb_lower
            #
            and cci_check
            #
            and check_ichimoku_span
            and row.close < row.ichimoku_span_a
            and row.close < row.ichimoku_span_b
            and row.open < row.ichimoku_span_a
            and row.open < row.ichimoku_span_b
            #
            and row.high_low_pct_check
            and row.close_open_pct_check
            and row.rsi_rolling_15_check
            and er_check
            and kama_check
            #
            and row.adx > 15
            and row.adx < 60
            #
            and check_tsi
            and row.sar_short > row.ha_close
            # ------------------------------- 8h timeframe ------------------------------- #
            # and row.sar_short_8h > row.close_8h
        )

        return "short" if short else "none"

    df["entryType"] = df.apply(signal, axis=1)

    return df


async def get_signal_by_symbol(symbol=None, timeframe="6h", data_length=1000, datetime_start=None, datetime_end=None, lookback=7):
    try:
        df = await get_mongodb_data_historical(
            symbol, histCollection="historicalCrypto", timeframe=timeframe, limit=data_length, datetime_start=datetime_start, datetime_end=datetime_end
        )

        if df is None or df.empty:
            return None

        # rename dateTimeUtc entryDateTimeUtc
        df = df.rename(columns={"dateTimeUtc": "entryDateTimeUtc"})
        df = df.rename(columns={"dateTimeEst": "entryDateTimeEst"})

        df.index = df["entryDateTimeUtc"]
        df.index.name = "index"

        df["entryType"] = get_signal(df, lookback=lookback)["entryType"]

        df["time_last_row"] = datetime.utcnow()
        df["time_last_row"] = df["time_last_row"].apply(lambda x: pd.Timestamp(x).floor(get_df_minute(timeframe)))
        df["time_last_row"] = df["time_last_row"].iloc[-1] - pd.Timedelta(minutes=get_minutes(timeframe))
        df["isNew"] = df["entryDateTimeUtc"] == df["time_last_row"]

        # add 5m mins to entryDateTimeUtc and entryDateTimeEst so that it show for candle open
        df["entryDateTimeUtc"] = df["entryDateTimeUtc"] + pd.Timedelta(minutes=get_minutes(timeframe))
        df["entryDateTimeEst"] = df["entryDateTimeEst"] + pd.Timedelta(minutes=get_minutes(timeframe))
        df.index = df["entryDateTimeUtc"]
        df.index.name = "index"

        df["timeframe"] = timeframe
        df["symbol"] = symbol
        df["entryPrice"] = df["r_close"]
        df["comment"] = ""

        df = pd.merge(df, get_stop_loss_pct(df, 0.06, True), how="left", on="index")
        df = pd.merge(df, get_take_profit_pct(df, 0.02, 0.04, 0.08, 0.16, True), how="left", on="index")

        df["newCal"] = True

        df_new_signals = df[df["isNew"] == True]
        df["isNew"] = df["entryDateTimeUtc"].isin(df_new_signals["entryDateTimeUtc"])

        if df[df["entryType"] != "none"].empty:
            return None

        # keep only row with signal
        df = df[df["entryType"] != "none"]

        df["time"] = df["entryDateTimeUtc"]
        df.index = df["time"]

        df = add_required_columns(df)

        columns_signals = get_columns_signals

        df = df[columns_signals]
        df = df.replace({pd.NaT: None})

        return [df]

    except Exception as e:
        dev_print(f"Error!: {symbol} {e}")
        return None


async def get_signals_crypto_short_live1(symbols=[], data_length=1000, isEnabled=True, timeframe="6h", datetime_start=None, datetime_end=None, lookback=7):
    if isEnabled == False:
        return []
    signals_xyz = pd.DataFrame(columns=get_columns_signals)

    try:
        for i in range(0, len(symbols), 8):
            symbol_batch = symbols[i : i + 8]
            tasks = [
                get_signal_by_symbol(
                    symbol,
                    timeframe,
                    data_length=data_length,
                    datetime_start=datetime_start,
                    datetime_end=datetime_end,
                    lookback=lookback,
                )
                for symbol in symbol_batch
            ]
            results = await asyncio.gather(*tasks)
            for result in results:
                if result is not None:
                    signals_xyz = signals_xyz.append(result, ignore_index=True)

        signals_xyz = signals_xyz.sort_values(by=["entryDateTimeUtc"], ascending=False)
        return signals_xyz

    except Exception as e:
        dev_print(f"get_crypto_signals", e)
        return []
