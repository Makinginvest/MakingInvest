import asyncio
from datetime import datetime, timedelta
import numpy as np


import pandas as pd
from app.helpers.a_functions.crypto__functions import get_USDT_symbols_by_value
from app.helpers.a_functions.dev_print import dev_print
from app.helpers.a_functions.get_signal_result import get_signal_result

from app.helpers.a_functions.get_signals_performance import get_print_performance_summary
from app.helpers.a_functions.get_validate_generate_signals import get_validate_generate_signals
from app.helpers.a_functions.notifications_periods4 import handle_all_notifications
from app.helpers.a_functions_mongodb.a_mongodb_client import get_current_live_signals_from_mongodb, update_signals_by_symbol

from app.helpers.a_functions_mongodb.a_signals_aggr_update import update_signals_aggr, validate_firestore_update
from app.helpers.engines.signals_forex_live1.forex_strat_macd_long_live1 import get_signals_forex_long_live1
from app.helpers.engines.signals_forex_live1.forex_strat_macd_short_live1 import get_signals_forex_short_live1
from app.models.signal_model import get_columns_signals


async def get_signals_forex_all_live1(useOldSignal=True):
    current_time = datetime.utcnow()
    current_time_floor = pd.Timestamp(current_time).floor("15min")
    name = "signals_forex_v1"
    signalsCollection = "sSignalsForexTest"
    histCollection = "historicalForex"
    nameVersion = "1.0.0"
    firestore_col_name = "sSignalsAggrOpenTest"
    firestore_doc_name = "forex_v1"
    useOldSignal = useOldSignal
    nameType = "Forex"
    nameSort = 3
    noti_heading = "FOREX"
    is_risky = False
    datetime_start = datetime.utcnow() - pd.Timedelta(days=30 * 1.5)
    datetime_end = datetime.utcnow() - pd.Timedelta(days=90)
    datetime_end = None
    nameMarket = "Forex"
    periods = 4

    if useOldSignal == True:
        # datetime_start = datetime.utcnow() - pd.Timedelta(days=30 * 5.5)
        datetime_start = datetime.utcnow() - pd.Timedelta(days=30 * 1)
        signalsCollection = "signalsForex"
        firestore_col_name = "signalsAggrOpen_V2"

    did_gen_signals = get_validate_generate_signals(useOldSignal=useOldSignal, floor="30min", floor_factor=15)

    dev_print("did_gen_signals: ", did_gen_signals)

    data_length = int(420) if useOldSignal else 420
    data_length = int(420) if useOldSignal else 420

    try:
        s_long = await get_USDT_symbols_by_value("_datasets/data/_data_symbols_forex_oanda_main.csv")
        s_long = s_long[:50]
        # s_long = ["EURCZK"]

        s_short = await get_USDT_symbols_by_value("_datasets/data/_data_symbols_forex_oanda_main.csv")
        s_short = s_short[:50]
        # s_short = ["EURCZK"]

        df = pd.DataFrame()

        tasks_long = [
            get_signals_forex_long_live1(
                timeframe="30m",
                symbols=s_long,
                data_length=data_length,
                isEnabled=did_gen_signals,
                datetime_start=datetime_start,
                datetime_end=datetime_end,
                lookback=5,
            ),
        ]

        tasks_short = [
            get_signals_forex_short_live1(
                timeframe="30m",
                symbols=s_short,
                data_length=data_length,
                isEnabled=did_gen_signals,
                datetime_start=datetime_start,
                datetime_end=datetime_end,
                lookback=5,
            ),
        ]

        tasks = tasks_long + tasks_short

        res1, res2 = await asyncio.gather(*tasks)
        df = df.append(res1, ignore_index=True)
        df = df.append(res2, ignore_index=True)

        # JPY fix if symbol contains JPY or jpy divide takeProfit1Pips by 100
        if df.shape[0] > 0:
            df.loc[df["symbol"].str.contains("JPY", case=False), "takeProfit1Pips"] = df["takeProfit1Pips"] / 100
            df.loc[df["symbol"].str.contains("JPY", case=False), "takeProfit2Pips"] = df["takeProfit2Pips"] / 100
            df.loc[df["symbol"].str.contains("JPY", case=False), "takeProfit3Pips"] = df["takeProfit3Pips"] / 100
            df.loc[df["symbol"].str.contains("JPY", case=False), "takeProfit4Pips"] = df["takeProfit4Pips"] / 100
            df.loc[df["symbol"].str.contains("JPY", case=False), "stopLossPips"] = df["stopLossPips"] / 100
            df.loc[df["symbol"].str.contains("JPY", case=False), "highestPct"] = df["highestPct"] / 100

        if df.shape[0] > 0:
            current_time = datetime.utcnow()
            df = df[df["entryDateTimeUtc"] <= current_time]
            df["signalName"] = name
            df["lastCheckDateTimeUtc"] = df["entryDateTimeUtc"]
            df["lastCheckDateTimeEst"] = df["entryDateTimeEst"]
            df["time"] = df["entryDateTimeUtc"]
            df.index = df["time"]
            df = df.drop(columns=["time"])
            df["isNew"] = True

        # pull current live signals
        current_df = await get_current_live_signals_from_mongodb(name=name, nameVersion=nameVersion, useOldSignal=useOldSignal, signalsCollection=signalsCollection)
        df = df.append(current_df, ignore_index=True)
        df = df.drop_duplicates(subset=["symbol", "entryDateTimeUtc"], keep="last")

        if df.shape[0] == 0:
            return []

        df_list = []
        for symbol in df["symbol"].unique():
            df_list.append(df[df["symbol"] == symbol])

        df_res = pd.DataFrame()
        df_list = [x.sort_values(by=["entryDateTimeUtc"], ascending=False) for x in df_list]

        for i in range(0, len(df_list), 8):
            batch = df_list[i : i + 8]
            tasks_long = [get_signal_result(df, histCollection=histCollection, stop_lost_update_level=3, open_new_positions_level_int=3) for df in batch]
            res = await asyncio.gather(*tasks_long)

            for df in res:
                df_res = df_res.append(df, ignore_index=True)

        df_res = df_res.replace({pd.NaT: None})
        df_res = df_res[get_columns_signals]
        df_res = df_res.sort_values(by=["entryDateTimeUtc"], ascending=False)

        df_res["hasFutures"] = False

        # Close dead signals there are where lastCheckDateTimeUtc is less than 1 day ago set isClosed to True
        df_res["isClosed"] = df_res.apply(
            lambda x: True if x["lastCheckDateTimeUtc"] < current_time_floor - timedelta(days=1) and not x["isClosed"] else x["isClosed"], axis=1
        )
        df_res["entryAllowNewSignalDateTimeUtc"] = df_res.apply(
            lambda x: current_time_floor if x["isClosed"] and x["entryAllowNewSignalDateTimeUtc"] is None else x["entryAllowNewSignalDateTimeUtc"], axis=1
        )

        # convert all NaN to None
        df_res = df_res.replace({np.nan: None})

        df_open = df_res[df_res["isClosed"] == False]

        df_res_long = df_res[df_res["entryType"] == "long"]
        df_res_short = df_res[df_res["entryType"] == "short"]
        get_print_performance_summary(df_res_long, is_long=True)
        get_print_performance_summary(df_res_short, is_long=False)

        await asyncio.create_task(
            update_signals_by_symbol(
                baseCollection=signalsCollection,
                data=df_res.to_dict("records"),
                name=name,
                nameVersion=nameVersion,
                useOldSignal=useOldSignal,
                current_time_floor=current_time_floor,
            )
        )

        update_firestore = validate_firestore_update(
            df_res=df_res, useOldSignal=useOldSignal, did_gen_signals=did_gen_signals, current_time_floor=current_time_floor
        )
        if update_firestore:
            await update_signals_aggr(
                firestore_col_name=firestore_col_name,
                firestore_doc_name=firestore_doc_name,
                name=name,
                nameType=nameType,
                nameSort=nameSort,
                nameVersion=nameVersion,
                signalsCollection=signalsCollection,
                did_gen_signals=did_gen_signals,
                is_risky=is_risky,
                nameMarket=nameMarket,
            )

        # print signals where entryResult == 'in progress' and entryType == 'long'

        df_pending_long = df_open[(df_open["entryResult"] == "in progress") & (df_open["entryType"] == "long")]
        df_pending_short = df_open[(df_open["entryResult"] == "in progress") & (df_open["entryType"] == "short")]

        dev_print("Open Signals: ", len(df_open))
        dev_print("Pending Long Signals: ", len(df_pending_long))
        dev_print("Pending Short Signals: ", len(df_pending_short))

        asyncio.create_task(handle_all_notifications(signals=df_res, current_time_tp_sl=current_time_floor, noti_heading=noti_heading, name=name))

        return df_res.to_dict("records") if df.shape[0] > 0 else []

    except Exception as e:
        print(f"Error in get_signals_all: {e}")
        return []
