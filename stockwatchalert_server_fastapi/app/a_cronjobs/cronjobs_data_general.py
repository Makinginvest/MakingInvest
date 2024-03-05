import os

import aiocron
from dotenv import load_dotenv

from app.helpers.news.get_news_wordpress import update_news_wordpress

load_dotenv()
is_production = os.getenv("PRODUCTION")
is_allow_cron = os.getenv("ALLOW_CRON")
is_data_mode = os.getenv("DATA_MODE")




# ------------------------------  NEWS CRON ----------------------------- #
@aiocron.crontab("8 * * * *")
async def cron_news():
    if is_production == "True" and is_allow_cron == "True" and is_data_mode == "True":
        await update_news_wordpress()
        print("News updated")
