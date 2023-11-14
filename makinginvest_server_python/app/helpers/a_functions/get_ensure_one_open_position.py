from os import write
import pandas as pd


# def get_open_new_position_level(_df, open_new_positions_level_int=1):
#     df = _df.copy()

#     df = df.sort_values(by=["entryDateTimeUtc"], ascending=True)
#     df = df[df["entryType"] != "none"]

#     entryType = df["entryType"]
#     new_entryType = df["entryType"].copy()

#     if len(entryType) == 0:
#         return new_entryType

#     entryDateTimeUtc = df["entryDateTimeUtc"]
#     stopLossDateTimeUtc = df["stopLossDateTimeUtc"]
#     takeProfit1DateTimeUtc = df["takeProfit1DateTimeUtc"]
#     takeProfit2DateTimeUtc = df["takeProfit2DateTimeUtc"]
#     takeProfit3DateTimeUtc = df["takeProfit3DateTimeUtc"]

#     takeProfitDateTimeUtc = takeProfit1DateTimeUtc
#     if open_new_positions_level_int == 2:
#         takeProfitDateTimeUtc = takeProfit2DateTimeUtc
#     elif open_new_positions_level_int == 3:
#         takeProfitDateTimeUtc = takeProfit3DateTimeUtc

#     for i in range(len(entryType)):
#         j = i - 1
#         while j >= 0:
#             condition1 = entryType[i] == entryType[j]
#             condition2 = pd.isna(takeProfitDateTimeUtc[j]) or entryDateTimeUtc[i] <= takeProfitDateTimeUtc[j]
#             condition3 = pd.isna(stopLossDateTimeUtc[j]) or entryDateTimeUtc[i] <= stopLossDateTimeUtc[j]

#             if condition1 and condition2 and condition3:
#                 new_entryType[i] = "none"
#             j -= 1

#     return new_entryType


def get_open_new_position_level(_df, open_new_positions_level_int=1):

    df_copy = _df.copy()

    entryType = df_copy["entryType"]
    new_entryType = df_copy["entryType"].copy()
    entryDateTimeUtc = df_copy["entryDateTimeUtc"]

    for i in range(len(entryDateTimeUtc)):

        current_index = df_copy.index[i]

        if entryType[current_index] == "none":
            continue

        df_i = df_copy.copy()
        df_i = df_i[df_i["entryType"] == entryType[current_index]]
        df_i = df_i[df_i["entryDateTimeUtc"] < entryDateTimeUtc[current_index]]

        entryAllowNewSignalDateTimeUtc = df_i["entryAllowNewSignalDateTimeUtc"]
        entryAllowNewSignalDateTimeUtc_list = entryAllowNewSignalDateTimeUtc.tolist()

        if not entryAllowNewSignalDateTimeUtc_list:
            new_entryType[current_index] = entryType[current_index]
            df_copy.loc[current_index, "entryType"] = entryType[current_index]
            continue

        if any(pd.isna(entryAllowNewSignalDateTimeUtc_list)):
            new_entryType[current_index] = "none"
            df_copy.loc[current_index, "entryType"] = "none"
            continue

        # entryDateTimeUtc[current_index] >= all entryAllowNewSignalDateTimeUtc
        if entryDateTimeUtc[current_index] < max(entryAllowNewSignalDateTimeUtc_list):
            new_entryType[current_index] = "none"
            df_copy.loc[current_index, "entryType"] = "none"
            continue

    return new_entryType
