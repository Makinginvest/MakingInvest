import numpy as np
import pandas as pd


def check_increasing_success(df_series: pd.Series, window: int = 11, success_threshold: int = 7) -> pd.Series:
    rolling_window = df_series.rolling(window=window, min_periods=1)
    return rolling_window.apply(lambda x: (sum(x[:-1] < x[1:]) >= success_threshold) and (x[-1] > x[0]), raw=True)


def check_decreasing_success(df_series: pd.Series, window: int = 11, success_threshold: int = 7) -> pd.Series:
    rolling_window = df_series.rolling(window=window, min_periods=1)
    return rolling_window.apply(lambda x: (sum(x[:-1] > x[1:]) >= success_threshold) and (x[-1] < x[0]), raw=True)


def check_increasing_diff_success(df_series1: pd.Series, df_series2: pd.Series, window: int = 11, success_threshold: int = 7) -> pd.Series:
    diff_abs = np.abs(df_series1 - df_series2) / df_series2
    rolling_window = diff_abs.rolling(window=window, min_periods=1)
    return rolling_window.apply(lambda x: (sum(x[:-1] < x[1:]) >= success_threshold) and (x[-1] > x[0]), raw=True)


def check_decreasing_diff_success(df_series1: pd.Series, df_series2: pd.Series, window: int = 11, success_threshold: int = 7) -> pd.Series:
    diff_abs = np.abs(df_series1 - df_series2) / df_series2
    rolling_window = diff_abs.rolling(window=window, min_periods=1)
    return rolling_window.apply(lambda x: (sum(x[:-1] > x[1:]) >= success_threshold) and (x[-1] < x[0]), raw=True)
