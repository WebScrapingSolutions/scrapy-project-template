from datetime import datetime

import web_poet
import attr

from scrapy_project.items import ProductItem


@attr.define
class ProductPage(web_poet.WebPage):
    page_params: web_poet.PageParams
    http: web_poet.HttpClient

    def to_item(self):
        item = ProductItem()
        item["vendor"] = self.get_vendor()
        item["status"] = self.get_status()

        item["updated"] = self.get_updated()

        # General Product Information
        item["availability"] = self.get_availability()
        item["color"] = self.get_color()
        item["currency"] = self.get_currency()
        item["currencyRaw"] = self.get_currencyRaw()
        item["productId"] = self.get_productId()

        # Product Identification Numbers (GTIN)
        item["gtin"] = self.get_gtin()

        # Product Images
        item["images"] = self.get_images()
        item["mainImage"] = self.get_mainImage()

        # Product Information
        item["mpn"] = self.get_mpn()
        item["name"] = self.get_name()
        item["available_quantity"] = self.get_available_quantity()
        item["price"] = self.get_price()
        item["regularPrice"] = self.get_regularPrice()
        item["size"] = self.get_size()
        item["sku"] = self.get_sku()
        item["style"] = self.get_style()

        # Additional product properties
        item["additionalProperties"] = self.get_additionalProperties()

        # Product URLs
        item["url"] = self.url
        item["canonicalUrl"] = self.get_canonicalUrl()

        # Product Rating
        item["aggregateRating"] = self.get_aggregateRating()

        # Product Brand Information
        item["brand"] = self.get_brand()

        # Breadcrumbs (navigation path)
        item["breadcrumbs"] = self.get_breadcrumbs()

        # Product Features
        item["features"] = self.get_features()

        # Product Description
        item["description"] = self.get_description()
        item["descriptionHtml"] = self.get_descriptionHtml()

        # Product Options
        item["variants"] = self.get_variants()

        # Additional metadata
        item["metadata"] = self.get_metadata()
        yield item

    def get_vendor(self):
        return None

    def get_status(self):
        return "NEW"

    def get_created(self):
        return None

    def get_updated(self):
        return None

    def get_availability(self):
        return None

    def get_color(self):
        return None

    def get_currency(self):
        return None

    def get_currencyRaw(self):
        return None

    def get_productId(self):
        return None

    def get_gtin(self):
        return None

    def get_images(self):
        return None

    def get_mainImage(self):
        return None

    def get_mpn(self):
        return None

    def get_name(self):
        return None

    def get_available_quantity(self):
        return None

    def get_price(self):
        return None

    def get_regularPrice(self):
        return None

    def get_size(self):
        return None

    def get_sku(self):
        return None

    def get_style(self):
        return None

    def get_additionalProperties(self):
        return None

    def get_canonicalUrl(self):
        return None

    def get_aggregateRating(self):
        return None

    def get_brand(self):
        return None

    def get_breadcrumbs(self):
        return None

    def get_features(self):
        return None

    def get_description(self):
        return None

    def get_descriptionHtml(self):
        return None

    def get_variants(self):
        return None

    def get_metadata(self):
        # Get current UTC time
        current_utc_time = datetime.utcnow()
        # Format the time in ISO 8601 format
        formatted_time = current_utc_time.strftime("%Y-%m-%dT%H:%M:%SZ")
        return {"dateDownloaded": formatted_time, "probability": 1}
