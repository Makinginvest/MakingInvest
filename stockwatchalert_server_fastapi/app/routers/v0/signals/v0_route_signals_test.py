from fastapi import APIRouter
from fastapi.exceptions import HTTPException

from _log_config.app_logger import app_logger
from app.a_firebase.a_validate_api_key import validate_apikey


router = APIRouter()


#
