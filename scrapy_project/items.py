import scrapy


class ProductItem(scrapy.Item):
    vendor = scrapy.Field()
    status = scrapy.Field()
    created = scrapy.Field()
    updated = scrapy.Field()

    # General Product Information
    availability = scrapy.Field()
    color = scrapy.Field()
    currency = scrapy.Field()
    currencyRaw = scrapy.Field()
    productId = scrapy.Field()

    # Product Identification Numbers (GTIN)
    gtin = scrapy.Field()

    # Product Images
    images = scrapy.Field()
    mainImage = scrapy.Field()

    # Product Information
    mpn = scrapy.Field()
    name = scrapy.Field()
    available_quantity = scrapy.Field()
    price = scrapy.Field()
    regularPrice = scrapy.Field()
    size = scrapy.Field()
    sku = scrapy.Field()
    style = scrapy.Field()

    # Additional product properties
    additionalProperties = scrapy.Field()

    # Product URLs
    url = scrapy.Field()
    canonicalUrl = scrapy.Field()

    # Product Rating
    aggregateRating = scrapy.Field()

    # Product Brand Information
    brand = scrapy.Field()

    # Breadcrumbs (navigation path)
    breadcrumbs = scrapy.Field()

    # Product Features
    features = scrapy.Field()

    # Product Description
    description = scrapy.Field()
    descriptionHtml = scrapy.Field()

    # Product Options
    variants = scrapy.Field()

    # Additional metadata
    metadata = scrapy.Field()
