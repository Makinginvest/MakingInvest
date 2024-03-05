import asyncio
import os
from firebase_admin import messaging
from app.a_database_client.db_connect_client import database_mongodb_client

from dotenv import load_dotenv

from app.helpers.a_functions.dev_print import dev_print

load_dotenv()
is_production = os.getenv("PRODUCTION")


async def handle_all_notifications(signals: list = None, current_time_tp_sl=None, noti_heading: str = "Signal Update", name: str = None):
    signals_takeProfit1 = signals[signals["takeProfit1DateTimeUtc"] == current_time_tp_sl]
    signals_takeProfit1 = signals_takeProfit1[signals_takeProfit1["takeProfit1Result"] == "profit"]
    #
    signals_takeProfit2 = signals[signals["takeProfit2DateTimeUtc"] == current_time_tp_sl]
    signals_takeProfit2 = signals_takeProfit2[signals_takeProfit2["takeProfit2Result"] == "profit"]
    #
    signals_takeProfit3 = signals[signals["takeProfit3DateTimeUtc"] == current_time_tp_sl]
    signals_takeProfit3 = signals_takeProfit3[signals_takeProfit3["takeProfit3Result"] == "profit"]
    #
    signals_takeProfit4 = signals[signals["takeProfit4DateTimeUtc"] == current_time_tp_sl]
    signals_takeProfit4 = signals_takeProfit4[signals_takeProfit4["takeProfit4Result"] == "profit"]
    #
    signals_stopLoss = signals[signals["stopLossDateTimeUtc"] == current_time_tp_sl]
    # signals_stopLoss = signals_stopLoss[signals_stopLoss["takeProfit3Hit"] == "loss"]
    signals_sl_after_tp0 = signals_stopLoss[signals_stopLoss["takeProfit1Hit"] == False]
    signals_sl_after_tp1 = signals_stopLoss[signals_stopLoss["takeProfit1Hit"] == True]
    signals_sl_after_tp2 = signals_stopLoss[signals_stopLoss["takeProfit2Hit"] == True]
    signals_sl_after_tp3 = signals_stopLoss[signals_stopLoss["takeProfit3Hit"] == True]

    signals_takeProfit1_dict = signals_takeProfit1.to_dict("records") if signals_takeProfit1.shape[0] > 0 else []
    signals_takeProfit2_dict = signals_takeProfit2.to_dict("records") if signals_takeProfit2.shape[0] > 0 else []
    signals_takeProfit3_dict = signals_takeProfit3.to_dict("records") if signals_takeProfit3.shape[0] > 0 else []
    signals_takeProfit4_dict = signals_takeProfit4.to_dict("records") if signals_takeProfit4.shape[0] > 0 else []
    signals_sl_after_tp0_dict = signals_sl_after_tp0.to_dict("records") if signals_sl_after_tp0.shape[0] > 0 else []
    signals_sl_after_tp1_dict = signals_sl_after_tp1.to_dict("records") if signals_sl_after_tp1.shape[0] > 0 else []
    signals_sl_after_tp2_dict = signals_sl_after_tp2.to_dict("records") if signals_sl_after_tp2.shape[0] > 0 else []
    signals_sl_after_tp3_dict = signals_sl_after_tp3.to_dict("records") if signals_sl_after_tp3.shape[0] > 0 else []

    # fix for double notifications check if signals_sl_after_tp2_dict has a signal and entryDateTimeUtc is the same as signals_sl_after_tp1_dict delete from signals_sl_after_tp1_dict
    if signals_sl_after_tp2_dict != [] and signals_sl_after_tp1_dict != []:
        for s_tp2 in signals_sl_after_tp2_dict:
            for s_tp1 in signals_sl_after_tp1_dict:
                if s_tp2["entryDateTimeUtc"] == s_tp1["entryDateTimeUtc"] and s_tp2["symbol"] == s_tp1["symbol"]:
                    signals_sl_after_tp1_dict.remove(s_tp1)

    # fix for double notifications check if signals_sl_after_tp3_dict has a signal and entryDateTimeUtc is the same as signals_sl_after_tp2_dict delete from signals_sl_after_tp2_dict
    if signals_sl_after_tp3_dict != [] and signals_sl_after_tp2_dict != []:
        for s_tp3 in signals_sl_after_tp3_dict:
            for s_tp2 in signals_sl_after_tp2_dict:
                if s_tp3["entryDateTimeUtc"] == s_tp2["entryDateTimeUtc"] and s_tp3["symbol"] == s_tp2["symbol"]:
                    signals_sl_after_tp2_dict.remove(s_tp2)

    signals_new = signals[signals["entryDateTimeUtc"] == current_time_tp_sl]
    signals_new_dict = signals_new.to_dict("records") if signals_new.shape[0] > 0 else []

    await asyncio.create_task(send_signal_notification_to_all_tp_sl(signals=signals_new_dict, text="new", noti_heading=noti_heading, name=name))
    await asyncio.create_task(send_signal_notification_to_all_tp_sl(signals=signals_takeProfit1_dict, text="tp1", noti_heading=noti_heading, name=name))
    await asyncio.create_task(send_signal_notification_to_all_tp_sl(signals=signals_takeProfit2_dict, text="tp2", noti_heading=noti_heading, name=name))
    await asyncio.create_task(send_signal_notification_to_all_tp_sl(signals=signals_takeProfit3_dict, text="tp3", noti_heading=noti_heading, name=name))
    await asyncio.create_task(send_signal_notification_to_all_tp_sl(signals=signals_takeProfit4_dict, text="tp4", noti_heading=noti_heading, name=name))
    await asyncio.create_task(send_signal_notification_to_all_tp_sl(signals=signals_sl_after_tp0_dict, text="sl0", noti_heading=noti_heading, name=name))
    await asyncio.create_task(send_signal_notification_to_all_tp_sl(signals=signals_sl_after_tp1_dict, text="sl1", noti_heading=noti_heading, name=name))
    await asyncio.create_task(send_signal_notification_to_all_tp_sl(signals=signals_sl_after_tp2_dict, text="sl2", noti_heading=noti_heading, name=name))
    await asyncio.create_task(send_signal_notification_to_all_tp_sl(signals=signals_sl_after_tp3_dict, text="sl3", noti_heading=noti_heading, name=name))

    dev_print(f"signals_new_dict: {len(signals_new_dict)}")
    dev_print(f"signals_takeProfit1_dict: {len(signals_takeProfit1_dict)}")
    dev_print(f"signals_takeProfit2_dict: {len(signals_takeProfit2_dict)}")
    dev_print(f"signals_takeProfit3_dict: {len(signals_takeProfit3_dict)}")
    dev_print(f"signals_takeProfit4_dict: {len(signals_takeProfit4_dict)}")
    #
    dev_print(f"signals_sl_after_tp1_dict: {len(signals_sl_after_tp1_dict)}")
    dev_print(f"signals_sl_after_tp2_dict: {len(signals_sl_after_tp2_dict)}")
    dev_print(f"signals_sl_after_tp3_dict: {len(signals_sl_after_tp3_dict)}")
    dev_print(f"signals_sl_after_tp0_dict: {len(signals_sl_after_tp0_dict)}")


async def send_signal_notification_to_all_tp_sl(signals: list = None, text: str = "tp1", noti_heading: str = "Signal Update", name: str = None):
    if is_production != "True":
        return False

    if signals == []:
        return

    try:
        user_collection = database_mongodb_client[f"users"]
        users: list = await user_collection.find({"appBuildNumber": {"$gte": 29, "$lt": 1001}, "notificationsDisabled": {"$nin": [name]}}).to_list(length=100000)
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
                    body = f'✅ Target 1 done with {get_pct(pct=signal["takeProfit1Pct"], pips=signal["takeProfit1Pips"], is_forex=is_forex)} \n🚀 {signal_type}'
                if text == "tp2":
                    body = f'✅ Target 2 done with {get_pct(pct=signal["takeProfit2Pct"], pips=signal["takeProfit2Pips"], is_forex=is_forex)} \n🚀 {signal_type}'
                if text == "tp3":
                    body = f'✅ Target 3 done with {get_pct(pct=signal["takeProfit3Pct"], pips=signal["takeProfit3Pips"], is_forex=is_forex)} \n🚀 {signal_type}'
                if text == "tp4":
                    body = f'✅ Target 4 done with {get_pct(pct=signal["takeProfit4Pct"], pips=signal["takeProfit4Pips"], is_forex=is_forex)} \n🚀 {signal_type}'
                if text == "sl0":
                    body = f'⛔ Stop loss \nLoss: {get_pct(pct=signal["stopLossPct"], pips=signal["stopLossPips"], is_forex=is_forex)} \n🚀 {signal_type}'
                if text == "sl1":
                    body = f'✅ Signal closed. \nMinimum profit: {get_pct(pct=signal["takeProfit1Pct"], pips=signal["takeProfit1Pips"], is_forex=is_forex)} (Target 1) \n🚀 {signal_type}'
                if text == "sl2":
                    body = f'✅ Signal closed. \nMinimum profit: {get_pct(pct=signal["takeProfit2Pct"], pips=signal["takeProfit2Pips"], is_forex=is_forex)} (Target 2) \n🚀 {signal_type}'
                if text == "sl3":
                    body = f'✅ Signal closed. \nMinimum profit: {get_pct(pct=signal["takeProfit3Pct"], pips=signal["takeProfit3Pips"], is_forex=is_forex)} (Target 3) \n🚀 {signal_type}'

                title = ""
                if text == "new":
                    title = f"[{noti_heading}] [NEW SIGNAL] ${signal['symbol']}"
                if text == "tp1" or text == "tp2" or text == "tp3" or text == "tp4":
                    title = f"[{noti_heading}] [TAKE PROFIT] ${signal['symbol']}"
                if text == "sl0":
                    title = f"[{noti_heading}] [STOP LOSS] ${signal['symbol']}"
                if text == "sl1" or text == "sl2" or text == "sl3":
                    title = f"[{noti_heading}] [SIGNAL CLOSED] ${signal['symbol']}"

                messages = [
                    messaging.Message(
                        notification=messaging.Notification(
                            title=title,
                            body=body,
                        ),
                        token=token,
                    )
                    for token in token_chunk
                ]
                response = messaging.send_all(messages)
                dev_print("Successfully sent message:", response)

        return True
    except Exception as e:
        print("Error:", e)


def get_pct(pct: float = 0.0, pips: float = 0.0, is_forex: bool = False) -> str:
    if is_forex:
        return f"{str(round(pips))} pips"

    return f"{str(round(pct*100, 2))}%"
