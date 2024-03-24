import pandas as pd
import requests


def fetch_stocks_to_csv(api_url, headers, csv_filename):
    """
    Fetch stock list from the Alpaca API, filter for stocks under $100, and write to a CSV file.

    Parameters:
    - api_url: URL of the Alpaca API endpoint to fetch stock data.
    - headers: Headers required for authentication with the Alpaca API.
    - csv_filename: The name of the CSV file to write to.
    """
    # Fetch the data
    response = requests.get(api_url, headers=headers)
    if response.status_code == 200:
        # Convert JSON response to pandas DataFrame
        df = pd.DataFrame(response.json())

        # Filter for stocks under $100
        # df = df[df["price"] >= 1]
        # df = df[df["price"] <= 7]

        # Filter for stocks from NASDAQ, NYSE, AMEX, and CBOE exchanges
        keep_exchanges = ["NASDAQ", "NYSE", "AMEX", "CBOE"]
        df = df[df["exchange"].isin(keep_exchanges)]

        # Filter for assets of type "stock"
        # df = df[df["asset_class"] == "us_equity"]
        df = df[df["tradable"] == True]
        # remove where symbol containers "."
        # print(df["symbol"])
        df = df[~df["symbol"].str.contains(".", regex=False)]
        df = df[~df["symbol"].str.contains("-", regex=False)]
        df = df[~df["name"].str.contains("ETF", regex=False)]
        df = df[~df["name"].str.contains("%", regex=False)]

        columns = ["exchange", "symbol", "name", "status", "tradable"]

        # Write to CSV
        df[columns].to_csv(csv_filename, index=False)
    else:
        print("Failed to fetch data")


# Alpaca API endpoint
api_url = "https://paper-api.alpaca.markets/v2/assets?status=active&exchange=NYSE%2CNASDAQ&attributes="
headers = {"APCA-API-KEY-ID": "PKP54IQSJ4CAPG89OJ70", "APCA-API-SECRET-KEY": "WyaK46LT5OL7pFm6o5ScJelU6nGhAdPExJqtkujo", "accept": "application/json"}
csv_filename = "_project/datasets/data/_data_symbols_stock_us_market.csv"

# Fetch stock data and write to CSV
fetch_stocks_to_csv(api_url, headers, csv_filename)
