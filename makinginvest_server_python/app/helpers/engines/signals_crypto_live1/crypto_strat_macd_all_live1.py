import asyncio
from datetime import datetime, timedelta
import numpy as np

import pandas as pd
from app.helpers.a_functions.crypto__functions import get_crypto_symbols_with_futures, get_USDT_symbols_by_value
from app.helpers.a_functions.dev_print import dev_print
from app.helpers.a_functions.get_signal_result import get_signal_result, get_signal_result

from app.helpers.a_functions.get_signals_performance import get_print_performance_summary
from app.helpers.a_functions.get_signals_summary import get_closed_signals_results_summary
from app.helpers.a_functions.get_validate_generate_signals import get_validate_generate_signals
from app.helpers.a_functions.notifications_periods4 import handle_all_notifications
from app.helpers.a_functions_mongodb.a_mongodb_client import get_current_live_signals_from_mongodb, update_signals_by_symbol

from app.helpers.a_functions_mongodb.a_signals_aggr_update import update_signals_aggr, validate_firestore_update
from app.helpers.engines.signals_crypto_live1.crypto_strat_macd_long_live1 import get_signals_crypto_long_live1
from app.helpers.engines.signals_crypto_live1.crypto_strat_macd_short_live1 import get_signals_crypto_short_live1


from app.models.signal_model import get_columns_signals


async def get_signals_crypto_all_live1(useOldSignal=True):
    current_time = datetime.utcnow()
    current_time_floor = pd.Timestamp(current_time).floor("15min")
    name = "signals_crypto_v1"
    signalsCollection = "sSignalsCryptoTest"
    histCollection = "historicalCrypto"
    nameVersion = "1.0.0"
    firestore_col_name = "sSignalsAggrOpenTest"
    firestore_doc_name = "crypto_v1"
    nameType = "Crypto"
    nameTypeSubtitle = ""
    nameSort = 1
    noti_heading = "CRYPTO"
    useOldSignal = useOldSignal
    is_risky = False
    datetime_start = datetime.utcnow() - pd.Timedelta(days=30 * 1.5)
    datetime_end = datetime.utcnow() - pd.Timedelta(days=30)
    datetime_end = None
    nameMarket = "crypto"

    if useOldSignal == False:
        datetime_start = datetime.utcnow() - pd.Timedelta(days=30 * 5.5)
        # datetime_start = datetime.utcnow() - pd.Timedelta(days=30 * 1)
        signalsCollection = "signalsCrypto"
        firestore_col_name = "signalsAggrOpen_V2"

    did_gen_signals = get_validate_generate_signals(useOldSignal=useOldSignal, floor="4h", floor_factor=15)

    dev_print("did_gen_signals: ", did_gen_signals)

    data_length = int(320) if useOldSignal else int(320)

    try:
        f_symbols = get_crypto_symbols_with_futures()

        s_long = await get_USDT_symbols_by_value("_datasets/data/_data_symbols_crypto_usdt_busd_futures.csv")
        s_long = [x for x in s_long if x in f_symbols]
        # s_long = ["DOTUSDT", "INJUSDT", "ICPUSDT", "SPELLUSDT", "ZILUSDT", "MINAUSDT", "AXSUSDT", "REEFUSDT"]
        # s_long = ["IOSTUSDT"]
        s_long = s_long[:200]

        s_short = await get_USDT_symbols_by_value("_datasets/data/_data_symbols_crypto_usdt_busd_futures.csv")
        s_short = [x for x in s_short if x in f_symbols]
        # s_short = ["DOTUSDT", "INJUSDT", "ICPUSDT", "SPELLUSDT", "ZILUSDT", "MINAUSDT", "AXSUSDT", "REEFUSDT"]
        # s_short = ["IOSTUSDT"]
        s_short = s_short[:200]

        df = pd.DataFrame()

        tasks = [
            get_signals_crypto_long_live1(
                timeframe="4h",
                symbols=s_long,
                data_length=data_length,
                isEnabled=did_gen_signals,
                datetime_start=datetime_start,
                datetime_end=datetime_end,
                lookback=2,
            ),
        ]

        tasks_short = [
            get_signals_crypto_short_live1(
                timeframe="4h",
                symbols=s_short,
                data_length=data_length,
                isEnabled=did_gen_signals,
                datetime_start=datetime_start,
                datetime_end=datetime_end,
                lookback=2,
            ),
        ]

        tasks = tasks + tasks_short

        (res1, res2) = await asyncio.gather(*tasks)
        df = df.append(res1, ignore_index=True)
        df = df.append(res2, ignore_index=True)

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
            tasks = [get_signal_result(df, histCollection=histCollection, stop_lost_update_level=3, open_new_positions_level_int=3) for df in batch]
            res = await asyncio.gather(*tasks)

            for df in res:
                df_res = df_res.append(df, ignore_index=True)

        df_res = df_res.replace({pd.NaT: None})
        df_res = df_res[get_columns_signals]
        df_res = df_res.sort_values(by=["entryDateTimeUtc"], ascending=False)

        symbols_with_futures = get_crypto_symbols_with_futures()
        df_res["hasFutures"] = df_res["symbol"].apply(lambda x: True if x in symbols_with_futures else False)

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
                nameTypeSubtitle=nameTypeSubtitle,
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
        df_with_futures = df_res[df_res["hasFutures"] == True]
        dev_print("Open Signals: ", len(df_open))
        dev_print("Signals Futures: ", len(df_with_futures))
        dev_print("Pending Long Signals: ", len(df_pending_long))
        dev_print("Pending Short Signals: ", len(df_pending_short))

        asyncio.create_task(handle_all_notifications(signals=df_res, current_time_tp_sl=current_time_floor, noti_heading=noti_heading, name=name))

        start_date = datetime.now() - timedelta(days=30 * 13)
        end_date = datetime.now()
        res_performance = await get_closed_signals_results_summary(signalsCollection, name, nameVersion, start_date, end_date)
        res_df = df_res.to_dict("records") if df.shape[0] > 0 else []

        for d in res_df:
            del d["entryAllowNewSignalDateTimeEst"]
            del d["entryAllowNewSignalDateTimeUtc"]

        return {
            "performance": res_performance,
            "signals": res_df,
        }

    except Exception as e:
        print(f"Error in get_signals_all: {e}")
        return []
