from scrapy_project.models import (
    ProductItemModel,
)
from scrapy_project.pipelines import BaseDBPipeline


class EcommercePricesDBPipeline(BaseDBPipeline):

    max_items = 1000

    def insert_to_db(self, items):
        ProductItemModel.insert_many(items).execute()
