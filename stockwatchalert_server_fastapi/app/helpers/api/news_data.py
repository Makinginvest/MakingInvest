from app._database.db_connect_data import database_mongodb_data
from app._database.db_connect_client import database_mongodb_client
from app._firebase.firebase import firestore_db
from firebase_admin import firestore


async def update_all_news_mongodb_firestore_aggr():
    try:
        collection = database_mongodb_data["appControlsPrivate"]
        query = await collection.find_one({"name": "appControlsPrivate"})
        dtNewsAggrUpdatedData = None
        if query:
            dtNewsAggrUpdatedData = query.get("dtNewsAggrUpdated", None)

        collection = database_mongodb_client["appControlsPrivate"]
        query = await collection.find_one({"name": "appControlsPrivate"})
        dtNewsAggrUpdatedClient = None
        if query:
            dtNewsAggrUpdatedClient = query.get("dtNewsAggrUpdated", None)

        if dtNewsAggrUpdatedClient == dtNewsAggrUpdatedData:
            return {}

        news_crypto = await getNewsMongodb("crypto")
        news_forex = await getNewsMongodb("forex")
        news_stocks = await getNewsMongodb("stocks")
        news_all = await getNewsAll(type="all")

        await update_firestore_news_aggr(news_crypto=news_crypto, news_forex=news_forex, news_stocks=news_stocks)

        # write the last updated datetime to the database
        collection = database_mongodb_client["appControlsPrivate"]
        await collection.update_one({"name": "appControlsPrivate"}, {"$set": {"dtNewsAggrUpdated": dtNewsAggrUpdatedData}}, upsert=True)

        return {
            "status": "success",
        }

    except Exception as e:
        print(e)
        return {}


async def getNewsAll(type="all"):
    try:
        collection = database_mongodb_data["news"]
        data = await collection.find_one({"type": type})

        if data:
            # delete the _id
            data.pop("_id")
            collection = database_mongodb_client["news"]
            await collection.update_one({"type": type}, {"$set": {**data}}, upsert=True)
            return data

        return []

    except Exception as e:
        print(e)
        return []


async def getNewsMongodb(type):
    try:
        collection = database_mongodb_data["news"]
        data = await collection.find_one({"type": type})

        if data:
            collection = database_mongodb_client["news"]
            await collection.update_one(
                {"type": type},
                {
                    "$set": {
                        "data": data.get(
                            "data",
                            [],
                        )
                    }
                },
                upsert=True,
            )
            return data.get(
                "data",
                [],
            )

        return []

    except Exception as e:
        return []


async def update_firestore_news_aggr(news_crypto=None, news_forex=None, news_stocks=None):
    try:
        data = {
            "dataCrypto": news_crypto,
            "dataForex": news_forex,
            "dataStocks": news_stocks,
            "lastUpdatedFirestore": firestore.SERVER_TIMESTAMP,
        }

        firestore_db.collection("newsAggr").document("newsAggr").set(data, merge=True)
        return data

    except Exception as e:
        print("Error update_firestore_crypto_signals", e)
    return {}
