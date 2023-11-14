from datetime import datetime
import pandas as pd

from app.helpers.a_functions.get_ensure_one_open_position import get_open_new_position_level
from app.helpers.a_functions_mongodb.a_mongodb_data import get_mongodb_data_historical
from app.models.signal_model import SignalModel


async def get_signal_result(df: pd.DataFrame, histCollection=None, open_new_positions_level_int=3, stop_lost_update_level=3, **kwargs):
    try:
        df = df[df["entryType"] != "none"]
        df = df.sort_values(by=["entryDateTimeUtc"], ascending=True)

        symbol = df["symbol"].unique()[0]
        lowest_lastCheckDateTimeUtc = df["lastCheckDateTimeUtc"].min()
        lowest_lastCheckDateTimeUtc = lowest_lastCheckDateTimeUtc - pd.Timedelta(days=2)

        df_lower_t = await get_mongodb_data_historical(symbol, histCollection=histCollection, timeframe="15m", datetime_start=lowest_lastCheckDateTimeUtc)

        df_lower_t["dateTimeUtc"] = df_lower_t["dateTimeUtc"] + pd.Timedelta("15 minutes")
        df_lower_t["dateTimeEst"] = df_lower_t["dateTimeEst"] + pd.Timedelta("15 minutes")

        df_lower_t["time"] = df_lower_t["dateTimeUtc"]
        df_lower_t.index = df_lower_t["time"]

        # remove where datTimeUtc is in the future?
        current_time = datetime.utcnow()
        df_lower_t = df_lower_t[df_lower_t["dateTimeUtc"] <= current_time]

        df_json = df.to_dict("records")
        df_json = [SignalModel(**x) for x in df_json]

        for i in range(len(df_json)):
            df_json[i] = get_signal_result_per_signal_period4(
                df_json[i], df_lower_t, stop_lost_update_level=stop_lost_update_level, open_new_positions_level_int=open_new_positions_level_int
            )
            df_json[i] = df_json[i].dict()

        df = pd.DataFrame(df_json, columns=df.columns)
        df["time"] = df["entryDateTimeUtc"]
        df.index = df["time"]

        df["entryType"] = get_open_new_position_level(df, open_new_positions_level_int=open_new_positions_level_int)
        df["entryType"] = df["entryType"].fillna("none")
        df = df[df["entryType"] != "none"]

        return df

    except Exception as e:
        print("Error in get_signal_result_periods: ", e)
        return df


def get_signal_result_per_signal_period4(signal: SignalModel, _df_lower: pd.DataFrame, stop_lost_update_level=3, open_new_positions_level_int=3):
    last_entryDateTimeUtc = _df_lower.index[-1]

    isClosed = False
    isClosedAuto = False
    closedDateTimeUtc = None

    stopLoss = signal.stopLoss
    stopLossHit = signal.stopLossHit
    stopLossDateTimeUtc = signal.stopLossDateTimeUtc

    stopLossRevised = signal.stopLossRevised
    stopLossRevisedHit = signal.stopLossRevisedHit
    stopLossRevisedDateTimeUtc = signal.stopLossRevisedDateTimeUtc

    takeProfit1 = signal.takeProfit1
    takeProfit1Hit = signal.takeProfit1Hit
    takeProfit1DateTimeUtc = signal.takeProfit1DateTimeUtc
    takeProfit1Result = signal.takeProfit1Result

    takeProfit2 = signal.takeProfit2
    takeProfit2Hit = signal.takeProfit2Hit
    takeProfit2DateTimeUtc = signal.takeProfit2DateTimeUtc
    takeProfit2Result = signal.takeProfit2Result

    takeProfit3 = signal.takeProfit3
    takeProfit3Hit = signal.takeProfit3Hit
    takeProfit3DateTimeUtc = signal.takeProfit3DateTimeUtc
    takeProfit3Result = signal.takeProfit3Result

    takeProfit4 = signal.takeProfit4
    takeProfit4Hit = signal.takeProfit4Hit
    takeProfit4DateTimeUtc = signal.takeProfit4DateTimeUtc
    takeProfit4Result = signal.takeProfit4Result

    high: pd.Series = _df_lower["high"]
    low: pd.Series = _df_lower["low"]
    high_l: pd.Series = high.iloc[high.index > signal.entryDateTimeUtc].copy()
    low_l: pd.Series = low.iloc[low.index > signal.entryDateTimeUtc].copy()

    if signal.entryType == "long":
        for i in range(len(high_l)):
            # ------------------------------  highestPct ----------------------------- #
            currentPct = (high_l.iloc[i] - signal.entryPrice) / signal.entryPrice
            if signal.highestPct is None:
                signal.highestPct = 0
            if currentPct > signal.highestPct:
                currentPips = (high_l.iloc[i] - signal.entryPrice) * 10000
                signal.highestPct = currentPct
                signal.highestPips = currentPips
                signal.highestPctPipsDateTimeUtc = high_l.index[i]

            if high_l.iloc[i] >= takeProfit1 and not takeProfit1Hit:
                takeProfit1Hit = True
                takeProfit1DateTimeUtc = high_l.index[i]
                takeProfit1Result = "profit"
                signal.entryProfitLevel = 1
                # move stop loss to breakeven
                if stop_lost_update_level == 1:
                    stopLossRevised = signal.entryPrice
                    signal.stopLossRevised = signal.entryPrice
                    signal.stopLossRevisedPct = 0
                    signal.stopLossRevisedPips = 0
                    signal.stopLossRevisedTp1 = True
                # update new entry allow new signal
                if open_new_positions_level_int == 1:
                    signal.entryAllowNewSignalDateTimeUtc = high_l.index[i]

            if high_l.iloc[i] >= takeProfit2 and not takeProfit2Hit:
                takeProfit2Hit = True
                takeProfit2DateTimeUtc = high_l.index[i]
                takeProfit2Result = "profit"
                signal.entryProfitLevel = 2
                # move stop loss to take profit 1
                if stop_lost_update_level == 2:
                    stopLossRevised = signal.entryPrice
                    signal.stopLossRevised = signal.entryPrice
                    signal.stopLossRevisedPct = 0
                    signal.stopLossRevisedPips = 0
                    signal.stopLossRevisedTp2 = True
                # update new entry allow new signal
                if open_new_positions_level_int == 2:
                    signal.entryAllowNewSignalDateTimeUtc = high_l.index[i]

            if high_l.iloc[i] >= takeProfit3 and not takeProfit3Hit:
                takeProfit3Hit = True
                takeProfit3DateTimeUtc = high_l.index[i]
                takeProfit3Result = "profit"
                signal.entryProfitLevel = 3
                # move stop loss to take profit 2
                if stop_lost_update_level == 3:
                    stopLossRevised = signal.entryPrice
                    signal.stopLossRevised = signal.entryPrice
                    signal.stopLossRevisedPct = 0
                    signal.stopLossRevisedPips = 0
                    signal.stopLossRevisedTp3 = True

                # update new entry allow new signal
                if open_new_positions_level_int == 3:
                    signal.entryAllowNewSignalDateTimeUtc = high_l.index[i]

            if high_l.iloc[i] >= takeProfit4 and not takeProfit4Hit:
                takeProfit4Hit = True
                takeProfit4DateTimeUtc = high_l.index[i]
                takeProfit4Result = "profit"
                signal.entryProfitLevel = 4
                isClosed = True
                isClosedAuto = True
                closedDateTimeUtc = high_l.index[i]

                # allow new signal
                signal.entryAllowNewSignalDateTimeUtc = high_l.index[i]
                break

            if low_l.iloc[i] <= stopLoss and not signal.stopLossRevisedTp1 and not signal.stopLossRevisedTp2 and not signal.stopLossRevisedTp3:
                stopLossHit = True
                stopLossDateTimeUtc = low_l.index[i]
                isClosed = True
                isClosedAuto = True
                closedDateTimeUtc = low_l.index[i]
                # some fixes
                takeProfit1Result = "loss" if takeProfit1Result == "" else takeProfit1Result
                takeProfit2Result = "loss" if takeProfit2Result == "" else takeProfit2Result
                takeProfit3Result = "loss" if takeProfit3Result == "" else takeProfit3Result
                takeProfit4Result = "loss" if takeProfit4Result == "" else takeProfit4Result

                # allow new signal
                signal.entryAllowNewSignalDateTimeUtc = high_l.index[i]
                break

            if stopLossRevised and low_l.iloc[i] <= stopLossRevised and signal.stopLossRevisedTp1 and low_l.index[i] > takeProfit1DateTimeUtc:
                stopLossRevisedHit = True
                stopLossRevisedDateTimeUtc = low_l.index[i]
                isClosed = True
                isClosedAuto = True
                closedDateTimeUtc = low_l.index[i]
                # some fixes
                takeProfit1Result = "loss" if takeProfit1Result == "" else takeProfit1Result
                takeProfit2Result = "loss" if takeProfit2Result == "" else takeProfit2Result
                takeProfit3Result = "loss" if takeProfit3Result == "" else takeProfit3Result
                takeProfit4Result = "loss" if takeProfit4Result == "" else takeProfit4Result

                # allow new signal
                signal.entryAllowNewSignalDateTimeUtc = high_l.index[i]
                break

            if stopLossRevised and low_l.iloc[i] <= stopLossRevised and signal.stopLossRevisedTp2 and low_l.index[i] > takeProfit2DateTimeUtc:
                stopLossRevisedHit = True
                stopLossRevisedDateTimeUtc = low_l.index[i]
                isClosed = True
                isClosedAuto = True
                closedDateTimeUtc = low_l.index[i]

                # some fixes
                takeProfit1Result = "loss" if takeProfit1Result == "" else takeProfit1Result
                takeProfit2Result = "loss" if takeProfit2Result == "" else takeProfit2Result
                takeProfit3Result = "loss" if takeProfit3Result == "" else takeProfit3Result
                takeProfit4Result = "loss" if takeProfit4Result == "" else takeProfit4Result

                # allow new signal
                signal.entryAllowNewSignalDateTimeUtc = high_l.index[i]
                break

            if stopLossRevised and low_l.iloc[i] <= stopLossRevised and signal.stopLossRevisedTp3 and low_l.index[i] > takeProfit3DateTimeUtc:
                stopLossRevisedHit = True
                stopLossRevisedDateTimeUtc = low_l.index[i]
                isClosed = True
                isClosedAuto = True
                closedDateTimeUtc = low_l.index[i]

                # some fixes
                takeProfit1Result = "loss" if takeProfit1Result == "" else takeProfit1Result
                takeProfit2Result = "loss" if takeProfit2Result == "" else takeProfit2Result
                takeProfit3Result = "loss" if takeProfit3Result == "" else takeProfit3Result
                takeProfit4Result = "loss" if takeProfit4Result == "" else takeProfit4Result

                # allow new signal
                signal.entryAllowNewSignalDateTimeUtc = high_l.index[i]
                break

    if signal.entryType == "short":
        for i in range(len(high_l)):
            # ------------------------------  highestPct ----------------------------- #
            currentPct = (signal.entryPrice - low_l.iloc[i]) / signal.entryPrice
            if signal.highestPct is None:
                signal.highestPct = 0
            if currentPct > signal.highestPct:
                currentPips = (signal.entryPrice - low_l.iloc[i]) * 10000
                signal.highestPct = currentPct
                signal.highestPips = currentPips
                signal.highestPctPipsDateTimeUtc = low_l.index[i]

            if low_l.iloc[i] <= takeProfit1 and not takeProfit1Hit:
                takeProfit1Hit = True
                takeProfit1DateTimeUtc = low_l.index[i]
                takeProfit1Result = "profit"
                signal.entryProfitLevel = 1
                # move stop loss to breakeven
                if stop_lost_update_level == 1:
                    stopLossRevised = signal.entryPrice
                    signal.stopLossRevised = signal.entryPrice
                    signal.stopLossRevisedPct = 0
                    signal.stopLossRevisedPips = 0
                    signal.stopLossRevisedTp1 = True
                # update new entry allow new signal
                if open_new_positions_level_int == 1:
                    signal.entryAllowNewSignalDateTimeUtc = low_l.index[i]

            if low_l.iloc[i] <= takeProfit2 and not takeProfit2Hit:
                takeProfit2Hit = True
                takeProfit2DateTimeUtc = low_l.index[i]
                takeProfit2Result = "profit"
                signal.entryProfitLevel = 2
                # move stop loss to take profit 1
                if stop_lost_update_level == 2:
                    stopLossRevised = signal.entryPrice
                    signal.stopLossRevised = signal.entryPrice
                    signal.stopLossRevisedPct = 0
                    signal.stopLossRevisedPips = 0
                    signal.stopLossRevisedTp2 = True

                # update new entry allow new signal
                if open_new_positions_level_int == 2:
                    signal.entryAllowNewSignalDateTimeUtc = low_l.index[i]

            if low_l.iloc[i] <= takeProfit3 and not takeProfit3Hit:
                takeProfit3Hit = True
                takeProfit3DateTimeUtc = low_l.index[i]
                takeProfit3Result = "profit"
                signal.entryProfitLevel = 3
                # move stop loss to take profit 2
                if stop_lost_update_level == 3:
                    stopLossRevised = signal.entryPrice
                    signal.stopLossRevised = signal.entryPrice
                    signal.stopLossRevisedPct = 0
                    signal.stopLossRevisedPips = 0
                    signal.stopLossRevisedTp3 = True

                # update new entry allow new signal
                if open_new_positions_level_int == 3:
                    signal.entryAllowNewSignalDateTimeUtc = low_l.index[i]

            if low_l.iloc[i] <= takeProfit4 and not takeProfit4Hit:
                takeProfit4Hit = True
                takeProfit4DateTimeUtc = low_l.index[i]
                takeProfit4Result = "profit"
                signal.entryProfitLevel = 4
                isClosed = True
                isClosedAuto = True
                closedDateTimeUtc = low_l.index[i]

                # allow new signal
                signal.entryAllowNewSignalDateTimeUtc = low_l.index[i]
                break

            if high_l.iloc[i] >= stopLoss and not signal.stopLossRevisedTp1 and not signal.stopLossRevisedTp2 and not signal.stopLossRevisedTp3:
                stopLossHit = True
                stopLossDateTimeUtc = high_l.index[i]
                isClosed = True
                isClosedAuto = True
                closedDateTimeUtc = high_l.index[i]
                # some fixes
                takeProfit1Result = "loss" if takeProfit1Result == "" else takeProfit1Result
                takeProfit2Result = "loss" if takeProfit2Result == "" else takeProfit2Result
                takeProfit3Result = "loss" if takeProfit3Result == "" else takeProfit3Result
                takeProfit4Result = "loss" if takeProfit4Result == "" else takeProfit4Result

                # allow new signal
                signal.entryAllowNewSignalDateTimeUtc = low_l.index[i]
                break

            if stopLossRevised and high_l.iloc[i] >= stopLossRevised and signal.stopLossRevisedTp1 and high_l.index[i] > takeProfit1DateTimeUtc:
                stopLossRevisedHit = True
                stopLossRevisedDateTimeUtc = high_l.index[i]
                isClosed = True
                isClosedAuto = True
                closedDateTimeUtc = high_l.index[i]
                # some fixes
                takeProfit1Result = "loss" if takeProfit1Result == "" else takeProfit1Result
                takeProfit2Result = "loss" if takeProfit2Result == "" else takeProfit2Result
                takeProfit3Result = "loss" if takeProfit3Result == "" else takeProfit3Result
                takeProfit4Result = "loss" if takeProfit4Result == "" else takeProfit4Result

                # allow new signal
                signal.entryAllowNewSignalDateTimeUtc = low_l.index[i]
                break

            if stopLossRevised and high_l.iloc[i] >= stopLossRevised and signal.stopLossRevisedTp2 and high_l.index[i] > takeProfit2DateTimeUtc:
                stopLossRevisedHit = True
                stopLossRevisedDateTimeUtc = high_l.index[i]
                isClosed = True
                isClosedAuto = True
                closedDateTimeUtc = high_l.index[i]
                # some fixes
                takeProfit1Result = "loss" if takeProfit1Result == "" else takeProfit1Result
                takeProfit2Result = "loss" if takeProfit2Result == "" else takeProfit2Result
                takeProfit3Result = "loss" if takeProfit3Result == "" else takeProfit3Result
                takeProfit4Result = "loss" if takeProfit4Result == "" else takeProfit4Result

                # allow new signal
                signal.entryAllowNewSignalDateTimeUtc = low_l.index[i]
                break

            if stopLossRevised and high_l.iloc[i] >= stopLossRevised and signal.stopLossRevisedTp3 and high_l.index[i] > takeProfit3DateTimeUtc:
                stopLossRevisedHit = True
                stopLossRevisedDateTimeUtc = high_l.index[i]
                isClosed = True
                isClosedAuto = True
                closedDateTimeUtc = high_l.index[i]
                # some fixes
                takeProfit1Result = "loss" if takeProfit1Result == "" else takeProfit1Result
                takeProfit2Result = "loss" if takeProfit2Result == "" else takeProfit2Result
                takeProfit3Result = "loss" if takeProfit3Result == "" else takeProfit3Result
                takeProfit4Result = "loss" if takeProfit4Result == "" else takeProfit4Result

                # allow new signal
                signal.entryAllowNewSignalDateTimeUtc = low_l.index[i]
                break

    signal.stopLossHit = stopLossHit
    signal.stopLossDateTimeUtc = stopLossDateTimeUtc

    signal.stopLossRevisedHit = stopLossRevisedHit
    signal.stopLossRevisedDateTimeUtc = stopLossRevisedDateTimeUtc

    signal.takeProfit1Hit = takeProfit1Hit
    signal.takeProfit1DateTimeUtc = takeProfit1DateTimeUtc
    signal.takeProfit1Result = takeProfit1Result

    signal.takeProfit2Hit = takeProfit2Hit
    signal.takeProfit2DateTimeUtc = takeProfit2DateTimeUtc
    signal.takeProfit2Result = takeProfit2Result

    signal.takeProfit3Hit = takeProfit3Hit
    signal.takeProfit3DateTimeUtc = takeProfit3DateTimeUtc
    signal.takeProfit3Result = takeProfit3Result

    signal.takeProfit4Hit = takeProfit4Hit
    signal.takeProfit4DateTimeUtc = takeProfit4DateTimeUtc
    signal.takeProfit4Result = takeProfit4Result

    signal.isClosed = isClosed
    signal.isClosedAuto = isClosedAuto
    signal.closedDateTimeUtc = closedDateTimeUtc
    signal.lastCheckDateTimeUtc = last_entryDateTimeUtc

    # entryResult
    if signal.stopLossHit and signal.takeProfit1Hit:
        signal.entryResult = "profit"
    if signal.stopLossHit and not signal.takeProfit1Hit:
        signal.entryResult = "loss"
    if (not signal.stopLossHit) and signal.takeProfit1Hit:
        signal.entryResult = "profit"

    if signal.takeProfit1Hit:
        signal.entryProfitPct = signal.takeProfit1Pct
        signal.entryProfitPips = signal.takeProfit1Pips
    if signal.takeProfit2Hit:
        signal.entryProfitPct = signal.takeProfit2Pct
        signal.entryProfitPips = signal.takeProfit2Pips
    if signal.takeProfit3Hit:
        signal.entryProfitPct = signal.takeProfit3Pct
        signal.entryProfitPips = signal.takeProfit3Pips
    if signal.takeProfit4Hit:
        signal.entryProfitPct = signal.takeProfit4Pct
        signal.entryProfitPips = signal.takeProfit4Pips
    if signal.stopLossHit and not signal.takeProfit1Hit:
        signal.entryProfitPct = -signal.stopLossPct
        signal.entryProfitPips = -signal.stopLossPips

    # est dates
    signal.closedDateTimeEst = signal.closedDateTimeUtc - pd.Timedelta(hours=5)
    signal.stopLossDateTimeEst = signal.stopLossDateTimeUtc - pd.Timedelta(hours=5)
    signal.stopLossRevisedDateTimeEst = signal.stopLossRevisedDateTimeUtc - pd.Timedelta(hours=5)
    signal.takeProfit1DateTimeEst = signal.takeProfit1DateTimeUtc - pd.Timedelta(hours=5)
    signal.takeProfit2DateTimeEst = signal.takeProfit2DateTimeUtc - pd.Timedelta(hours=5)
    signal.takeProfit3DateTimeEst = signal.takeProfit3DateTimeUtc - pd.Timedelta(hours=5)
    signal.takeProfit4DateTimeEst = signal.takeProfit4DateTimeUtc - pd.Timedelta(hours=5)
    signal.lastCheckDateTimeEst = signal.lastCheckDateTimeUtc - pd.Timedelta(hours=5)
    signal.highestPctPipsDateTimeEst = signal.highestPctPipsDateTimeUtc - pd.Timedelta(hours=5)
    signal.entryAllowNewSignalDateTimeEst = signal.entryAllowNewSignalDateTimeUtc - pd.Timedelta(hours=5)

    return signal
