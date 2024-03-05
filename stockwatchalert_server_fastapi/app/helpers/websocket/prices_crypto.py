import aiohttp


async def getPricesCrypto():
    url = "https://api.binance.com/api/v3/ticker/price"
    data = []
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                for symbol_info in await response.json():
                    data.append({"s": symbol_info["symbol"], "p": convert_string_to_float(symbol_info["price"])})

                # keep symbols ending in USDT or BUSD
                data = [symbol for symbol in data if symbol["s"].endswith("USDT") or symbol["s"].endswith("BUSD")]
                return data
    except Exception as e:
        print(e)
        return []


def convert_string_to_float(string):
    if type(string) is str:
        return float(string)
    elif type(string) is float:
        return string
    else:
        return 0.0
