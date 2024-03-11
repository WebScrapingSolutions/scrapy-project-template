import datetime

from peewee import *
from playhouse.postgres_ext import JSONField

from scrapy_project.utils.utils import CustomDatabaseProxy


class BaseModel(Model):
    class Meta:
        database = CustomDatabaseProxy()


class ProductItemModel(BaseModel):
    vendor = TextField(null=False)  # str
    status = TextField(null=False)  # str
    created = DateTimeField(null=False, default=datetime.datetime.now())
    updated = DateTimeField(null=True)

    # General Product Information
    availability = TextField(default="InStock", null=True)  # str
    color = TextField(null=True)  # str
    currency = TextField(null=True)  # str
    currencyRaw = TextField(null=True)  # str
    productId = TextField(null=True)  # str

    # Product Identification Numbers (GTIN)
    gtin = JSONField(null=True)  # List[Dict[str, str]]

    # Product Images
    images = JSONField(null=True)  # List[Dict[str, str]]
    mainImage = JSONField(null=True)  # Dict[str, Any]

    # Product Information
    mpn = TextField(null=True)  # str Manufacture Product Number
    name = TextField(null=True)  # str Product Name
    available_quantity = TextField(
        null=True
    )  # str How many products are available to order
    price = TextField(null=True)  # str Product Price
    regularPrice = TextField(null=True)  # str Regular product price
    size = TextField(null=True)  # str Product Size
    sku = TextField(null=True)  # str Product Article
    style = TextField(null=True)  # str Product Style

    # Additional product properties
    additionalProperties = JSONField(null=True)  # List[Dict[str, Any]]

    # Product URLs
    url = TextField(null=True)  # str
    canonicalUrl = TextField(null=True)  # str

    # Product Rating
    aggregateRating = JSONField(null=True)  # Dict[str, Any]

    # Product Brand Information
    brand = JSONField(null=True)  # Dict[str, Any]

    # Breadcrumbs (navigation path)
    breadcrumbs = JSONField(null=True)  # List[Dict[str, Any]]

    # Product Features
    features = JSONField(null=True)  # List[Dict[str, Any]]

    # Product Description
    description = TextField(null=True)  # str
    descriptionHtml = TextField(null=True)  # str

    # Product Options
    variants = JSONField(null=True)  # List[Dict[str, Any]]

    # Additional metadata
    metadata = JSONField(null=True)  # Dict[str, Any]

    class Meta:
        db_table = "product_item"


def connect_to_db(db_uri):
    db_handle = CustomDatabaseProxy(db_uri=db_uri)
    db_handle.create_tables([ProductItemModel])  # table creation example
    return db_handle
