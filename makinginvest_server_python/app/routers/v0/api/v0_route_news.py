from _log_config.app_logger import app_logger
from app.a_database_client.db_connect_client import database_mongodb_client
from app.helpers.news.get_news_wordpress import get_news_wordpress, update_news_wordpress


from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from app.a_firebase.a_validate_api_key import validate_apikey
from app.a_firebase.a_validate_key_jsonwebtoken import validate_apikey_json_webtoken
from app.helpers.data.get_news_data import update_all_news_mongodb_firestore_aggr


v0_router_news = APIRouter()


@v0_router_news.get("/news-all")
async def get_signals(jsonWebToken: str = None, apikey: str = None, limit: int = None):
    try:
        validate_apikey_json_webtoken(apikey=apikey, token=jsonWebToken)

        collection = database_mongodb_client["news"]
        news = await collection.find_one({"type": "all"})

        # check if dataCrypto exists
        if limit:
            if news and news["dataCrypto"]:
                if isinstance(news["dataCrypto"], list):
                    if len(news["dataCrypto"]) >= limit:
                        news["dataCrypto"] = news["dataCrypto"][:limit]
            if news and news["dataStocks"]:
                if isinstance(news["dataStocks"], list):
                    if len(news["dataStocks"]) >= limit:
                        news["dataStocks"] = news["dataStocks"][:limit]
            if news and news["dataForex"]:
                if isinstance(news["dataForex"], list):
                    if len(news["dataForex"]) >= limit:
                        news["dataForex"] = news["dataForex"][:limit]

            news.pop("_id")
            return news

        if news:
            news.pop("_id")
            return news

        collection.createIndex({type: 1})
        return news

    # create index on type

    except HTTPException as e:
        raise e

    except Exception as e:
        app_logger().info("Error generating news: ", e)
        raise HTTPException(500, detail=e)


@v0_router_news.patch("/news-all")
async def patch_signals(apikey: str = None):
    try:
        validate_apikey(apikey)
        news = await update_all_news_mongodb_firestore_aggr()
        return {
            "news": news,
        }

    except HTTPException as e:
        raise e

    except Exception as e:
        app_logger().info("Error generating news: ", e)
        raise HTTPException(500, detail=e)


@v0_router_news.get("/news-wordpress")
async def patch_signals(apikey: str = None, jsonWebToken: str = None):
    try:
        validate_apikey_json_webtoken(apikey=apikey, token=jsonWebToken)
        news = await get_news_wordpress()
        news = news.get("data", [])
        return {
            "news": news,
        }

    except HTTPException as e:
        raise e

    except Exception as e:
        app_logger().info("Error generating news: ", e)
        raise HTTPException(500, detail=e)


@v0_router_news.patch("/news-wordpress")
async def patch_signals(apikey: str = None):
    try:
        validate_apikey(apikey)
        news = await update_news_wordpress()
        return {"news": news}

    except HTTPException as e:
        raise e

    except Exception as e:
        app_logger().info("Error generating news: ", e)
        raise HTTPException(500, detail=e)
