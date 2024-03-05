import asyncio
from datetime import datetime
from typing import List

import pandas as pd
import pandas_ta as pta

from app.a_database_data.db_connect_data import database_mongodb_data
from app.helpers.a_functions_indicators.kaufman_efficiency_ratio import kaufman_efficiency_ratio
from app.helpers.a_functions_mongodb.a_mongodb_data import get_mongodb_data_historical


async def get_market_analysis():
    collection = database_mongodb_data["marketAnalysis"]
    res = await collection.find_one({"name": "marketAnalysis"})
    return res


async def update_market_analysis():
    symbols_crypto = ["BTCUSDT", "ETHUSDT", "MATICUSDT", "SOLUSDT", "ADAUSDT", "AVAXUSDT", "LINKUSDT", "DOTUSDT", "BNBUSDT", "ADAUSDT", "XRPUSDT"]
    symbols_forex = ["EURUSD", "GBPUSD", "USDJPY", "USDCHF", "AUDUSD", "NZDUSD", "USDCAD", "EURJPY", "EURGBP"]
    symbols_stocks = ["AAPL", "AMZN", "GOOG", "MSFT", "META", "TSLA", "NVDA", "PYPL", "NFLX", "ADBE", "INTC", "CSCO"]

    tasks = [
        update_market_analysis_by_market(symbols=symbols_crypto, db_collection="historicalCrypto"),
        update_market_analysis_by_market(symbols=symbols_forex, db_collection="historicalForex"),
        update_market_analysis_by_market(symbols=symbols_stocks, db_collection="historicalStocks"),
    ]

    res1, res2, res3 = await asyncio.gather(*tasks)
    res = res1 + res2 + res3

    collection = database_mongodb_data["marketAnalysis"]
    await collection.update_one(
        {"name": "marketAnalysis"},
        {
            "$set": {
                "name": "marketAnalysis",
                "symbolsAnalysis": res,
                "cryptoSymbolsAnalysis": res1,
                "forexSymbolsAnalysis": res2,
                "stocksSymbolsAnalysis": res3,
                "dtUpdated": datetime.utcnow(),
            }
        },
        upsert=True,
    )

    collection = database_mongodb_data["appControlsPrivate"]
    await collection.update_one(
        {"name": "appControlsPrivate"},
        {"$set": {"dtMarketAnalysis": datetime.utcnow()}},
        upsert=True,
    )

    return {
        "name": "marketAnalysis",
        "symbolsAnalysis": res,
        "cryptoSymbolsAnalysis": res1,
        "forexSymbolsAnalysis": res2,
        "stocksSymbolsAnalysis": res3,
        "dtUpdated": datetime.utcnow(),
    }


async def update_market_analysis_by_market(symbols: List = [], db_collection: str = None):
    symbols = list(dict.fromkeys(symbols))

    tasks = [asyncio.create_task(update_market_analysis_by_symbol(symbol=symbol, db_collection=db_collection)) for symbol in symbols]

    results = await asyncio.gather(*tasks)
    res = []
    for r in results:
        if r is not None:
            res.append(r)

    return res


async def update_market_analysis_by_symbol(symbol: str = "BTCUSDT", db_collection: str = None):
    tasks = [
        asyncio.create_task(update_market_analysis_by_symbol_timeframe(symbol=symbol, timeframe="15m", db_collection=db_collection)),
        asyncio.create_task(update_market_analysis_by_symbol_timeframe(symbol=symbol, timeframe="30m", db_collection=db_collection)),
        asyncio.create_task(update_market_analysis_by_symbol_timeframe(symbol=symbol, timeframe="1h", db_collection=db_collection)),
        asyncio.create_task(update_market_analysis_by_symbol_timeframe(symbol=symbol, timeframe="2h", db_collection=db_collection)),
        asyncio.create_task(update_market_analysis_by_symbol_timeframe(symbol=symbol, timeframe="4h", db_collection=db_collection)),
    ]

    # check if path includes crypto
    if "Crypto" in db_collection:
        tasks.append(asyncio.create_task(update_market_analysis_by_symbol_timeframe(symbol=symbol, timeframe="1d", db_collection=db_collection)))

    results = await asyncio.gather(*tasks)
    result = []
    for r in results:
        if r is not None:
            result.append(r)

    res = {
        "symbol": symbol,
        "data": result,
    }

    return res


async def update_market_analysis_by_symbol_timeframe(symbol: str = "BTCUSDT", timeframe: str = "15m", db_collection: str = "historicalCrypto"):
    try:
        df = await get_mongodb_data_historical(symbol=symbol, histCollection=db_collection, timeframe=timeframe, limit=120)

        ha = pta.ha(open_=df["open"], high=df["high"], low=df["low"], close=df["close"])
        df["ha_open"] = ha["HA_open"]
        df["ha_high"] = ha["HA_high"]
        df["ha_low"] = ha["HA_low"]
        df["ha_close"] = ha["HA_close"]

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

        df["sar_long"] = pta.psar(high=df["ha_high"], low=df["ha_low"], close=df["ha_close"])["PSARl_0.02_0.2"]
        df["sar_long_prev1"] = df["sar_long"].shift(1)
        df["sar_short"] = pta.psar(high=df["ha_high"], low=df["ha_low"], close=df["ha_close"])["PSARs_0.02_0.2"]
        df["sar_short_prev1"] = df["sar_short"].shift(1)

        df["sar"] = df.apply(lambda x: x["sar_long"] if pd.notna(x["sar_long"]) else x["sar_short"], axis=1)

        is_close_ichimoku_base_bullish = df["ha_close"].iloc[-1] > df["ichimoku_base"].iloc[-1]
        is_sar_bullish = df["sar"].iloc[-1] < df["ha_close"].iloc[-1]

        status = None
        statusMessages = []

        if is_close_ichimoku_base_bullish & is_sar_bullish:
            status = "Bullish"
            statusMessages.append("Ichimoku bullish")
        elif ~is_close_ichimoku_base_bullish & ~is_sar_bullish:
            status = "Bearish"
            statusMessages.append("Ichimoku bearish")
        else:
            status = "Neutral"

        if is_sar_bullish:
            statusMessages.append("SAR bullish")
        else:
            statusMessages.append("SAR bearish")

        if df["er"].iloc[-1] > 0.5:
            statusMessages.append("ER bullish")
        elif df["er"].iloc[-1] < -0.5:
            statusMessages.append("ER bearish")
        else:
            statusMessages.append("ER neutral")

        return {
            "timeframe": timeframe,
            "status": status,
            "statusMessages": statusMessages,
        }
    except Exception as e:
        print(symbol, e)
        return None
