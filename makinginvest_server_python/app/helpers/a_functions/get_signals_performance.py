import numpy as np
import pandas as pd

from app.helpers.a_functions.dev_print import dev_print


def get_print_performance_summary(df, is_long=True):

    if df.empty:
        return None

    df_list = []
    for symbol in df["symbol"].unique():
        df_list.append(df[df["symbol"] == symbol])

    df_performance = pd.DataFrame()

    for i in range(0, len(df_list)):
        df = df_list[i].reset_index(drop=True)
        d = get_signal_performance2(df)
        if d is not None:
            df_performance = df_performance.append(d)

    # sort by win rate ensure 100% win rate is on top
    # convert wr to string remove % and convert to float then sort descending then convert back to string and add %
    df_performance["wr"] = df_performance["wr"].astype(str).str.replace("%", "").astype(float)
    df_performance = df_performance.sort_values(by=["wr"], ascending=False)
    df_performance["wr"] = df_performance["wr"].astype(str) + "%"

    long = "long" if is_long else "short"
    df_performance[df_performance["type"] == "total"].to_csv(f"_signals/performance_{long}.csv", index=False)

    dev_print(f"###################################  {long.upper()} PERFORMANCE SUMMARY ###################################")
    dev_print(df_performance[df_performance["type"] == "total"])
    df_performance["tir2$"] = df_performance["tir2$"].astype(float)
    df_performance["tir3$"] = df_performance["tir3$"].astype(float)
    r2 = df_performance[df_performance["type"] == "total"]["tir2$"].sum() / df_performance[df_performance["type"] == "total"]["inv2"].sum()
    r3 = df_performance[df_performance["type"] == "total"]["tir3$"].sum() / df_performance[df_performance["type"] == "total"]["inv3"].sum()
    dev_print(f"r2/trade: {r2*100-100}%")
    dev_print(f"r3/trade: {r3*100-100}%")


def get_signal_performance2(_df: pd.DataFrame):

    try:
        if _df.empty:
            return None

        symbol = _df["symbol"].iloc[0]

        df = _df[_df["entryType"] != "none"]

        if df.empty:
            return None

        duration = df["entryDateTimeUtc"].iloc[0] - df["entryDateTimeUtc"].iloc[-1]
        duration = duration / np.timedelta64(1, "D")

        total_no = len(df)
        total_no_profit1 = len(df[df["takeProfit1Result"] == "profit"])
        total_no_profit2 = len(df[df["takeProfit2Result"] == "profit"])
        total_no_profit3 = len(df[df["takeProfit3Result"] == "profit"])
        total_no_loss1 = len(df[df["takeProfit1Result"] == "loss"])
        total_no_loss2 = len(df[df["takeProfit2Result"] == "loss"])
        total_no_loss3 = len(df[df["takeProfit3Result"] == "loss"])

        win_rate1 = total_no_profit1 / total_no
        win_rate2 = total_no_profit2 / total_no
        win_rate3 = total_no_profit3 / total_no

        total_losers_sum1 = df[df["takeProfit1Result"] == "loss"]["stopLossPct"].sum()
        total_losers_sum2 = df[df["takeProfit2Result"] == "loss"]["stopLossPct"].sum()
        total_losers_sum3 = df[df["takeProfit3Result"] == "loss"]["stopLossPct"].sum()
        total_winners_sum1 = df[df["takeProfit1Result"] == "profit"]["takeProfit1Pct"].sum()
        total_winners_sum2 = df[df["takeProfit2Result"] == "profit"]["takeProfit2Pct"].sum()
        total_winners_sum3 = df[df["takeProfit3Result"] == "profit"]["takeProfit3Pct"].sum()

        total_gain_pct1 = (total_winners_sum1 - total_losers_sum1) * 100
        total_gain_pct2 = (total_winners_sum2 - total_losers_sum2) * 100
        total_gain_pct3 = (total_winners_sum3 - total_losers_sum3) * 100

        total_gain_dollar1 = (1 + (total_winners_sum1 - total_losers_sum1)) * 1000
        total_gain_dollar2 = (1 + (total_winners_sum2 - total_losers_sum2)) * 1000
        total_gain_dollar3 = (1 + (total_winners_sum3 - total_losers_sum3)) * 1000

        total_inv = 1000
        total_inv_return1 = total_gain_dollar1 - total_inv
        total_inv_return2 = total_gain_dollar2 - total_inv
        total_inv_return3 = total_gain_dollar3 - total_inv

        tiered_profit1 = get_total_winning_at_1(df)
        tiered_gain1 = tiered_profit1 - total_losers_sum1
        tiered_inv_return1 = (1 + tiered_gain1) * 1000

        tiered_profit2 = get_total_winning_at_2(df)
        tiered_gain2 = tiered_profit2 - total_losers_sum1
        tiered_inv_return2 = (1 + tiered_gain2) * 1000

        tiered_profit3 = get_total_winning_at_3(df)
        tiered_gain3 = tiered_profit3 - total_losers_sum1
        tiered_inv_return3 = (1 + tiered_gain3) * 1000

        columns_signal_results = [
            "type",
            "symbol",
            "d",
            #
            "no",
            "no_p",
            "no_l",
            "wr",
            # "w1%",
            # "l1%",
            # "g1%",
            #
            # "no2",
            # "no_p2",
            # "no_l2",
            # "wr2",
            # "w2%",
            # "l2%",
            # "g2%",
            #
            # "no3",
            # "no_p3",
            # "no_l3",
            # "wr3",
            # "w3%",
            # "l3%",
            # "g3%",
            #
            # "tp1",
            # "tl1",
            # "tg1",
            #
            "tp2",
            "tl2",
            "tg2",
            "inv2",
            "tir2$",
            #
            "tp3",
            "tl3",
            "tg3",
            "inv3",
            "tir3$",
            #
        ]

        # round to 2 decimals and convert

        df_signal_result = pd.DataFrame(
            [
                [
                    "total",
                    symbol,
                    round_to_string(duration),
                    #
                    total_no,
                    total_no_profit1,
                    total_no_loss1,
                    round_to_string_pct(win_rate1 * 100),
                    # round_to_string(total_winners_sum1),
                    # round_to_string(total_losers_sum1),
                    # round_to_string(total_gain_pct1),
                    #
                    # total_no,
                    # total_no_profit2,
                    # total_no_loss2,
                    # round_to_string(win_rate2),
                    # round_to_string(total_winners_sum2),
                    # round_to_string(total_losers_sum2),
                    # round_to_string(total_gain_pct2),
                    #
                    # total_no,
                    # total_no_profit3,
                    # total_no_loss3,
                    # round_to_string(win_rate3),
                    # round_to_string(total_winners_sum3),
                    # round_to_string(total_losers_sum3),
                    # round_to_string(total_gain_pct3),
                    #
                    # round_to_string(tiered_profit1 * 100),
                    # round_to_string(total_losers_sum1 * -100),
                    # round_to_string(tiered_gain1 * 100),
                    #
                    round_to_string_pct(tiered_profit2 * 100),
                    round_to_string_pct(total_losers_sum1 * -100),
                    round_to_string_pct(tiered_gain2 * 100),
                    total_inv,
                    round_to_string(tiered_inv_return2),
                    #
                    round_to_string_pct(tiered_profit3 * 100),
                    round_to_string_pct(total_losers_sum1 * -100),
                    round_to_string_pct(tiered_gain3 * 100),
                    total_inv,
                    round_to_string(tiered_inv_return3),
                ],
            ],
            columns=columns_signal_results,
        )

        # comvert to float

        return df_signal_result

    except Exception as e:
        print(e)
        return None


def get_total_winning_at_3(df):
    takeProfit1Pct = df["takeProfit1Pct"]
    takeProfit2Pct = df["takeProfit2Pct"]
    takeProfit3Pct = df["takeProfit3Pct"]

    takeProfit1Result = df["takeProfit1Result"]
    takeProfit2Result = df["takeProfit2Result"]
    takeProfit3Result = df["takeProfit3Result"]

    total = 0

    for i in range(len(df)):
        if takeProfit3Result[i] == "profit":
            total += takeProfit3Pct[i] * 0.71
        elif takeProfit2Result[i] == "profit":
            total += takeProfit2Pct[i] * 0.65
        elif takeProfit1Result[i] == "profit":
            total += takeProfit1Pct[i] * 0.5

    return total


def get_total_winning_at_2(df):
    takeProfit1Pct = df["takeProfit1Pct"]
    takeProfit2Pct = df["takeProfit2Pct"]

    takeProfit1Result = df["takeProfit1Result"]
    takeProfit2Result = df["takeProfit2Result"]

    total = 0

    for i in range(len(df)):
        if takeProfit2Result[i] == "profit":
            total += takeProfit2Pct[i] * 0.75
        elif takeProfit1Result[i] == "profit":
            total += takeProfit1Pct[i] * 0.5

    return total


def get_total_winning_at_1(df):
    takeProfit1Pct = df["takeProfit1Pct"]

    takeProfit1Result = df["takeProfit1Result"]
    takeProfit2Result = df["takeProfit2Result"]

    total = 0

    for i in range(len(df)):
        if takeProfit1Result[i] == "profit":
            total += takeProfit1Pct[i] * 0.5

    return total


def round_to_string(x):
    return f"{str(round(x, 2))}"


def round_to_string_pct(x):
    return f"{str(round(x, 2))}%"
