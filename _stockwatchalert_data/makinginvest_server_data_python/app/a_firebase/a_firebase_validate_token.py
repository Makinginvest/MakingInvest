from fastapi import HTTPException
from app.a_firebase.firebase import firebase_auth


def firebase_validate_jsonwebtoken(token: str):
    try:

        if token == None:
            raise HTTPException(401, detail="Invalid Token")

        decoded_token = firebase_auth.verify_id_token(token)
        uid = decoded_token["uid"]
        return uid

    except Exception as e:
        print("Error validating token: ", e)
        raise HTTPException(401, detail="Invalid Token")


def firebase_validate_jsonwebtoken_bool(token: str) -> bool:
    try:

        if token == None:
            return False

        decoded_token = firebase_auth.verify_id_token(token)
        uid = decoded_token["uid"]
        return True

    except Exception as e:
        print("Error validating token: ", e)
        return False
