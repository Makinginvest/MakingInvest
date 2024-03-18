import os
from dotenv import load_dotenv
from fastapi import HTTPException
from app._firebase.firebase import firebase_auth


load_dotenv()
api_key = os.getenv("APIKEY")


def validate_apikey_json_webtoken(apikey: str = None, token: str = None):
    try:
        if apikey is None and token is None:
            print("Invalid apikey or token")
            raise HTTPException(
                401,
                detail="Invalid apikey or token",
            )

        if apikey == api_key:
            return True

        decoded_token = firebase_auth.verify_id_token(token)
        if decoded_token["uid"]:
            return True

        raise HTTPException(401, detail="Invalid apikey or token")

    except Exception as e:
        print("Invalid API Key or token: ", e)
        raise HTTPException(401, detail="Invalid apikey or token")


def validate_apikey_json_webtoken_bool(apikey: str = None, token: str = None) -> bool:
    try:
        if apikey is None and token is None:
            print("Invalid apikey or token")
            return False

        if apikey == api_key:
            return True

        decoded_token = firebase_auth.verify_id_token(token)
        if decoded_token["uid"]:
            return True

        return False

    except Exception as e:
        print("Invalid API Key or token: ", e)
        return False
