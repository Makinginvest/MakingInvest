import aiohttp
from _log_config.app_logger import app_logger


from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from app.a_firebase.a_validate_api_key import validate_apikey
import pandas as pd


router_symbols_rank_v0 = APIRouter()


@router_symbols_rank_v0.patch("/symbols-rank-crypto")
async def patch_signals(apikey: str = None):
    url = "https://api.coinpaprika.com/v1/tickers"
    try:
        validate_apikey(apikey)
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                data = await response.json()
                # delete  quotes if exist

        data = pd.DataFrame(data)
        data = data[["name", "symbol", "rank", "first_data_at", "last_updated"]]
        data.rename(columns={"first_data_at": "firstDataAt"}, inplace=True)
        data.rename(columns={"last_updated": "lastUpdated"}, inplace=True)
        # add USDT to symbol
        data["symbolFormatted"] = data.apply(lambda row: row["symbol"] + "/USDT:USDT", axis=1)
        data["symbol"] = data["symbol"] + "USDT"
        data = data.sort_values(by="rank")
        data.reset_index(drop=True, inplace=True)

        # write to csv
        # symbolFormatted  columns should have double quotes and a comma at the end when writing to csv
        data.to_csv("_datasets/data/_data_symbols_crypto_rank.csv", index=False)

        return data.to_dict("records")

    except HTTPException as e:
        app_logger.error(e)
        return e.detail
