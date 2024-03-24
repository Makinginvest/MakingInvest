from _project.log_config.app_logger import app_logger
from app._database.db_connect_client import database_mongodb_client


from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from app._firebase.a_validate_api_key import validate_apikey
from app._firebase.a_validate_key_jsonwebtoken import validate_apikey_json_webtoken
from app.helpers.api.news_data import update_all_news_mongodb_firestore_aggr


router_news_v1 = APIRouter(prefix="/v1")


@router_news_v1.get("/news-all")
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

    except HTTPException as e:
        raise e

    except Exception as e:
        app_logger().info("Error generating news: ", e)
        raise HTTPException(500, detail=e)


@router_news_v1.patch("/news-all")
async def patch_signals(apikey: str = None):
    try:
        validate_apikey(apikey)
        news = await update_all_news_mongodb_firestore_aggr()
        return news

    except HTTPException as e:
        raise e

    except Exception as e:
        app_logger().info("Error generating news: ", e)
        raise HTTPException(500, detail=e)
