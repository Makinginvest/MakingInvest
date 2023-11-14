import os
from dotenv import load_dotenv
import pandas as pd
from app.a_firebase.firebase import firestore_db

load_dotenv()
is_production = os.getenv("PRODUCTION")
is_allow_cron = os.getenv("ALLOW_CRON")
is_data_mode = os.getenv("DATA_MODE")
is_websocket_mode = os.getenv("WEBSOCKET_MODE")


async def update_future_prices_firestore():

    if is_production != "True":
        return

    try:
        symbols = pd.read_csv("_datasets/data/_data_symbols_crypto_futures.csv")
        symbols["symbol"] = symbols["symbol"].str.replace("/", "")

        firestore_db.collection("symbolsFuturesAggr").document("futures").set({"data": symbols.to_dict("records")})

        return symbols.to_dict("records")

    except Exception as e:
        print(e)
        raise e
