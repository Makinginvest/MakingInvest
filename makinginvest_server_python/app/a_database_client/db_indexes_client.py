from app.a_database_client.db_connect_client import database_mongodb_client


async def update_mongodb_indexes():
    try:

        await create_mongodb_index_users()
        await create_mongodb_index_symbols_by_signals(baseCollection="signalsCrypto")
        await create_mongodb_index_symbols_by_signals(baseCollection="signalsStocks")
        await create_mongodb_index_symbols_by_signals(baseCollection="signalsForex")
        await create_mongodb_index_symbols_by_signals(baseCollection="sSignalsCryptoTest")
        await create_mongodb_index_symbols_by_signals(baseCollection="sSignalsStocksTest")
        await create_mongodb_index_symbols_by_signals(baseCollection="sSignalsForexTest")

    except Exception as e:
        print("Error creating mongodb index: ", e)
        return True


async def create_mongodb_index_users():
    try:

        collection = database_mongodb_client[f"users"]
        await collection.create_index([("firebaseUserId", 1)], unique=True)
        return False

    except Exception as e:
        print("Error creating mongodb index: ", e)
        return True


async def create_mongodb_index_symbols_by_signals(baseCollection: str = "signalsCrypto"):
    try:
        collection = database_mongodb_client[f"{baseCollection}"]
        await collection.create_index([("entryDateTimeUtc", -1)], unique=False)
        await collection.create_index([("entryDateTimeUtc", 1)], unique=False)
        await collection.create_index([("isAlgo", 1)], unique=False)
        await collection.create_index([("name", 1)], unique=False)
        await collection.create_index([("nameVersion", 1)], unique=False)
        await collection.create_index([("symbol", 1)], unique=False)
        await collection.create_index([("name", 1), ("nameVersion", 1), ("isAlgo", 1), ("symbol", 1), ("entryDateTimeUtc", 1)], unique=False)
        await collection.create_index([("name", 1), ("nameVersion", 1), ("isAlgo", 1), ("symbol", 1), ("entryDateTimeUtc", -1)], unique=False)
        await collection.create_index([("name", 1), ("nameVersion", 1), ("isAlgo", 1), ("symbol", 1), ("isClosed", 1)], unique=False)
        await collection.create_index([("name", 1), ("nameVersion", 1), ("isAlgo", 1), ("symbol", 1), ("isClosed", -1)], unique=False)
        await collection.create_index([("name", 1), ("nameVersion", 1), ("isAlgo", 1), ("symbol", 1), ("isClosed", 1), ("entryType", 1)], unique=False)
        await collection.create_index([("name", 1), ("nameVersion", 1), ("isAlgo", 1), ("symbol", 1), ("isClosed", -1), ("entryType", 1)], unique=False)
        await collection.create_index([("name", 1), ("nameVersion", 1), ("isClosed", 1)], unique=False)
        await collection.create_index([("name", 1), ("nameVersion", 1), ("isClosed", -1)], unique=False)
        return False

    except Exception as e:
        print("Error creating mongodb index: ", e)
        return True
