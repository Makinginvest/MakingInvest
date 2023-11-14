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
from app.helpers.engines.signals_stocks_live1.stocks_strat_macd_long_live1 import get_signals_stocks_long_live1
from app.helpers.engines.signals_stocks_live1.stocks_strat_macd_short_live1 import get_signals_stocks_short_live1


from app.models.signal_model import get_columns_signals


async def get_signals_stocks_all_live1(useOldSignal=True):
    current_time = datetime.utcnow()
    current_time_floor = pd.Timestamp(current_time).floor("15min")
    name = "signals_stocks_v1"
    signalsCollection = "sSignalsStocksTest"
    histCollection = "historicalStocks"
    nameVersion = "1.0.0"
    firestore_col_name = "sSignalsAggrOpenTest"
    firestore_doc_name = "stocks_v1"
    nameType = "Stocks"
    nameSort = 4
    noti_heading = "STOCKS"
    useOldSignal = useOldSignal
    is_risky = False
    datetime_start = datetime.utcnow() - pd.Timedelta(days=30 * 1.5)
    datetime_end = datetime.utcnow() - pd.Timedelta(days=90)
    datetime_end = None
    nameMarket = "stocks"

    if useOldSignal == True:
        # datetime_start = datetime.utcnow() - pd.Timedelta(days=30 * 5.5)
        datetime_start = datetime.utcnow() - pd.Timedelta(days=30 * 1)
        signalsCollection = "signalsStocks"
        firestore_col_name = "signalsAggrOpen_V2"

    did_gen_signals = get_validate_generate_signals(useOldSignal=useOldSignal, floor="1h", floor_factor=15)

    dev_print("did_gen_signals: ", did_gen_signals)

    data_length = int(320) if useOldSignal else int(320)

    try:
        s_long_nasdaq = await get_USDT_symbols_by_value("_datasets/data/_data_symbols_stock_nasdaq_100.csv")
        s_long_sp = await get_USDT_symbols_by_value("_datasets/data/_data_symbols_stock_options_sp500.csv")
        s_long = s_long_nasdaq + s_long_sp[:300]
        s_long = list(dict.fromkeys(s_long))
        s_long = s_long[:250]
        # s_long = s_long_nasdaq
        # s_long = ["TSLA"]

        s_short_nasdaq = await get_USDT_symbols_by_value("_datasets/data/_data_symbols_stock_nasdaq_100.csv")
        s_short_sp = await get_USDT_symbols_by_value("_datasets/data/_data_symbols_stock_options_sp500.csv")
        s_short = s_short_nasdaq + s_short_sp[:300]
        s_short = list(dict.fromkeys(s_short))
        s_short = s_short[:250]
        # s_short = s_short_nasdaq
        # s_short = ["TSLA"]

        df = pd.DataFrame()

        tasks_long = [
            get_signals_stocks_long_live1(
                timeframe="1h",
                symbols=s_long,
                data_length=data_length,
                isEnabled=did_gen_signals,
                datetime_start=datetime_start,
                datetime_end=datetime_end,
                lookback=5,
            ),
        ]

        tasks_short = [
            get_signals_stocks_short_live1(
                timeframe="1h",
                symbols=s_short,
                data_length=data_length,
                isEnabled=did_gen_signals,
                datetime_start=datetime_start,
                datetime_end=datetime_end,
                lookback=5,
            ),
        ]

        tasks = tasks_long + tasks_short

        (res1, res2) = await asyncio.gather(*tasks)
        df = df.append(res1, ignore_index=True)
        df = df.append(res2, ignore_index=True)

        if df.shape[0] > 0:
            # remove entries where entryDateTimeUtc is greater than current time utc
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

        symbols_with_futures = get_crypto_symbols_with_futures()
        df_res["hasFutures"] = df_res["symbol"].apply(lambda x: True if x in symbols_with_futures else False)
        df_res["hasFutures"] = False

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

        return {
            "performance": res_performance,
            "signals": res_df,
        }

    except Exception as e:
        print(f"Error in get_signals_all: {e}")
        return []
