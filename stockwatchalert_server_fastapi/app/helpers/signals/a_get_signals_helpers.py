from datetime import datetime
import os
import numpy as np
import pandas as pd
from tabulate import tabulate
from tqdm import tqdm

from app.helpers.signals.a_get_dataframes_indicators import get_dates_months, get_trades_duration_from_seconds

from dotenv import load_dotenv

load_dotenv()
is_production = os.getenv("PRODUCTION", "False")

signals_columns = [
    "entryDateTimeUtc",
    "entryDateTimeEst",
    "exitDateTimeUtc",
    "exitDateTimeEst",
    "lastCheckedDateTimeUtc",
    "leverage",
    "statusTrade",
    "statusTarget",
    "symbol",
    "timeframe",
    "entryType",
    "entryPrice",
    "exitPrice",
    "tp1Pct",
    "tp1Price",
    "tp1Pips",
    "tp1DateTimeUtc",
    "tp1DateTimeEst",
    "tp2Pct",
    "tp2Price",
    "tp2Pips",
    "tp2DateTimeUtc",
    "tp2DateTimeEst",
    "tp3Pct",
    "tp3Price",
    "tp3Pips",
    "tp3DateTimeUtc",
    "tp3DateTimeEst",
    "slPct",
    "slPips",
    "slDateTimeUtc",
    "slDateTimeEst",
    "slPrice",
    "comment",
    "analysisImage",
    "tradeDurationStr",
    "tradeDurationSeconds",
    "amtTradeStart",
    "amtTrade",
    "amtProfit",
    "amtProfitMaxPct",
    "amtProfitMinPct",
    "amtProfitMaxPips",
    "amtProfitMinPips",
    "amtProfitMaxDateTimeUtc",
    "amtProfitMinDateTimeUtc",
    "isClosed",
    "isNew",
    "market",
    "minPrice",
    "maxPrice",
]


def calculate_results(
    df_signals: pd.DataFrame,
    df_candles: pd.DataFrame,
    active_trades_dict=[],
    max_open_trades=20,
    starting_bal=1000,
    slPct=-0.06,
    tp1Pct=0.02,
    tp2Pct=0.04,
    tp3Pct=0.06,
    lev=1,
    market="crypto",
    current_time_floor=pd.Timestamp(datetime.utcnow()).floor("15min"),
):

    if len(df_signals) == 0 and len(active_trades_dict) == 0:
        return {"signalsClosed": [], "signalsActive": []}

    active_trades_dict = active_trades_dict
    amount_per_trade = starting_bal / max_open_trades
    amount_reseved_per_trade = amount_per_trade * len(active_trades_dict)
    # update active trades with new amount per trade
    for trade in active_trades_dict:
        # print("trade", trade)
        trade["amtTrade"] = amount_per_trade
        trade["amtAvailable"] = None
        trade["amtTradeStart"] = None
    #
    trade_outcomes = active_trades_dict
    starting_bal = starting_bal
    avail_bal = starting_bal - amount_reseved_per_trade
    curr_bal = starting_bal
    min_bal = starting_bal
    max_bal = starting_bal

    # only add column is dataframe is not empty
    if len(df_signals) > 0:
        df_signals["tp1Pct"] = tp1Pct
        df_signals["tp2Pct"] = tp2Pct
        df_signals["tp3Pct"] = tp3Pct
        df_signals["tp1Pips"] = df_signals["tp1Pct"] * df_signals["close"] * 10000
        df_signals["tp2Pips"] = df_signals["tp2Pct"] * df_signals["close"] * 10000
        df_signals["tp3Pips"] = df_signals["tp3Pct"] * df_signals["close"] * 10000
        df_signals["tp1Price"] = np.where(df_signals["entryType"] == "long", df_signals["close"] * (1 + df_signals["tp1Pct"]), df_signals["close"] * (1 - df_signals["tp1Pct"]))
        df_signals["tp2Price"] = np.where(df_signals["entryType"] == "long", df_signals["close"] * (1 + df_signals["tp2Pct"]), df_signals["close"] * (1 - df_signals["tp2Pct"]))
        df_signals["tp3Price"] = np.where(df_signals["entryType"] == "long", df_signals["close"] * (1 + df_signals["tp3Pct"]), df_signals["close"] * (1 - df_signals["tp3Pct"]))
        df_signals["tp1DateTimeEst"] = None
        df_signals["tp1DateTimeUtc"] = None
        df_signals["tp2DateTimeEst"] = None
        df_signals["tp2DateTimeUtc"] = None
        df_signals["tp3DateTimeEst"] = None
        df_signals["tp3DateTimeUtc"] = None
        df_signals["slPct"] = slPct
        df_signals["slPips"] = df_signals["slPct"] * df_signals["close"] * 10000
        df_signals["slPrice"] = np.where(df_signals["entryType"] == "long", df_signals["close"] * (1 + df_signals["slPct"]), df_signals["close"] * (1 - df_signals["slPct"]))
        df_signals["slDateTimeEst"] = None
        df_signals["slDateTimeUtc"] = None
        df_signals["comment"] = ""
        df_signals["analysisImage"] = ""
        df_signals["tradeDurationSeconds"] = None
        df_signals["tradeDurationStr"] = ""
        df_signals["statusTrade"] = ""
        df_signals["statusTarget"] = "In Progress"
        df_signals["entryDateTimeUtc"] = None
        df_signals["entryDateTimeEst"] = None
        df_signals["exitDateTimeUtc"] = None
        df_signals["exitDateTimeEst"] = None
        df_signals["entryPrice"] = df_signals["close"]
        df_signals["exitPrice"] = None
        df_signals["lastCheckedDateTimeUtc"] = df_signals["dateTimeUtc"]
        df_signals["openTrades"] = 0
        df_signals["amtAvailable"] = 0
        df_signals["amtTradeStart"] = 0
        df_signals["amtTrade"] = 0
        df_signals["amtProfit"] = 0
        df_signals["amtProfitMaxPct"] = 0
        df_signals["amtProfitMinPct"] = 0
        df_signals["amtProfitMaxPips"] = 0
        df_signals["amtProfitMinPips"] = 0
        df_signals["amtProfitMaxDateTimeUtc"] = None
        df_signals["amtProfitMinDateTimeUtc"] = None
        df_signals["leverage"] = lev
        df_signals["market"] = market
        df_signals["minPrice"] = df_signals["low"]
        df_signals["maxPrice"] = df_signals["high"]

        # if symbol includes JPY and market is forex, divide tp1Pips, tp2Pips, tp3Pips and slPips by 100
        df_signals["tp1Pips"] = df_signals.apply(lambda x: x["tp1Pips"] / 100 if "JPY" in x["symbol"] and x["market"] == "forex" else x["tp1Pips"], axis=1)
        df_signals["tp2Pips"] = df_signals.apply(lambda x: x["tp2Pips"] / 100 if "JPY" in x["symbol"] and x["market"] == "forex" else x["tp2Pips"], axis=1)
        df_signals["tp3Pips"] = df_signals.apply(lambda x: x["tp3Pips"] / 100 if "JPY" in x["symbol"] and x["market"] == "forex" else x["tp3Pips"], axis=1)
        df_signals["slPips"] = df_signals.apply(lambda x: x["slPips"] / 100 if "JPY" in x["symbol"] and x["market"] == "forex" else x["slPips"], axis=1)

    # datetimes_signal = df_signals["dateTimeUtc"].unique()
    df_candles_datetimes = df_candles["dateTimeUtc"].sort_values(ascending=True).unique()
    df_candles_datetime_first = df_candles_datetimes[0]
    df_candles_datetime_last = df_candles_datetimes[-1]
    df_candles["dateTimeUtc2"] = df_candles["dateTimeUtc"]
    grouped_candles = df_candles.groupby("symbol").apply(lambda x: x.set_index("dateTimeUtc2"))
    # write to file
    # print("df_candles_datetime_first", df_candles_datetime_first, "df_candles_datetime_last", df_candles_datetime_last)

    sequence = df_candles_datetimes if is_production == "True" else tqdm(df_candles_datetimes)
    for current_time in sequence:
        for trade in active_trades_dict:
            if (trade["symbol"], current_time) in grouped_candles.index:
                candle = grouped_candles.loc[trade["symbol"], current_time]
            else:
                candle = None
                continue

            if current_time < trade["entryDateTimeUtc"]:
                continue

            # --- PRODUCTION  PREVENT OLD TIMEFRAME CLOSING TRADES -- #
            if is_production == "True":
                if current_time < current_time_floor:
                    continue

            trade["lastCheckedDateTimeUtc"] = current_time
            # ----------------------------------- LONG ----------------------------------- #
            if trade["entryType"] == "long":
                change_max_pct = (candle["high"] - trade["entryPrice"]) / trade["entryPrice"]
                change_min_pct = (candle["low"] - trade["entryPrice"]) / trade["entryPrice"]
                trade["amtProfitMaxPct"] = max(trade["amtProfitMaxPct"], change_max_pct)
                trade["amtProfitMinPct"] = min(trade["amtProfitMinPct"], change_min_pct)

                trade["minPrice"] = min(trade["minPrice"], candle["low"])
                trade["maxPrice"] = max(trade["maxPrice"], candle["high"])
                trade["amtProfitMaxPips"] = (trade["maxPrice"] - trade["entryPrice"]) * 10000
                trade["amtProfitMinPips"] = (trade["minPrice"] - trade["entryPrice"]) * 10000

                # if market is forex and symbol contains JPY divide amtProfitMaxPips and amtProfitMinPips by 100
                if "JPY" in trade["symbol"] and market == "forex":
                    trade["amtProfitMaxPips"] = trade["amtProfitMaxPips"] / 100
                    trade["amtProfitMinPips"] = trade["amtProfitMinPips"] / 100
                trade["amtProfitMaxDateTimeUtc"] = candle["dateTimeUtc"] if trade["amtProfitMaxPct"] == change_max_pct else trade["amtProfitMaxDateTimeUtc"]
                trade["amtProfitMinDateTimeUtc"] = candle["dateTimeUtc"] if trade["amtProfitMinPct"] == change_min_pct else trade["amtProfitMinDateTimeUtc"]
                if candle["low"] <= trade["slPrice"] and trade["slDateTimeUtc"] is None:
                    # update starting balance
                    trade["isClosed"] = True
                    trade["exitPrice"] = trade["slPrice"]
                    trade["statusTrade"] = "loss" if trade["statusTrade"] == "open" else trade["statusTrade"]
                    trade["statusTarget"] = "Stop loss" if trade["statusTarget"] == "In Progress" else trade["statusTarget"]
                    trade["exitDateTimeUtc"] = candle["dateTimeUtc"]
                    trade["exitDateTimeEst"] = candle["dateTimeEst"]
                    trade["slDateTimeUtc"] = candle["dateTimeUtc"]
                    trade["slDateTimeEst"] = candle["dateTimeEst"]
                    if trade["isClosed"] == True and trade["tp1DateTimeUtc"] == None:
                        curr_bal = curr_bal + trade["amtTrade"] * trade["slPct"] * lev
                        avail_bal = avail_bal + trade["amtTrade"] + trade["amtTrade"] * trade["slPct"] * lev
                        min_bal = min(min_bal, curr_bal)
                        max_bal = max(max_bal, curr_bal)
                        trade["amtProfit"] = trade["amtTrade"] * trade["slPct"] * lev
                    if trade["isClosed"] == True and trade["tp1DateTimeUtc"] != None:
                        curr_bal = curr_bal + trade["amtTrade"] * trade["tp1Pct"] * lev
                        avail_bal = avail_bal + trade["amtTrade"] + trade["amtTrade"] * trade["tp1Pct"] * lev
                        min_bal = min(min_bal, curr_bal)
                        max_bal = max(max_bal, curr_bal)
                        trade["amtProfit"] = trade["amtTrade"] * trade["tp1Pct"] * lev
                    for trade_outcome in trade_outcomes:
                        if trade_outcome["symbol"] == trade["symbol"] and trade_outcome["entryDateTimeUtc"] == trade["entryDateTimeUtc"]:
                            trade_outcome = trade
                            break
                    else:
                        trade_outcomes.append(trade)
                    break
                if candle["high"] >= trade["tp1Price"] and trade["tp1DateTimeUtc"] is None:
                    trade["statusTrade"] = "win"
                    trade["statusTarget"] = "Target 1"
                    trade["tp1DateTimeUtc"] = candle["dateTimeUtc"]
                    trade["tp1DateTimeEst"] = candle["dateTimeEst"]
                    # update starting balance
                    if trade["isClosed"] == True:
                        curr_bal = curr_bal + trade["amtTrade"] * trade["tp1Pct"] * lev
                        avail_bal = avail_bal + trade["amtTrade"] + trade["amtTrade"] * trade["tp1Pct"] * lev
                        min_bal = min(min_bal, curr_bal)
                        max_bal = max(max_bal, curr_bal)
                        trade["amtProfit"] = trade["amtTrade"] * trade["tp1Pct"] * lev
                    for trade_outcome in trade_outcomes:
                        if trade_outcome["symbol"] == trade["symbol"] and trade_outcome["entryDateTimeUtc"] == trade["entryDateTimeUtc"]:
                            trade_outcome = trade
                            break
                    else:
                        trade_outcomes.append(trade)
                if candle["high"] >= trade["tp2Price"] and trade["tp2DateTimeUtc"] is None:
                    trade["statusTrade"] = "win"
                    trade["statusTarget"] = "Target 2"
                    trade["tp2DateTimeUtc"] = candle["dateTimeUtc"]
                    trade["tp2DateTimeEst"] = candle["dateTimeEst"]
                    trade["slPct"] = 0
                    trade["slPrice"] = trade["entryPrice"]
                    # update starting balance
                    if trade["isClosed"] == True:
                        curr_bal = curr_bal + trade["amtTrade"] * trade["tp1Pct"] * lev
                        avail_bal = avail_bal + trade["amtTrade"] + trade["amtTrade"] * trade["tp1Pct"] * lev
                        min_bal = min(min_bal, curr_bal)
                        max_bal = max(max_bal, curr_bal)
                        trade["amtProfit"] = trade["amtTrade"] * trade["tp1Pct"] * lev
                    for trade_outcome in trade_outcomes:
                        if trade_outcome["symbol"] == trade["symbol"] and trade_outcome["entryDateTimeUtc"] == trade["entryDateTimeUtc"]:
                            trade_outcome = trade
                            break
                if candle["high"] >= trade["tp3Price"] and trade["tp3DateTimeUtc"] is None:
                    trade["isClosed"] = True
                    trade["statusTrade"] = "win"
                    trade["statusTarget"] = "Target 3"
                    trade["exitPrice"] = trade["tp3Price"]
                    trade["tp3DateTimeUtc"] = candle["dateTimeUtc"]
                    trade["tp3DateTimeEst"] = candle["dateTimeEst"]
                    trade["exitDateTimeUtc"] = candle["dateTimeUtc"]
                    trade["exitDateTimeEst"] = candle["dateTimeEst"]
                    # update starting balance
                    if trade["isClosed"] == True:
                        curr_bal = curr_bal + trade["amtTrade"] * trade["tp1Pct"] * lev
                        avail_bal = avail_bal + trade["amtTrade"] + trade["amtTrade"] * trade["tp1Pct"] * lev
                        min_bal = min(min_bal, curr_bal)
                        max_bal = max(max_bal, curr_bal)
                        trade["amtProfit"] = trade["amtTrade"] * trade["tp1Pct"] * lev
                    for trade_outcome in trade_outcomes:
                        if trade_outcome["symbol"] == trade["symbol"] and trade_outcome["entryDateTimeUtc"] == trade["entryDateTimeUtc"]:
                            trade_outcome = trade
                            break
                    break
            # ----------------------------------- SHORT ---------------------------------- #
            if trade["entryType"] == "short" and trade["slDateTimeUtc"] is None:
                change_max_pct = (trade["entryPrice"] - candle["low"]) / trade["entryPrice"]
                change_min_pct = (trade["entryPrice"] - candle["high"]) / trade["entryPrice"]
                trade["amtProfitMaxPct"] = max(trade["amtProfitMaxPct"], change_max_pct)
                trade["amtProfitMinPct"] = min(trade["amtProfitMinPct"], change_min_pct)

                trade["maxPrice"] = min(trade["maxPrice"], candle["low"])
                trade["minPrice"] = max(trade["minPrice"], candle["high"])
                trade["amtProfitMaxPips"] = (trade["entryPrice"] - trade["maxPrice"]) * 10000
                trade["amtProfitMinPips"] = (trade["entryPrice"] - trade["minPrice"]) * 10000
                # if market is forex and symbol contains JPY divide amtProfitMaxPips and amtProfitMinPips by 100
                if "JPY" in trade["symbol"] and market == "forex":
                    trade["amtProfitMaxPips"] = trade["amtProfitMaxPips"] / 100
                    trade["amtProfitMinPips"] = trade["amtProfitMinPips"] / 100

                trade["amtProfitMaxDateTimeUtc"] = candle["dateTimeUtc"] if trade["amtProfitMaxPct"] == change_max_pct else trade["amtProfitMaxDateTimeUtc"]
                trade["amtProfitMinDateTimeUtc"] = candle["dateTimeUtc"] if trade["amtProfitMinPct"] == change_min_pct else trade["amtProfitMinDateTimeUtc"]
                if candle["high"] >= trade["slPrice"]:
                    trade["isClosed"] = True
                    trade["statusTrade"] = "loss" if trade["statusTrade"] == "open" else trade["statusTrade"]
                    trade["statusTarget"] = "Stop loss" if trade["statusTarget"] == "In Progress" else trade["statusTarget"]
                    trade["exitPrice"] = trade["slPrice"]
                    trade["exitDateTimeUtc"] = candle["dateTimeUtc"]
                    trade["exitDateTimeEst"] = candle["dateTimeEst"]
                    trade["slDateTimeUtc"] = candle["dateTimeUtc"]
                    trade["slDateTimeEst"] = candle["dateTimeEst"]
                    if trade["isClosed"] == True and trade["tp1DateTimeUtc"] == None:
                        curr_bal = curr_bal + trade["amtTrade"] * trade["slPct"] * lev
                        avail_bal = avail_bal + trade["amtTrade"] + trade["amtTrade"] * trade["slPct"] * lev
                        min_bal = min(min_bal, curr_bal)
                        max_bal = max(max_bal, curr_bal)
                        trade["amtProfit"] = trade["amtTrade"] * trade["slPct"] * lev
                    if trade["isClosed"] == True and trade["tp1DateTimeUtc"] != None:
                        curr_bal = curr_bal + trade["amtTrade"] * trade["tp1Pct"] * lev
                        avail_bal = avail_bal + trade["amtTrade"] + trade["amtTrade"] * trade["tp1Pct"] * lev
                        min_bal = min(min_bal, curr_bal)
                        max_bal = max(max_bal, curr_bal)
                        trade["amtProfit"] = trade["amtTrade"] * trade["tp1Pct"] * lev
                    for trade_outcome in trade_outcomes:
                        if trade_outcome["symbol"] == trade["symbol"] and trade_outcome["entryDateTimeUtc"] == trade["entryDateTimeUtc"]:
                            trade_outcome = trade
                            break
                    else:
                        trade_outcomes.append(trade)
                    break
                if candle["low"] <= trade["tp1Price"] and trade["tp1DateTimeUtc"] is None:
                    # update starting balance
                    trade["statusTrade"] = "win"
                    trade["statusTarget"] = "Target 1"
                    trade["tp1DateTimeUtc"] = candle["dateTimeUtc"]
                    trade["tp1DateTimeEst"] = candle["dateTimeEst"]
                    for trade_outcome in trade_outcomes:
                        if trade_outcome["symbol"] == trade["symbol"] and trade_outcome["entryDateTimeUtc"] == trade["entryDateTimeUtc"]:
                            trade_outcome = trade
                            break
                    else:
                        trade_outcomes.append(trade)
                    if trade["isClosed"] == True:
                        curr_bal = curr_bal + trade["amtTrade"] * trade["tp1Pct"] * lev
                        avail_bal = avail_bal + trade["amtTrade"] + trade["amtTrade"] * trade["tp1Pct"] * lev
                        min_bal = min(min_bal, curr_bal)
                        max_bal = max(max_bal, curr_bal)
                        trade["amtProfit"] = trade["amtTrade"] * trade["tp1Pct"] * lev
                if candle["low"] <= trade["tp2Price"] and trade["tp2DateTimeUtc"] is None:
                    trade["statusTrade"] = "win"
                    trade["statusTarget"] = "Target 2"
                    trade["tp2DateTimeUtc"] = candle["dateTimeUtc"]
                    trade["tp2DateTimeEst"] = candle["dateTimeEst"]
                    trade["slPct"] = 0
                    trade["slPrice"] = trade["entryPrice"]
                    if trade["isClosed"] == True:
                        curr_bal = curr_bal + trade["amtTrade"] * trade["tp1Pct"] * lev
                        avail_bal = avail_bal + trade["amtTrade"] + trade["amtTrade"] * trade["tp1Pct"] * lev
                        min_bal = min(min_bal, curr_bal)
                        max_bal = max(max_bal, curr_bal)
                        trade["amtProfit"] = trade["amtTrade"] * trade["tp1Pct"] * lev
                    for trade_outcome in trade_outcomes:
                        if trade_outcome["symbol"] == trade["symbol"] and trade_outcome["entryDateTimeUtc"] == trade["entryDateTimeUtc"]:
                            trade_outcome = trade
                            break
                if candle["low"] <= trade["tp3Price"] and trade["tp3DateTimeUtc"] is None:
                    trade["isClosed"] = True
                    trade["statusTrade"] = "win"
                    trade["statusTarget"] = "Target 3"
                    trade["exitPrice"] = trade["tp3Price"]
                    trade["tp3DateTimeUtc"] = candle["dateTimeUtc"]
                    trade["tp3DateTimeEst"] = candle["dateTimeEst"]
                    trade["exitDateTimeUtc"] = candle["dateTimeUtc"]
                    trade["exitDateTimeEst"] = candle["dateTimeEst"]
                    if trade["isClosed"] == True:
                        curr_bal = curr_bal + trade["amtTrade"] * trade["tp1Pct"] * lev
                        avail_bal = avail_bal + trade["amtTrade"] + trade["amtTrade"] * trade["tp1Pct"] * lev
                        min_bal = min(min_bal, curr_bal)
                        max_bal = max(max_bal, curr_bal)
                        trade["amtProfit"] = trade["amtTrade"] * trade["tp1Pct"] * lev
                    for trade_outcome in trade_outcomes:
                        if trade_outcome["symbol"] == trade["symbol"] and trade_outcome["entryDateTimeUtc"] == trade["entryDateTimeUtc"]:
                            trade_outcome = trade
                            break
                    break

        # update the active trades list
        active_trades_dict = [trade for trade in active_trades_dict if trade["isClosed"] == False]

        # -------------------------------- New Signals ------------------------------- #
        if len(active_trades_dict) < max_open_trades:
            new_signals = df_signals[df_signals["dateTimeUtc"] == current_time] if df_signals.shape[0] > 0 else pd.DataFrame()
            for _, row in new_signals.iterrows():

                # --- PRODUCTION  PREVENT OLD SIGNALS FROM BEING ADDED TO THE ACTIVE TRADES -- #
                if is_production == "True":
                    if row["dateTimeUtc"] < current_time_floor:
                        continue

                open_trades_symbols = [trade["symbol"] for trade in active_trades_dict]
                if len(active_trades_dict) < max_open_trades and row["symbol"] not in open_trades_symbols:
                    count_available_trades = max_open_trades - len(active_trades_dict)
                    amtTrade = avail_bal / count_available_trades if count_available_trades > 0 else 0
                    avail_bal = avail_bal - amtTrade
                    amtTradeStart = curr_bal
                    row_dict = row.to_dict()
                    active_trades_dict.append(
                        {
                            **row_dict,
                            "leverage": lev,
                            "isClosed": False,
                            "statusTrade": "open",
                            "entryDateTimeUtc": row["dateTimeUtc"],
                            "entryDateTimeEst": row["dateTimeEst"],
                            "exitDateTimeUtc": None,
                            "exitDateTimeEst": None,
                            "entryPrice": row["close"],
                            "exitPrice": None,
                            "lastCheckedDateTimeUtc": current_time,
                            "openTrades": len(active_trades_dict) + 1,
                            "amtAvailable": avail_bal,
                            "amtTradeStart": amtTradeStart,
                            "amtTrade": amtTrade,
                            "amtProfit": 0,
                        }
                    )

    df_trade_outcomes = pd.DataFrame(trade_outcomes)
    if df_trade_outcomes.shape[0] > 0:
        df_trade_outcomes["tradeDurationSeconds"] = df_trade_outcomes["lastCheckedDateTimeUtc"] - df_trade_outcomes["entryDateTimeUtc"]
        df_trade_outcomes["tradeDurationSeconds"] = df_trade_outcomes["tradeDurationSeconds"].dt.total_seconds().astype(int)
        df_trade_outcomes["tradeDurationStr"] = df_trade_outcomes.apply(lambda x: get_trades_duration_from_seconds(x["tradeDurationSeconds"]), axis=1)

    df_active_trades = pd.DataFrame(active_trades_dict)

    get_results_table(df_trades_outcomes=df_trade_outcomes, starting_bal=starting_bal, current_bal=curr_bal, min_bal=min_bal, max_bal=max_bal, active_trades=active_trades_dict)
    get_signals_csv(df_trade_outcomes, "_project/data_results/df_signals.csv")

    df_trade_outcomes.replace([np.inf, -np.inf, np.nan], None, inplace=True)
    df_active_trades.replace([np.inf, -np.inf, np.nan], None, inplace=True)
    # sort the dataframe by entryDateTimeUtc news first
    df_trade_outcomes = df_trade_outcomes.sort_values(by="entryDateTimeUtc", ascending=False) if df_trade_outcomes.shape[0] > 0 else df_trade_outcomes
    df_active_trades = df_active_trades.sort_values(by="entryDateTimeUtc", ascending=False) if df_active_trades.shape[0] > 0 else df_active_trades
    df_closed_trades = df_trade_outcomes[df_trade_outcomes["isClosed"] == True] if df_trade_outcomes.shape[0] > 0 else pd.DataFrame()
    df_active_trades_dict = df_active_trades[signals_columns].to_dict(orient="records") if df_active_trades.shape[0] > 0 else []
    df_closed_trades_dict = df_closed_trades[signals_columns].to_dict(orient="records") if df_closed_trades.shape[0] > 0 else []

    return {
        "signalsClosed": df_closed_trades_dict,
        "signalsActive": df_active_trades_dict,
    }


def get_signals_csv(df_trade_outcomes: pd.DataFrame, fileName: str):
    if is_production == "True":
        return
    try:
        columns = [
            "entryDateTimeEst",
            "exitDateTimeEst",
            "lastCheckedDateTimeUtc",
            "leverage",
            "symbol",
            "timeframe",
            "entryType",
            "tp1Pct",
            "tp1Price",
            "tp1DateTimeEst",
            "tp2Pct",
            "tp2Price",
            "tp2DateTimeEst",
            "tp3Pct",
            "tp3Price",
            "tp3DateTimeEst",
            "slPct",
            "slDateTimeEst",
            "slPrice",
            "tradeDurationStr",
            "statusTrade",
            "entryPrice",
            "exitPrice",
            "openTrades",
            "amtTradeStart",
            "amtTrade",
            "amtProfit",
            "amtProfitMaxPct",
            "amtProfitMinPct",
            "amtProfitMaxDateTimeUtc",
            "amtProfitMinDateTimeUtc",
            "isClosed",
        ]
        # add missing columns only of they are not in the dataframe
        for column in columns:
            if column not in df_trade_outcomes.columns:
                df_trade_outcomes[column] = None
        df_trade_outcomes[columns].to_csv(fileName, index=False) if df_trade_outcomes.shape[0] > 0 else None
    except Exception as e:
        print(f"An error occurred while saving the dataframe to csv: {e}")


def get_results_table(df_trades_outcomes: pd.DataFrame, active_trades: pd.DataFrame, starting_bal: float, current_bal: float, min_bal: float, max_bal: float):
    try:
        if is_production == "True":
            return
        if len(df_trades_outcomes) == 0 and len(active_trades) == 0:
            print("No trades to show")
            return
        if len(df_trades_outcomes) == 0:
            print("No trades to show")
            return

        count_total = len(df_trades_outcomes)
        count_wins = len(df_trades_outcomes[df_trades_outcomes["statusTrade"] == "win"])
        win_pct = (count_wins / count_total if count_total > 0 else 0) * 100
        count_losses = len(df_trades_outcomes[df_trades_outcomes["statusTrade"] == "loss"])
        loss_pct = (count_losses / count_total if count_total > 0 else 0) * 100
        average_duration = df_trades_outcomes[df_trades_outcomes["isClosed"] == True]["tradeDurationSeconds"].mean()
        average_duration_str = get_trades_duration_from_seconds(average_duration)
        first_trade_datetime = df_trades_outcomes.head(1)["entryDateTimeUtc"].values[0]
        last_trade_datetime = df_trades_outcomes.tail(1)["entryDateTimeUtc"].values[0]
        first_trade_datetime = pd.to_datetime(first_trade_datetime)
        last_trade_datetime = pd.to_datetime(last_trade_datetime)
        first_trade_datetime_str = first_trade_datetime.strftime("%Y-%m-%d %H:%M:%S")
        last_trade_datetime_str = last_trade_datetime.strftime("%Y-%m-%d %H:%M:%S")
        trading_days = last_trade_datetime - first_trade_datetime
        trading_days_str = get_trades_duration_from_seconds(trading_days.total_seconds())

        headers = ["Activity", "Result"]
        rows = [
            ["Trades", count_total],
            ["Wins", count_wins],
            ["Win %", win_pct],
            ["Losses", count_losses],
            ["Loss %", loss_pct],
            ["Open Trades", len(active_trades)],
            ["Avg Duration", average_duration_str],
            ["Trading Days", trading_days_str],
            ["First Trade", first_trade_datetime_str],
            ["Last Trade", last_trade_datetime_str],
        ]

        print(tabulate(rows, headers=headers, tablefmt="outline", colalign=("left",), floatfmt=".2f"))

        headers = ["Activity", "Result"]
        rows = [["startingBalance", starting_bal], ["minBalance", min_bal], ["maxBalance", max_bal], ["currentBalance", current_bal]]

        print(tabulate(rows, headers=headers, tablefmt="outline", colalign=("left",), floatfmt=".2f"))

        date_ranges_months = get_dates_months(first_trade_datetime, last_trade_datetime)
        trades_months = []
        headers_trade_months = [
            "Month",
            "Profit",
            "Ave Amt",
            "Trades",
            "Win %",
            "Long Trades",
            "Long Win %",
            "Short Trades",
            "Short Win %",
            "Avg Duration",
        ]
        for date_range in date_ranges_months:
            trades_month = df_trades_outcomes[(df_trades_outcomes["entryDateTimeUtc"] >= date_range["start"]) & (df_trades_outcomes["entryDateTimeUtc"] <= date_range["end"])]
            count_total = len(trades_month)
            count_wins = len(trades_month[trades_month["statusTrade"] == "win"])
            win_pct = (count_wins / count_total if count_total > 0 else 0) * 100
            count_long = len(trades_month[trades_month["entryType"] == "long"])
            count_short = len(trades_month[trades_month["entryType"] == "short"])
            win_pct_long = (len(trades_month[(trades_month["entryType"] == "long") & (trades_month["statusTrade"] == "win")]) / count_long if count_long > 0 else 0) * 100
            win_pct_short = (len(trades_month[(trades_month["entryType"] == "short") & (trades_month["statusTrade"] == "win")]) / count_short if count_short > 0 else 0) * 100
            average_duration = trades_month[trades_month["isClosed"] == True]["tradeDurationSeconds"].mean()
            average_duration_str = get_trades_duration_from_seconds(average_duration)
            amtProfit = trades_month[trades_month["isClosed"] == True]["amtProfit"].sum()
            ave_amount = trades_month[trades_month["isClosed"] == True]["amtTrade"].mean()
            trades_months.append(
                [
                    date_range["start"].strftime("%Y-%m"),
                    amtProfit,
                    ave_amount,
                    count_total,
                    win_pct,
                    count_long,
                    win_pct_long,
                    count_short,
                    win_pct_short,
                    average_duration_str,
                ]
            )

        print(tabulate(trades_months, headers=headers_trade_months, tablefmt="outline", colalign=("left",), floatfmt=".2f"))

        headers_symbols = ["Symbol", "Profit", "Ave Amt", "Trades", "Win %", "Long Trades", "Long Win %", "Short Trades", "Short Win %", "Avg Duration"]
        trades_symbols = []
        symbols = df_trades_outcomes["symbol"].unique()
        for symbol in symbols:
            trades_by_symbol = df_trades_outcomes[df_trades_outcomes["symbol"] == symbol]
            trades_by_symbol = trades_by_symbol[trades_by_symbol["isClosed"] == True]
            count_total = len(trades_by_symbol)
            count_wins = len(trades_by_symbol[trades_by_symbol["statusTrade"] == "win"])
            win_pct = (count_wins / count_total if count_total > 0 else 0) * 100
            count_long = len(trades_by_symbol[trades_by_symbol["entryType"] == "long"])
            count_short = len(trades_by_symbol[trades_by_symbol["entryType"] == "short"])
            win_pct_long = (len(trades_by_symbol[(trades_by_symbol["entryType"] == "long") & (trades_by_symbol["statusTrade"] == "win")]) / count_long if count_long > 0 else 0) * 100
            win_pct_short = (
                len(trades_by_symbol[(trades_by_symbol["entryType"] == "short") & (trades_by_symbol["statusTrade"] == "win")]) / count_short if count_short > 0 else 0
            ) * 100
            average_duration = trades_by_symbol[trades_by_symbol["isClosed"] == True]["tradeDurationSeconds"].mean()
            average_duration_str = get_trades_duration_from_seconds(average_duration)
            amtProfit = trades_by_symbol[trades_by_symbol["isClosed"] == True]["amtProfit"].sum()
            ave_amount = trades_by_symbol[trades_by_symbol["isClosed"] == True]["amtTrade"].mean()
            trades_symbols.append(
                [
                    symbol,
                    amtProfit,
                    ave_amount,
                    count_total,
                    win_pct,
                    count_long,
                    win_pct_long,
                    count_short,
                    win_pct_short,
                    average_duration_str,
                ]
            )
        # remove where count_total < 1
        trades_symbols = [trade for trade in trades_symbols if trade[3] > 0]
        trades_symbols = sorted(trades_symbols, key=lambda x: x[1], reverse=True)
        print(tabulate(trades_symbols, headers=headers_symbols, tablefmt="outline", colalign=("left",), floatfmt=".2f"))
    except Exception as e:
        print(f"An error occurred get_results_table: {e}")
