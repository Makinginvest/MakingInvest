import warnings
import numpy as np

import pandas as pd
import pandas_ta as pta

from app.helpers.a_functions.dev_print import dev_print
from app.helpers.a_functions.get_ha_candles import get_ha_candles
from app.helpers.a_functions_indicators.calculate_volatility import calculate_volatility
from app.helpers.a_functions_indicators.kaufman_efficiency_ratio import kaufman_efficiency_ratio
from app.helpers.a_functions_mongodb.a_mongodb_data import get_mongodb_data_historical


pd.options.display.float_format = "{:.8f}".format
warnings.filterwarnings("ignore")


def get_resample_df(df, resample="1d"):
    _df = df.resample(resample).agg({"open": "first", "high": "max", "low": "min", "close": "last", "volume": "sum"})
    _df = _df.dropna()
    _df.columns = [f"{x}_{resample}" for x in _df.columns]
    columns = [f"{x}_{resample}" for x in ["open", "high", "low", "close", "volume"]]
    _df = _df[columns]

    _df[f"volitility_{resample}"] = calculate_volatility(_df[f"close_{resample}"], 10)
    return _df


async def get_btc_df(symbol=None, timeframe="6h", data_length=1000, datetime_start=None, datetime_end=None, lookback=7):
    try:
        df = await get_mongodb_data_historical(
            symbol,
            histCollection="historicalCrypto",
            timeframe=timeframe,
            limit=data_length,
            datetime_start=datetime_start,
            datetime_end=datetime_end,
        )

        if df is None or df.empty:
            return None

        # rename dateTimeUtc entryDateTimeUtc
        df = df.rename(columns={"dateTimeUtc": "entryDateTimeUtc"})
        df = df.rename(columns={"dateTimeEst": "entryDateTimeEst"})

        df.index = df["entryDateTimeUtc"]
        df.index.name = "index"

        df["bb_upper"] = pta.bbands(df["close"], length=20, std=2.0, append=True)["BBU_20_2.0"]
        df["bb_lower"] = pta.bbands(df["close"], length=20, std=2.0, append=True)["BBL_20_2.0"]

        df["original_index"] = df.index
        df = pd.merge(df, get_ha_candles(df), left_index=True, right_index=True, how="left")
        df.index = df["original_index"]
        df.index.name = "index"

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
        df["rsi_wma_prev"] = df["rsi_wma"].shift(1)

        df["cci"] = pta.cci(df["ha_high"], df["ha_low"], df["ha_close"], length=13)
        df["cci_wma"] = pta.wma(df["cci"], length=5)
        df["cci_wma_prev"] = df["cci_wma"].shift(1)

        # high vs low pct diff less than 4.0%
        df["high_low_pct"] = np.abs(df["low"] - df["high"]) / df["low"]
        df["high_low_pct_check"] = df["high_low_pct"].rolling(lookback).apply(lambda x: all(i < 0.08 for i in x))

        df["close_open_pct"] = np.abs(df["close"] - df["open"]) / df["open"]
        df["close_open_pct_check"] = df["close_open_pct"].rolling(lookback).apply(lambda x: all(i < 0.06 for i in x))
        df["rsi_rolling_85_check"] = df["rsi"].rolling(lookback).apply(lambda x: all(i < 85 for i in x))

        df["adx"] = pta.adx(df["high"], df["low"], df["close"], length=13, lensig=13, mamode="rma")["ADX_13"]
        df["adx_prev"] = df["adx"].shift(1)

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

        # columns = [f"{symbol}_{x}_{timeframe}" for x in df.columns]
        # df = df[columns]
        # rename columns to include symbol and timeframe
        df.columns = [f"{symbol}_{x}_{timeframe}" for x in df.columns]
        return df

    except Exception as e:
        dev_print(f"Error!: {symbol} {e}")
        return None
