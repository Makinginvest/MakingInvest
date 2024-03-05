import asyncio
import warnings
from datetime import datetime
import numpy as np

import pandas as pd
import pandas_ta as pta
from app.helpers.a_functions.calculate_slope_vectorized import check_crossovers_lookback

from app.helpers.a_functions.dev_print import dev_print
from app.helpers.a_functions.get_minutes import get_df_minute, get_minutes
from app.helpers.a_functions.get_stop_loss import get_stop_loss_pct
from app.helpers.a_functions.get_take_profit_pct import get_take_profit_pct, get_take_profit_pct
from app.helpers.a_functions_indicators.macd_wma import macd_wma
from app.helpers.a_functions_mongodb.a_mongodb_data import get_mongodb_data_historical
from app.models.signal_model import add_required_columns, get_columns_signals


pd.options.display.float_format = "{:.8f}".format
warnings.filterwarnings("ignore")


name = "signals_macd_momentum_long_v1"
nameStr = "Engine 1"
nameInfo = "MACD momentum long"
nameType = "long"
nameSort = 1001
nameVersion = "1.0.2"
nameIsActive = True


def get_signal(df, lookback=7):
    df["r_close"] = df["close"]
    df["r_high"] = df["high"]
    df["r_low"] = df["low"]
    df["r_open"] = df["open"]

    df["r_close_prev"] = df["r_close"].shift(1)
    df["r_high_prev"] = df["r_high"].shift(1)
    df["r_low_prev"] = df["r_low"].shift(1)
    df["r_open_prev"] = df["r_open"].shift(1)

    df["bb_upper"] = pta.bbands(df["close"], length=20, std=3.0, append=True)["BBU_20_3.0"]
    df["bb_lower"] = pta.bbands(df["close"], length=20, std=3.0, append=True)["BBL_20_3.0"]
    df["bb_upper_prev"] = df["bb_upper"].shift(1)
    df["bb_lower_prev"] = df["bb_lower"].shift(1)
    df["close_bb_upper_check"] = check_crossovers_lookback(series1=df["close"], series2=df["bb_upper"], lookback=2, max_cross=0)
    df["close_bb_lower_check"] = check_crossovers_lookback(series1=df["close"], series2=df["bb_lower"], lookback=2, max_cross=0)

    ha = pta.ha(open_=df["open"], high=df["high"], low=df["low"], close=df["close"])
    df["open"] = ha["HA_open"]
    df["high"] = ha["HA_high"]
    df["low"] = ha["HA_low"]
    df["close"] = ha["HA_close"]
    df["high_prev"] = df["high"].shift(1)
    df["low_prev"] = df["low"].shift(1)

    ichimoku1 = pta.ichimoku(high=df["high"], low=df["low"], close=df["close"], lookahead=False)[0]
    ichimoku2 = pta.ichimoku(high=df["high"], low=df["low"], close=df["close"], lookahead=False)[1]

    df["ichimoku_span_a"] = ichimoku1["ISA_9"]
    df["ichimoku_span_b"] = ichimoku1["ISB_26"]
    df["ichimoku_conversion"] = ichimoku1["ITS_9"]
    df["ichimoku_conversion_prev"] = df["ichimoku_conversion"].shift(1)
    df["ichimoku_conversion_prev_prev"] = df["ichimoku_conversion"].shift(2)
    df["ichimoku_base"] = ichimoku1["IKS_26"]

    series_ichimoku_ahead_span_a = pd.concat([ichimoku1["ISA_9"], ichimoku2["ISA_9"]])
    series_ichimoku_ahead_span_b = pd.concat([ichimoku1["ISB_26"], ichimoku2["ISB_26"]])
    series_ichimoku_ahead_span_a = series_ichimoku_ahead_span_a.iloc[26:]
    series_ichimoku_ahead_span_b = series_ichimoku_ahead_span_b.iloc[26:]
    series_ichimoku_ahead_span_a.index = df.index
    series_ichimoku_ahead_span_b.index = df.index
    df["ichimoku_ahead_span_a"] = series_ichimoku_ahead_span_a
    df["ichimoku_ahead_span_b"] = series_ichimoku_ahead_span_b

    df["cci"] = pta.cci(df["high"], df["low"], df["close"], length=13)
    df["cci_prev"] = df["cci"].shift(1)
    df["cci_wma"] = pta.wma(df["cci"], length=8)
    df["cci_wma_prev"] = df["cci_wma"].shift(1)

    df["adx"] = pta.adx(df["high"], df["low"], df["close"], length=13, lensig=13, mamode="rma")["ADX_13"]
    df["adx_prev"] = df["adx"].shift(1)
    df["adx_prev_prev"] = df["adx"].shift(2)

    df["rsi"] = pta.rsi(df["close"], length=13)
    df["rsi_prev"] = df["rsi"].shift(1)
    df["rsi_wma"] = pta.wma(df["rsi"], length=8)
    df["rsi_wma_prev"] = df["rsi_wma"].shift(1)

    # high vs low pct diff less than 4.0%
    df["high_low_pct"] = np.abs(df["r_low"] - df["r_high"]) / df["r_low"]
    df["high_low_pct_check"] = df["high_low_pct"].rolling(lookback * 1).apply(lambda x: all(i < 0.06 for i in x))

    def signal(row):
        adx_check1 = row.adx > 25 and row.adx > row.adx_prev
        adx_check2 = row.adx > 20
        adx_check = adx_check1
        short_gap_check = abs(row.r_close_prev - row.r_open) / row.r_close_prev < 0.02
        short = (
            row.close < row.open
            #
            and row.rsi < row.rsi_prev
            and row.rsi_wma < row.rsi_wma_prev
            and row.rsi_wma < 55
            #
            and row.cci < row.cci_prev
            and row.cci_wma < row.cci_wma_prev
            and row.cci_wma > -150
            #
            and row.close < row.ichimoku_span_a
            and row.close < row.ichimoku_span_b
            and row.low < row.ichimoku_span_a
            and row.low < row.ichimoku_span_b
            and row.ichimoku_span_a < row.ichimoku_span_b
            and row.ichimoku_ahead_span_a < row.ichimoku_ahead_span_b
            #
            and adx_check
            and row.high_low_pct_check
            and row.close_bb_lower_check
            and short_gap_check
        )

        return "short" if short else "none"

    df["entryType"] = df.apply(signal, axis=1)

    return df


async def get_signal_by_symbol(symbol=None, timeframe="6h", data_length=1000, datetime_start=None, datetime_end=None, lookback=7):

    try:
        df = await get_mongodb_data_historical(
            symbol, histCollection="historicalStocks", timeframe=timeframe, limit=data_length, datetime_start=datetime_start, datetime_end=datetime_end
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

        df = pd.merge(df, get_stop_loss_pct(df, 0.05), how="left", on="index")
        df = pd.merge(df, get_take_profit_pct(df, 0.02, 0.04, 0.06, 0.08), how="left", on="index")

        df["newCal"] = True

        df_new_signals = df[df["isNew"] == True]
        df["isNew"] = df["entryDateTimeUtc"].isin(df_new_signals["entryDateTimeUtc"])

        if df[df["entryType"] != "none"].empty:
            return None

        # keep only row with signal
        df = df[df["entryType"] != "none"]

        df["time"] = df["entryDateTimeUtc"]
        df.index = df["time"]

        df["signalName"] = name
        df = add_required_columns(df, market="stocks")

        columns_signals = get_columns_signals

        df = df[columns_signals]
        df = df.replace({pd.NaT: None})

        return [df]

    except Exception as e:
        dev_print(f"Error!: {symbol} {e}")
        return None


async def get_signals_stocks_short_live1(symbols=[], data_length=1000, isEnabled=True, timeframe="6h", datetime_start=None, datetime_end=None, lookback=7):
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
        dev_print(f"get_stocks_signals", e)
        return []
