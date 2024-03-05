import pandas as pd
import numpy as np


def calculate_slope_degrees(close: pd.Series, lookback: int = 10) -> pd.DataFrame:
    # Calculate the slope
    slopes = (close - close.shift(lookback)) / close.shift(lookback) * 100
    slopes = (close - close.shift(lookback)) / lookback

    # Calculate the angle in degrees
    angles = np.degrees(np.arctan(slopes))

    # Create a new DataFrame with slopes and angles
    result = pd.DataFrame({"slope": slopes, "angle_degrees": angles})

    return result


def calculate_slope_degrees_pct(close: pd.Series, lookback: int = 10) -> pd.DataFrame:
    # Calculate the percent change
    percent_change = (close - close.shift(lookback)) / close.shift(lookback) * 100

    # Normalize the percent change values using min-max scaling
    normalized_percent_change = (percent_change - percent_change.min()) / (percent_change.max() - percent_change.min())

    # Map the normalized values to the desired range (0 to 180 degrees)
    mapped_percent_change = normalized_percent_change * 180

    # Calculate the angle in degrees
    angles = np.degrees(np.arctan(mapped_percent_change))

    # Create a new DataFrame with percent change and angles
    result = pd.DataFrame({"percent_change": percent_change, "angle_degrees": angles})

    return result
