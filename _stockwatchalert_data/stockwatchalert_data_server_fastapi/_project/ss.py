import pandas as pd
import requests


def fetch_stocks_to_csv(api_url, csv_filename):
    """
    Fetch stock list from the API, filter for stocks under $100, and write to a CSV file.

    Parameters:
    - api_url: URL of the API endpoint to fetch stock data.
    - csv_filename: The name of the CSV file to write to.
    """
    # Fetch the data
    response = requests.get(api_url)
    if response.status_code == 200:
        # Convert JSON response to pandas DataFrame
        df = pd.DataFrame(response.json())

        # Convert price column to numeric, forcing errors to NaN (not a number)
        df["price"] = pd.to_numeric(df["price"], errors="coerce")

        # Filter for stocks under $100
        df = df[df["price"] >= 1]
        df = df[df["price"] <= 7]
        #
        keep_exchanges = ["NASDAQ", "NYSE", "AMEX", "CBOE"]
        df = df[df["exchangeShortName"].isin(keep_exchanges)]

        # type = stock
        df = df[df["type"] == "stock"]

        # Write to CSV
        df.to_csv(csv_filename, index=False)
    else:
        print("Failed to fetch data")


# API endpoint
api_url = "https://financialmodelingprep.com/api/v3/stock/list?apikey=bd2c777f360a804e003e03f88cef3fa9"

# Output CSV filename
csv_filename = "stocks_under_100.csv"

# Fetch stock data and write to CSV
fetch_stocks_to_csv(api_url, csv_filename)
