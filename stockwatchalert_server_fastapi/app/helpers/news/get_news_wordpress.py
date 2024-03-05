import aiohttp
from app.a_database_client.db_connect_client import database_mongodb_client


async def get_news_wordpress():
    collection = database_mongodb_client["news"]
    news = await collection.find_one({"type": "wordpress"})

    if news:
        news.pop("_id")
        return news
    return news


async def update_news_wordpress():
    url = "https://makinginvest.com/wp-json/wp/v2/all_posts"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data_raw = await response.json()
            data = []

            if data_raw:
                for d in data_raw:
                    data.append(
                        {
                            "id": d["id"],
                            "title": d["title"],
                            "text": remove_html_tags(d["content"]),
                            "date": None,
                            "dateString": d["date"],
                            "url": d["guid"],
                            "image": d["featured_media"][0],
                        }
                    )

            # sort by id
            data = sorted(data, key=lambda k: k["id"], reverse=True)

            # write to mongodb
            collection = database_mongodb_client["news"]
            await collection.update_one({"type": "wordpress"}, {"$set": {"data": data}}, upsert=True)

            # add index for type
            # await collection.create_index([("type", 1)])

            return data


def remove_html_tags(text):
    import re

    clean = re.compile("<.*?>")
    clean = re.sub(clean, "", text)

    return clean
