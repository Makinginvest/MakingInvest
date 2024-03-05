from app.a_database_data.db_connect_data import database_mongodb_data


async def get_market_analysis():
    collection = database_mongodb_data["marketAnalysis"]
    res = await collection.find_one({"name": "marketAnalysis"})
    return res
