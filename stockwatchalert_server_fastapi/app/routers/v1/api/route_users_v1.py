from fastapi import APIRouter
from fastapi.exceptions import HTTPException

from app._database.db_connect_client import database_mongodb_client
from app._firebase.a_firebase_validate_token import firebase_validate_jsonwebtoken
from app._firebase.a_validate_key_jsonwebtoken import validate_apikey_json_webtoken
from app._firebase.firebase import firestore_db
from _project.log_config.app_logger import app_logger

from app.helpers.api.users import delete_user, update_user
from app.utils.convert_fb_timestamp_datetime_obj import check_fb_timestamp_datetime_obj

router_users_v1 = APIRouter(prefix="/v1")


@router_users_v1.get("/users")
async def patch_signals(jsonWebToken: str = None, apikey: str = None, user: dict = None):
    try:
        validate_apikey_json_webtoken(apikey=apikey, token=jsonWebToken)

        collection = database_mongodb_client["users"]
        users = await collection.find().to_list(length=100000)

        for user in users:
            user["_id"] = str(user["_id"])

        return users

    except HTTPException as e:
        raise e

    except Exception as e:
        app_logger().info("Error generating news: ", e)
        raise HTTPException(400, detail=e)


@router_users_v1.get("/users", tags=["users"])
async def patch_signals(jsonWebToken: str = None, apikey: str = None, user: dict = None):
    try:
        validate_apikey_json_webtoken(apikey=apikey, token=jsonWebToken)

        collection = database_mongodb_client["users"]
        users = await collection.find().to_list(length=100000)

        for user in users:
            user["_id"] = str(user["_id"])

        print(users[0])

        return users

    except HTTPException as e:
        raise e

    except Exception as e:
        app_logger().info("Error generating news: ", e)
        raise HTTPException(400, detail=e)


@router_users_v1.patch("/users")
async def patch_signals(jsonWebToken: str = None, user: dict = None):
    try:
        uid = firebase_validate_jsonwebtoken(token=jsonWebToken)
        user = await update_user(user=user, uid=uid)
        return user

    except HTTPException as e:
        raise e

    except Exception as e:
        app_logger().info("Error generating news: ", e)
        raise HTTPException(400, detail=e)


@router_users_v1.delete("/users/userId/{userId}/delete-account")
async def patch_signals(jsonWebToken: str = None, user: dict = None, userId: str = None):
    try:
        uid = firebase_validate_jsonwebtoken(token=jsonWebToken)
        if uid != userId:
            raise HTTPException(
                400,
                detail="You can only delete your own account",
            )

        await delete_user(userId=userId)
        return user

    except HTTPException as e:
        raise e

    except Exception as e:
        app_logger().info("Error generating news: ", e)
        raise HTTPException(400, detail=e)


@router_users_v1.patch("/users-update-from-firestore")
async def patch_signals(apikey: str = None, token: str = None, user: dict = None):
    try:
        validate_apikey_json_webtoken(apikey=apikey, token=token)
        # pull all users from firestore
        docs = firestore_db.collection("users").stream()
        users = []

        for doc in docs:
            users.append(
                {
                    **doc.to_dict(),
                    "uid": doc.id,
                    "id": doc.id,
                }
            )
            users = [check_fb_timestamp_datetime_obj(user) for user in users]

        for user in users:
            await update_user(
                user=user,
                uid=user["uid"],
            )

        return users

    except HTTPException as e:
        raise e

    except Exception as e:
        app_logger().info("Error generating news: ", e)
        raise HTTPException(400, detail=e)
