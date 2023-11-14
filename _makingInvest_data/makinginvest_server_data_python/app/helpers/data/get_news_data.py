from datetime import datetime, timezone
import aiohttp
import pandas as pd
from pandas import Timestamp
from app.a_database_data.db_connect_data import database_mongodb_data


import os
from dotenv import load_dotenv

load_dotenv()


async def update_all_news_mongodb_aggr():
    try:
        news_crypto = await update_news_crypto_mongodb_aggr()
        news_forex = await update_news_forex_mongodb_aggr()
        news_stocks = await updates_new_stocks_mongodb_aggr()

        data = await update_database_news_aggr(news_crypto=news_crypto, news_forex=news_forex, news_stocks=news_stocks)

        if "lastUpdatedFirestore" in data:
            del data["lastUpdatedFirestore"]

        return data

    except Exception as e:
        print(e)
        return {}


async def update_news_crypto_mongodb_aggr():
    try:
        news = await get_news_crypto_data(type="crypto_news", page_limit=5)
        collection = database_mongodb_data["news"]
        await collection.update_one({"type": "crypto"}, {"$set": {"data": news}}, upsert=True)
        return news

    except Exception as e:
        print(e)
        return []


async def update_news_forex_mongodb_aggr():
    try:
        news = await get_news_crypto_data(type="forex_news", page_limit=5)
        collection = database_mongodb_data["news"]
        await collection.update_one({"type": "forex"}, {"$set": {"data": news}}, upsert=True)
        return news

    except Exception as e:
        print(e)
        return []


async def updates_new_stocks_mongodb_aggr():
    try:
        news = await get_news_stocks(limit=100)
        collection = database_mongodb_data["news"]
        await collection.update_one({"type": "stocks"}, {"$set": {"data": news}}, upsert=True)
        return news

    except Exception as e:
        print(e)
        return []


async def update_database_news_aggr(news_crypto=None, news_forex=None, news_stocks=None):
    try:
        news_crypto = sorted(news_crypto, key=lambda k: k["publishedDate"], reverse=True)
        last_update_news_crypto = news_crypto[0]["publishedDate"] if len(news_crypto) > 0 else pd.to_datetime("2000-01-01 00:00:00+00:00")

        news_forex = sorted(news_forex, key=lambda k: k["publishedDate"], reverse=True)
        last_update_news_forex = news_forex[0]["publishedDate"] if len(news_forex) > 0 else pd.to_datetime("2000-01-01 00:00:00+00:00")

        news_stocks = sorted(news_stocks, key=lambda k: k["publishedDate"], reverse=True)
        last_update_news_stocks = news_stocks[0]["publishedDate"] if len(news_stocks) > 0 else pd.to_datetime("2000-01-01 00:00:00+00:00")

        # get the news of the last update last_update_news_crypto, last_update_news_forex, last_update_news_stocks
        last_update_news = None
        arr = [last_update_news_crypto, last_update_news_forex, last_update_news_stocks]
        arr = sorted(arr, reverse=True)
        last_update_news = arr[0]

        data = {
            "dataCrypto": news_crypto,
            "dataForex": news_forex,
            "dataStocks": news_stocks,
            "dtNewsCryptoUpdated": last_update_news_crypto,
            "dtNewsForexUpdated": last_update_news_forex,
            "dtNewsStocksUpdated": last_update_news_stocks,
            "dtNewsAggrUpdated": last_update_news,
        }

        dtNewsAggrUpdated = pd.to_datetime("1999-01-01 00:00:00+00:00")
        collection_app_controls_private = database_mongodb_data["appControlsPrivate"]
        current_doc = await collection_app_controls_private.find_one({"name": "appControlsPrivate"})

        if current_doc and current_doc.get("dtNewsAggrUpdated"):
            dtNewsAggrUpdated = current_doc.get("dtNewsAggrUpdated")
            dtNewsAggrUpdated = str(dtNewsAggrUpdated)
            dtNewsAggrUpdated = datetime.strptime(dtNewsAggrUpdated, "%Y-%m-%d %H:%M:%S")
            dtNewsAggrUpdated = dtNewsAggrUpdated.replace(tzinfo=timezone.utc)
            dtNewsAggrUpdated = dtNewsAggrUpdated.strftime("%Y-%m-%d %H:%M:%S+00:00")
            dtNewsAggrUpdated = pd.to_datetime(dtNewsAggrUpdated)

        if last_update_news > dtNewsAggrUpdated:
            collection_news_aggr = database_mongodb_data["news"]
            await collection_news_aggr.update_one(
                {"type": "all"},
                {"$set": {**data}},
                upsert=True,
            )

            collection_app_controls_private = database_mongodb_data["appControlsPrivate"]
            await collection_app_controls_private.update_one(
                {"name": "appControlsPrivate"},
                {"$set": {"name": "appControlsPrivate", "dtNewsAggrUpdated": last_update_news}},
                upsert=True,
            )

        return data

    except Exception as e:
        print("Error update_firestore_crypto_signals", e)
    return {}


async def get_news_crypto_data(type="crypto_news", page_limit=10):
    api_key = os.getenv("FINANCIALMODELINGPREP_APIKEY")
    try:
        async with aiohttp.ClientSession() as session:
            df = pd.DataFrame()
            for i in range(0, page_limit):
                url = f"https://financialmodelingprep.com/api/v4/{type}?page={i}&apikey={api_key}"
                async with session.get(url) as response:
                    data = await response.json()
                    res = []
                    for d in data:
                        r = {
                            "publishedDate": d["publishedDate"],
                            "title": d["title"],
                            "image": d["image"],
                            "site": d["site"],
                            "text": remove_html_tags(d["text"]),
                            "url": d["url"],
                            "symbol": d["symbol"],
                        }
                        res.append(r)

                    _df = pd.DataFrame(res)
                    _df["publishedDate"] = pd.to_datetime(_df["publishedDate"])
                    _df.insert(0, "time", _df["publishedDate"])
                    _df.insert(0, "timeUtc", _df["publishedDate"])
                    _df.insert(1, "timeEst", _df["publishedDate"] - pd.Timedelta(hours=5)),
                    _df = _df.set_index("time")
                    _df = _df.sort_index()

                    df = df.append(_df)

            return df.to_dict("records")
    except Exception as e:
        print(f"error:", e)
        return None


async def get_news_stocks(limit=50):
    api_key = os.getenv("FINANCIALMODELINGPREP_APIKEY")
    try:
        async with aiohttp.ClientSession() as session:
            df = pd.DataFrame()
            url = f"https://financialmodelingprep.com/api/v3/stock_news?limit={limit}&apikey={api_key}"

            async with session.get(url) as response:
                data = await response.json()
                res = []
                for d in data:
                    r = {
                        "publishedDate": d["publishedDate"],
                        "title": d["title"],
                        "image": d["image"],
                        "site": d["site"],
                        "text": remove_html_tags(d["text"]),
                        "url": d["url"],
                        "symbol": d["symbol"],
                        "publishedDate": d["publishedDate"],
                    }
                    res.append(r)

                _df = pd.DataFrame(res)
                # add +00:00 to the end of the date string if it doesn't exist
                _df["publishedDate"] = _df["publishedDate"].apply(lambda x: x if x[-6:] == "+00:00" else x + "+00:00")
                _df["publishedDate"] = pd.to_datetime(_df["publishedDate"])
                _df["publishedDate"] = _df["publishedDate"] + pd.Timedelta(hours=5)
                _df.insert(0, "time", _df["publishedDate"])
                _df.insert(0, "timeUtc", _df["publishedDate"])
                _df.insert(1, "timeEst", _df["publishedDate"] - pd.Timedelta(hours=5)),
                _df = _df.set_index("time")
                _df = _df.sort_index()

                df = df.append(_df)

            return df.to_dict("records")
    except Exception as e:
        print(f"error:", e)
        return None


def convert_timestamp_to_string(timestamp: Timestamp) -> str:
    if timestamp is None:
        return None
    return int(timestamp.timestamp() * 1000)


def remove_html_tags(text):
    """Remove html tags from a string"""
    import re

    clean = re.compile("<.*?>")
    return re.sub(clean, "", text)
