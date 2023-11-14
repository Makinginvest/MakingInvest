from fastapi import HTTPException
from _log_config.app_logger import app_logger
from app.models.user_model import UserModel
from app.a_database_client.db_connect_client import database_mongodb_client
import datetime as dt


async def update_user(user: dict, uid=None):
    try:
        user_model = UserModel(**user)
        if user_model.createdDateTime == None:
            user_model.createdDateTime = dt.datetime(2023, 1, 1)

        collection = database_mongodb_client["users"]
        mongo_user = await collection.find_one({"firebaseUserId": uid})

        update_user = {}

        # update only the fields present in the user object
        if mongo_user:
            for key in user_model.dict().keys():
                if key in user.keys():
                    update_user[key] = user_model.dict()[key]

            if "devTokens" in user.keys():
                devTokens = [mongo_user["devTokens"], user["devTokens"]]
                devTokens = [item for sublist in devTokens for item in sublist]
                devTokens = list(dict.fromkeys(devTokens))
                update_user["devTokens"] = user_model.dict()["devTokens"]

            if "favoriteSignals" in user.keys():
                update_user["favoriteSignals"] = user_model.dict()["favoriteSignals"]

            if "notificationsDisabled" in user.keys():
                update_user["notificationsDisabled"] = user_model.dict()["notificationsDisabled"]

            update_user["firebaseUserId"] = uid
            await collection.update_one({"firebaseUserId": uid}, {"$set": update_user}, upsert=True)

        else:
            user_model.firebaseUserId = uid
            await collection.insert_one(user_model.dict())

        # get user from mongodb
        mongo_user = await collection.find_one({"firebaseUserId": uid})

        # convert to user model
        user = UserModel(**mongo_user)

        return user.dict()

    except Exception as e:
        app_logger().info("Error generating news: ", e)
        raise HTTPException(400, detail=e)
