from app._database_data.db_connect_data import database_mongodb_data


async def update_mongodb_indexes():
    try:

        timeframes_crypto = ["5m", "15m", "30m", "1h", "2h", "4h", "6h", "8h", "12h", "1d"]
        timeframes_stocks = ["5m", "15m", "30m", "1h", "2h", "4h", "1d"]
        timeframes_forex = ["5m", "15m", "30m", "1h", "2h", "4h", "1d"]

        for timeframe in timeframes_crypto:
            await create_mongodb_index_symbols_by_signals(baseCollection=f"historicalCrypto{timeframe}")
        for timeframe in timeframes_stocks:
            await create_mongodb_index_symbols_by_signals(baseCollection=f"historicalStocks{timeframe}")
        for timeframe in timeframes_forex:
            await create_mongodb_index_symbols_by_signals(baseCollection=f"historicalForex{timeframe}")

    except Exception as e:
        print("Error creating mongodb index: ", e)
        return True


async def create_mongodb_index_symbols_by_signals(baseCollection: str = "signalsCrypto"):
    try:

        collection = database_mongodb_data[f"{baseCollection}"]
        await collection.create_index([("symbol", 1)], unique=False)
        await collection.create_index([("dateTimeUtc", 1)], unique=False)
        await collection.create_index([("dateTimeUtc", -1)], unique=False)
        await collection.create_index([("timeframe", 1)], unique=False)
        await collection.create_index([("symbol", 1), ("timeframe", 1)], unique=False)
        await collection.create_index([("symbol", 1), ("dateTimeUtc", 1), ("timeframe", 1)], unique=True)
        await collection.create_index([("symbol", 1), ("dateTimeUtc", -1), ("timeframe", 1)], unique=True)
        return False

    except Exception as e:
        print("Error creating mongodb index: ", e)
        return True
