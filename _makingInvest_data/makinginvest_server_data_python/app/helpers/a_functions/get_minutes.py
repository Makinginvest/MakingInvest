def get_minutes(timeframe):
    if timeframe == "1m":
        return 1
    elif timeframe == "3m":
        return 3
    elif timeframe == "5m":
        return 5
    elif timeframe == "15m":
        return 15
    elif timeframe == "30m":
        return 30
    elif timeframe == "1h":
        return 60
    elif timeframe == "2h":
        return 120
    elif timeframe == "4h":
        return 240
    elif timeframe == "6h":
        return 360
    elif timeframe == "8h":
        return 480
    elif timeframe == "12h":
        return 720
    elif timeframe == "1d":
        return 1440
    elif timeframe == "3d":
        return 4320
    elif timeframe == "1w":
        return 10080
    elif timeframe == "1M":
        return 43200


def get_df_minute(timeframe):
    if timeframe == "1m":
        return "1min"
    elif timeframe == "5m":
        return "5min"
    elif timeframe == "15m":
        return "15min"
    elif timeframe == "30m":
        return "30min"
    elif timeframe == "1h":
        return "1h"
    elif timeframe == "2h":
        return "2h"
    elif timeframe == "4h":
        return "4h"
    elif timeframe == "6h":
        return "6h"
    elif timeframe == "8h":
        return "8h"
    elif timeframe == "12h":
        return "12h"
    elif timeframe == "1d":
        return "1d"
    elif timeframe == "3d":
        return "3d"
    elif timeframe == "1w":
        return "1w"
    elif timeframe == "1M":
        return "1M"
    else:
        return None
