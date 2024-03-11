from scrapy_poet import callback_for

from scrapy_project.page_objects.base_page_objects.product_page import (
    ProductPage,
)
from scrapy_redis.spiders import RedisSpider


class ProductSpider(RedisSpider):
    """
    input: redis queue
    output: product items
    """

    name = "base_product_spider"

    custom_settings = {
        "SCHEDULER": "scrapy_redis.scheduler.Scheduler",
        "DUPEFILTER_CLASS": "scrapy_redis.dupefilter.RFPDupeFilter",
        "CONCURRENT_REQUESTS": 6,
        "CONCURRENT_REQUESTS_PER_DOMAIN": 6,
        "DOWNLOAD_DELAY": 0,
        "DOWNLOAD_TIMEOUT": 120,
        "CLOSESPIDER_ITEMCOUNT": 15000,
        "CLOSESPIDER_TIMEOUT": 3600 * 3,
        "RETRY_HTTP_CODES": [],
        "HTTPERROR_ALLOWED_CODES": [404],
        "DOWNLOADER_MIDDLEWARES": {
            "scrapy.downloadermiddlewares.retry.RetryMiddleware": 90,
            'scrapy_proxies.RandomProxy': 100,
            "scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware": 110,
            "scrapy_poet.InjectionMiddleware": 543,
        },
        "ITEM_PIPELINES": {
            "scrapy_project.pipelines.EcommercePricesDBPipeline": 100,
        },
    }

    redis_batch_size = 50
    redis_key = "redis-product-spider:start_urls"

    parse = callback_for(ProductPage)
