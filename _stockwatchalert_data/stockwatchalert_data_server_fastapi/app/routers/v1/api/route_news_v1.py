from _project.log_config.app_logger import app_logger


from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from app._security.a_validate_api_key import validate_apikey

from app.helpers.data.get_news_data import update_all_news_mongodb_aggr

router = APIRouter(prefix="/v1")


@router.patch("/news-all")
async def patch_signals(apikey: str = None):
    try:
        validate_apikey(apikey)
        news = await update_all_news_mongodb_aggr()
        return news

    except HTTPException as e:
        raise e

    except Exception as e:
        app_logger().info("Error generating news: ", e)
        raise HTTPException(500, detail=e)
