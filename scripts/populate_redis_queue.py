import json
import redis

from scrapy_project.models import CustomDatabaseProxy, ProductItemModel
from scrapy_project.settings import DATABASE_URI, REDIS_URL


if __name__ == "__main__":
    # connect to db
    CustomDatabaseProxy(db_uri=DATABASE_URI)
    # select product that we want to insert to redis queue
    rows_to_insert = ProductItemModel.select().where((ProductItemModel.status == "NEW"))
    # convert it to a list of dicts
    json_urls = [json.dumps({"url": model.url}) for model in rows_to_insert]
    # insert to redis queue
    with redis.from_url(url=REDIS_URL) as redis_connect:
        redis_connect.lpush("redis-product-spider:start_urls", *json_urls)
