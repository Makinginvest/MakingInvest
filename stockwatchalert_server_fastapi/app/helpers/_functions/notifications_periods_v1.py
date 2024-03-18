import asyncio
import os
from firebase_admin import messaging
import pandas as pd
from app._database.db_connect_client import database_mongodb_client

from dotenv import load_dotenv

from app.helpers._functions.dev_print_v1 import dev_print

load_dotenv()
is_production = os.getenv("PRODUCTION", "False")


async def handle_all_notifications_v1(signals_df: pd.DataFrame = None, current_time_tp_sl=None, noti_heading: str = "Signal Update", nameId: str = None):
    try:
        if len(signals_df) == 0:
            return
        signals_tp1 = signals_df[signals_df["tp1DateTimeUtc"] == current_time_tp_sl]
        signals_tp2 = signals_df[signals_df["tp2DateTimeUtc"] == current_time_tp_sl]
        signals_tp3 = signals_df[signals_df["tp3DateTimeUtc"] == current_time_tp_sl]

        signals_sl = signals_df[signals_df["slDateTimeUtc"] == current_time_tp_sl]
        signals_sl_after_tp0 = signals_sl[signals_sl["tp1DateTimeUtc"] == None]
        signals_sl_after_tp1 = signals_sl[signals_sl["tp1DateTimeUtc"] != None]
        signals_sl_after_tp2 = signals_sl[signals_sl["tp2DateTimeUtc"] != None]

        signals_tp1_dict = signals_tp1.to_dict("records") if signals_tp1.shape[0] > 0 else []
        signals_tp2_dict = signals_tp2.to_dict("records") if signals_tp2.shape[0] > 0 else []
        signals_tp3_dict = signals_tp3.to_dict("records") if signals_tp3.shape[0] > 0 else []
        signals_sl_after_tp0_dict = signals_sl_after_tp0.to_dict("records") if signals_sl_after_tp0.shape[0] > 0 else []
        signals_sl_after_tp1_dict = signals_sl_after_tp1.to_dict("records") if signals_sl_after_tp1.shape[0] > 0 else []
        signals_sl_after_tp2_dict = signals_sl_after_tp2.to_dict("records") if signals_sl_after_tp2.shape[0] > 0 else []

        signals_new = signals_df[signals_df["entryDateTimeUtc"] == current_time_tp_sl]
        signals_new_dict = signals_new.to_dict("records") if signals_new.shape[0] > 0 else []

        await asyncio.create_task(send_signal_notification_to_all_tp_sl_v1(signals=signals_new_dict, text="new", noti_heading=noti_heading, nameId=nameId))
        await asyncio.create_task(send_signal_notification_to_all_tp_sl_v1(signals=signals_tp1_dict, text="tp1", noti_heading=noti_heading, nameId=nameId))
        await asyncio.create_task(send_signal_notification_to_all_tp_sl_v1(signals=signals_tp2_dict, text="tp2", noti_heading=noti_heading, nameId=nameId))
        await asyncio.create_task(send_signal_notification_to_all_tp_sl_v1(signals=signals_tp3_dict, text="tp3", noti_heading=noti_heading, nameId=nameId))
        await asyncio.create_task(send_signal_notification_to_all_tp_sl_v1(signals=signals_sl_after_tp0_dict, text="sl0", noti_heading=noti_heading, nameId=nameId))
        await asyncio.create_task(send_signal_notification_to_all_tp_sl_v1(signals=signals_sl_after_tp1_dict, text="sl1", noti_heading=noti_heading, nameId=nameId))
        await asyncio.create_task(send_signal_notification_to_all_tp_sl_v1(signals=signals_sl_after_tp2_dict, text="sl2", noti_heading=noti_heading, nameId=nameId))

        dev_print(f"signals_new_dict: {len(signals_new_dict)}")
        dev_print(f"signals_tp1_dict: {len(signals_tp1_dict)}")
        dev_print(f"signals_tp2_dict: {len(signals_tp2_dict)}")
        dev_print(f"signals_tp3_dict: {len(signals_tp3_dict)}")
        #
        dev_print(f"signals_sl_after_tp1_dict: {len(signals_sl_after_tp1_dict)}")
        dev_print(f"signals_sl_after_tp2_dict: {len(signals_sl_after_tp2_dict)}")
        dev_print(f"signals_sl_after_tp0_dict: {len(signals_sl_after_tp0_dict)}")
    except Exception as e:
        print(f"An error occurred handle_all_notifications_v1: {e}")


async def send_signal_notification_to_all_tp_sl_v1(signals: list = None, text: str = "tp1", noti_heading: str = "Signal Update", nameId: str = None):
    if is_production != "True":
        return False

    if signals == []:
        return

    try:
        user_collection = database_mongodb_client[f"users"]
        users: list = await user_collection.find(
            {
                "appBuildNumber": {"$gte": 1000},
                "notificationsDisabled": {"$nin": [nameId]},
            }
        ).to_list(length=100000)
        user_with_notifications_enabled = []

        for user in users:
            if "isNotificationsEnabledGeneral" not in user:
                user["isNotificationsEnabledGeneral"] = True

            if user["isNotificationsEnabledGeneral"] != False:
                user_with_notifications_enabled.append(user)

        registration_tokens = []
        for user in user_with_notifications_enabled:
            registration_tokens.append(user["devTokens"])

        registration_tokens = [item for sublist in registration_tokens for item in sublist]
        registration_tokens = list(set(registration_tokens))

        if registration_tokens == []:
            return

        for signal in signals:
            _registration_tokens = [registration_tokens[i : i + 500] for i in range(0, len(registration_tokens), 500)]

            for token_chunk in _registration_tokens:
                signal_type = "LONG" if signal["entryType"] == "long" else "SHORT"
                is_forex = True if signal["market"] == "forex" else False
                body = ""
                if text == "new":
                    body = f'New signal ${signal["symbol"]}, check details in app \n🚀'
                if text == "tp1":
                    body = f'✅ Target 1 done with {get_pct(pct=signal["tp1Pct"], pips=signal["tp1Pips"], is_forex=is_forex)} \n🚀 {signal_type}'
                if text == "tp2":
                    body = f'✅ Target 2 done with {get_pct(pct=signal["tp2Pct"], pips=signal["tp2Pips"], is_forex=is_forex)} \n🚀 {signal_type}'
                if text == "tp3":
                    body = f'✅ Target 3 done with {get_pct(pct=signal["tp3Pct"], pips=signal["tp3Pips"], is_forex=is_forex)} \n🚀 {signal_type}'
                if text == "sl0":
                    body = f'⛔ Stop loss \nLoss: {get_pct(pct=signal["slPct"], pips=signal["slPips"], is_forex=is_forex)} \n🚀 {signal_type}'
                if text == "sl1":
                    body = f'✅ Signal closed. \nMinimum profit: {get_pct(pct=signal["tp1Pct"], pips=signal["tp1Pips"], is_forex=is_forex)} (Target 1) \n🚀 {signal_type}'
                if text == "sl2":
                    body = f'✅ Signal closed. \nMinimum profit: {get_pct(pct=signal["tp2Pct"], pips=signal["tp2Pips"], is_forex=is_forex)} (Target 2) \n🚀 {signal_type}'

                title = ""
                if text == "new":
                    title = f"[{noti_heading}] [NEW SIGNAL] ${signal['symbol']}"
                if text == "tp1" or text == "tp2" or text == "tp3":
                    title = f"[{noti_heading}] [TAKE PROFIT] ${signal['symbol']}"
                if text == "sl0":
                    title = f"[{noti_heading}] [STOP LOSS] ${signal['symbol']}"
                if text == "sl1" or text == "sl2" or text == "sl3":
                    title = f"[{noti_heading}] [SIGNAL CLOSED] ${signal['symbol']}"

                messages = [
                    messaging.Message(
                        notification=messaging.Notification(title=title, body=body),
                        token=token,
                    )
                    for token in token_chunk
                ]
                response = messaging.send_all(messages)
                dev_print("Successfully sent message:", response)

        return True
    except Exception as e:
        print("send_signal_notification_to_all_tp_sl_v1:", e)


def get_pct(pct: float = 0.0, pips: float = 0.0, is_forex: bool = False) -> str:
    if is_forex:
        return f"{str(round(pips))} pips"

    return f"{str(round(pct*100, 2))}%"
