from fastapi import HTTPException
from _log_config.app_logger import app_logger
from app.a_database_client.db_connect_client import database_mongodb_client
from app.a_firebase.firebase import firebase_auth, firestore_db


async def delete_user(userId=None):
    try:
        firebase_auth.delete_user(userId)

        collection = database_mongodb_client["users"]
        await collection.delete_one({"firebaseUserId": userId})

        firestore_db.collection("users").document(userId).delete()

        return True

    except Exception as e:
        app_logger().info("Error generating news: ", e)
        raise HTTPException(400, detail=e)
