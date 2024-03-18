import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from numba import jit, prange, njit


# -----------------------------  VECTOR SLOPE ---------------------------- #
@njit
def calculate_slope_lookback_numba(y: np.ndarray, lookback: int) -> np.ndarray:
    n = y.shape[0]
    result = np.empty(n)

    x = np.arange(lookback)

    for i in range(n):
        if i < lookback - 1:
            result[i] = np.nan
        else:
            y_window = y[i - lookback + 1 : i + 1]
            A = np.zeros((lookback, 2))
            A[:, 0] = x
            A[:, 1] = 1
            coef = np.dot(np.linalg.pinv(A), y_window)
            result[i] = coef[0]

    return result


def calculate_slope_lookback_vectorized(series: pd.Series, lookback: int, use_prev=False) -> pd.Series:
    if lookback <= 1:
        raise ValueError("lookback must be greater than 1")

    gradient_array = calculate_slope_lookback_numba(series.values, lookback)
    gradient_series = pd.Series(gradient_array, index=series.index)

    gradient_series_diff = gradient_series.diff(periods=lookback if not use_prev else 1)
    gradient_series = gradient_series_diff.apply(lambda x: 1 if x > 0 else -1 if x < 0 else 0)

    return gradient_series


# ---------------------------  INCREASING TREND -------------------------- #
@njit(parallel=True)
def check_increasing_trend_numba(series: np.ndarray, lookback: int, threshold: float, check_last: bool, check_first: bool) -> np.ndarray:
    n = series.shape[0]
    result = np.empty(n)

    for i in prange(n):
        if i < lookback - 1:
            result[i] = 0
        else:
            window = series[i - lookback + 1 : i + 1]
            diff = np.diff(window)
            pos_prop = np.sum(diff > 0) / (lookback - 1)

            if check_last and window[-1] <= window[-2]:
                result[i] = 0
            elif threshold == 0 or (pos_prop >= threshold and (not check_first or window[-1] > window[0])):
                result[i] = 1
            else:
                result[i] = 0

    return result


def check_increasing_trend(series: pd.Series, lookback: int, threshold: float = 0.6, check_last: bool = False, check_first: bool = True) -> pd.Series:
    if lookback <= 1:
        raise ValueError("lookback must be greater than 1")

    trend_array = check_increasing_trend_numba(series.values, lookback, threshold, check_last, check_first)
    trend_series = pd.Series(trend_array, index=series.index)

    return trend_series


# ---------------------------  DECREASING TREND -------------------------- #
@njit(parallel=True)
def check_decreasing_trend_numba(series: np.ndarray, lookback: int, threshold: float, check_last: bool, check_first: bool) -> np.ndarray:
    n = series.shape[0]
    result = np.empty(n)

    for i in prange(n):
        if i < lookback - 1:
            result[i] = 0
        else:
            window = series[i - lookback + 1 : i + 1]
            diff = np.diff(window)
            neg_prop = np.sum(diff < 0) / (lookback - 1)

            if check_last and window[-1] >= window[-2]:
                result[i] = 0
            elif threshold == 0 or (neg_prop >= threshold and (not check_first or window[-1] < window[0])):
                result[i] = -1
            else:
                result[i] = 0

    return result


def check_decreasing_trend(series: pd.Series, lookback: int, threshold: float = 0.6, check_last: bool = False, check_first: bool = True) -> pd.Series:
    if lookback <= 1:
        raise ValueError("lookback must be greater than 1")

    trend_array = check_decreasing_trend_numba(series.values, lookback, threshold, check_last, check_first)
    trend_series = pd.Series(trend_array, index=series.index)

    return trend_series


# ---------------------------  CROSS OVER CHECK -------------------------- #
def check_crossovers_lookback(series1: pd.Series, series2: pd.Series, lookback: int, max_cross: int, allow_cross=None) -> pd.Series:
    if lookback <= 1:
        raise ValueError("lookback must be greater than 1")
    if len(series1) != len(series2):
        raise ValueError("Both series must have the same length")

    # Calculate the difference between the two series
    diff = series1 - series2

    if allow_cross == "up":
        crossover_mask = (diff <= 0) & (diff.shift(1) > 0)  # Only count the times it crosses down
    elif allow_cross == "down":
        crossover_mask = (diff >= 0) & (diff.shift(1) < 0)  # Only count the times it crosses up
    else:
        crossover_mask = ((diff >= 0) & (diff.shift(1) < 0)) | ((diff <= 0) & (diff.shift(1) > 0))  # Count both up and down crosses

    # Count the number of crossovers within the lookback period
    crossovers_count = crossover_mask.rolling(window=lookback).sum()

    # Check if the number of crossovers is below the threshold
    crossovers_below_threshold = crossovers_count <= max_cross

    return crossovers_below_threshold.astype(int)


# ---------------------------  COUNT ABOVE VALUE -------------------------- #
def count_above_value_lookback(series: pd.Series, value: float, lookback: int, min_consecutive_period: int) -> pd.Series:
    above_value = series > value
    if min_consecutive_period == 0:
        counts = above_value.shift(1).rolling(window=lookback).sum()
    else:
        rolling_counts = above_value.rolling(window=min_consecutive_period).sum()
        counts = rolling_counts.shift(1).rolling(window=lookback - min_consecutive_period + 1).apply(lambda x: (x >= min_consecutive_period).any(), raw=True)

    result = pd.Series(counts, index=series.index)

    # print(pd.concat([series.tail(40), result.tail(40)], axis=1))

    return result


def count_below_value_lookback(series: pd.Series, value: float, lookback: int, min_consecutive_period: int) -> pd.Series:
    below_value = series < value
    if min_consecutive_period == 0:
        counts = below_value.shift(1).rolling(window=lookback).sum()
    else:
        rolling_counts = below_value.rolling(window=min_consecutive_period).sum()
        counts = rolling_counts.shift(1).rolling(window=lookback - min_consecutive_period + 1).apply(lambda x: (x >= min_consecutive_period).any(), raw=True)

    result = pd.Series(counts, index=series.index)

    # print(pd.concat([series.tail(40), result.tail(40)], axis=1))

    return result
