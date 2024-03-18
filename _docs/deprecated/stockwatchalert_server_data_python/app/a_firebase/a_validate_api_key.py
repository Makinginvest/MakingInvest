import os
from dotenv import load_dotenv
from fastapi import HTTPException
from httplib2 import Http


load_dotenv()
api_key = os.getenv("APIKEY")


def validate_apikey(key: str):
    try:
        if key == api_key:
            return True
        else:
            raise HTTPException(401, detail="Invalid apikey")

    except Exception as e:
        print("Invalid API Key: ", e)
        raise HTTPException(401, detail="Invalid API Key")
