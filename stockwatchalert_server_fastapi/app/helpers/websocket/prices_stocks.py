import aiohttp
import pandas as pd


async def getPricesStocks():
    url = "https://financialmodelingprep.com/api/v3/available-traded/list?apikey=e9240f50007f36b71affe852b9cf2a83"

    try:
        symbols = await get_USDT_symbols_by_value("_project/datasets/data/_data_symbols_stock_options_sp500.csv")

        data = []

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                for symbol_info in await response.json():
                    data.append(
                        {
                            "s": symbol_info["symbol"],
                            "p": convert_string_to_float(symbol_info["price"]),
                        }
                    )
                data = [x for x in data if x["s"] in symbols]

        return data

    except Exception as e:
        print(e)
        return []


async def get_USDT_symbols_by_value(path="_project/datasets/data/_data_symbols_stock_options_sp500.csv"):
    symbols = pd.read_csv(path)
    symbols = symbols["symbol"].tolist()
    return symbols


def convert_string_to_float(string):
    if type(string) is str:
        return float(string)
    elif type(string) is float:
        return string
    else:
        return 0.0
