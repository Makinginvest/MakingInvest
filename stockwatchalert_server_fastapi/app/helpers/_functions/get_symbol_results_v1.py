from datetime import datetime, timedelta
from fastapi import HTTPException

from _project.log_config.app_logger import app_logger
from app._database.db_connect_client import database_mongodb_client
from app.utils.convert_bson_json import convert_bson_json


async def get_closed_signals_v1(nameCollection: str, nameId: str, nameVersion: str):
    try:
        collection = database_mongodb_client[nameCollection]

        days_60_ago = datetime.utcnow() - timedelta(days=60)
        data_60_days = (
            await collection.find(
                {
                    "exitDateTimeUtc": {"$gte": days_60_ago},
                    "isClosed": True,
                    "nameId": nameId,
                    "nameVersion": nameVersion,
                }
            )
            .sort("exitDateTimeUtc", -1)
            .to_list(length=None)
        )

        if len(data_60_days) == 0:
            return None

        data_60_days = convert_bson_json(data_60_days)

        return {
            "signals": data_60_days,
        }

    except Exception as e:
        app_logger().info("get_closed_signals_v1: ", str(e))
        raise HTTPException(500, detail=str(e))
