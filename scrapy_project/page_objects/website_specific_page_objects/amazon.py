from scrapy_project.page_objects.base_page_objects import ProductPage
from price_parser import Price


class AmazonProductPage(ProductPage):
    """
    https://www.amazon.com/High-Protein-Bars-thinkThin-Non-GMO/dp/B00VXQGKRM
    """

    def get_vendor(self):
        return "amazon.com"

    def get_availability(self):
        product_is_available = self.xpath(
            "//div[@id='availability']/span/text()"
        ).get()
        # Check if any product is available
        if product_is_available:
            if any(
                s in product_is_available.lower().strip()
                for s in ["in stock", "usually ships within"]
            ):
                return "InStock"
            else:
                return "OutOfStock"
        else:
            return "OutOfStock"

    def get_color(self):
        return None

    def get_currency(self):
        price_string = self.get_current_price()
        if Price.fromstring(price_string).currency == "$":
            return "USD"
        else:
            return None

    def get_currencyRaw(self):
        price_string = self.get_current_price()
        return Price.fromstring(price_string).currency

    def get_productId(self):
        return self.get_canonicalUrl()

    def get_gtin(self):
        return []

    def get_images(self):
        image_selectors = [
            "//div[@id='altImages']//li//img/@src",
            "//div[@id='imgTagWrapperId']/img/@src",
        ]

        image_urls = next(
            (
                urls
                for selector in image_selectors
                if (urls := self.xpath(selector).getall())
            ),
            [],
        )

        image_urls = [
            ".".join(image_url.rsplit(".", 2)[::2])
            for image_url in image_urls
            if "gif" not in image_url
        ]

        image_urls = list(set(image_urls))
        return image_urls

    def get_mainImage(self):
        mainImage_url = self.xpath(
            "//div[@id='imgTagWrapperId']/img/@src"
        ).get()
        return mainImage_url

    def get_mpn(self):
        attributes = self.get_additionalProperties()
        mpn_column_names = ["Item model number", "Part Number"]
        return next(
            (
                attributes.get(name)
                for name in mpn_column_names
                if name in attributes.keys()
            ),
            None,
        )

    def get_name(self):
        return self.xpath("//span[@id='productTitle']/text()").get()

    def get_available_quantity(self):
        # there is no simple way to collect available quantity on amazon.com
        # if you really need this value - create a dedicated spider
        return None

    def get_current_price(self):
        if self.get_availability() != "InStock":
            return None

        selectors = [
            "//div[@class='a-section a-spacing-micro']"
            "//span[@class='a-offscreen']/text()"
            "//span[contains(text(), 'List Price')]"
            "//span[@class='a-offscreen']/text()",
            "//span[@id='price_inside_buybox']/text()",
        ]

        for xpath in selectors:
            price = self.xpath(xpath).get()
            if price:
                return price
        return None

    def get_price(self):
        price_string = self.get_current_price()
        return Price.fromstring(price_string).amount_text

    def get_regularPrice(self):
        regularPrice_string = self.xpath(
            "//span[contains(text(),'List Price:')]"
            "/span/span[@class='a-offscreen']/text()"
        ).get()
        return Price.fromstring(regularPrice_string).amount_text

    def get_sku(self):
        return self.url.split("/dp/", 1)[1]

    def get_additionalProperties(self):
        additionalProperties = {}

        def extract_attributes(
            xpath_query, name_query, info_query, name_clean=True
        ):
            for row in self.xpath(xpath_query):
                attribute_name = row.xpath(name_query).get()
                if attribute_name:
                    attribute_name = attribute_name.strip()
                    if name_clean:
                        attribute_name = attribute_name.split(":")[0]
                    attribute_name = self.clean_string(attribute_name)
                    if (
                        attribute_name != "Customer Reviews"
                    ):  # this attribute should be stored in a separate field
                        attributes_info = row.xpath(info_query).getall()
                        attributes_info = self.clean_string(attributes_info)
                        additionalProperties[attribute_name] = attributes_info

        tech_details = self.xpath("//div[@id='prodDetails']//table//tr")
        if len(tech_details) == 0:
            extract_attributes(
                "//div[contains(@id, 'productOverview')]//tr",
                "./td[1]/span//text()",
                "./td[2]/span[contains(@class,'a-size-base')]//text()",
            )
        else:
            extract_attributes(
                "//div[@id='prodDetails']//table//tr",
                "./th/text()",
                "./td//text()",
                name_clean=False,
            )

        extract_attributes(
            "//div[@id='detailBullets_feature_div']"
            "/ul/li/span[@class='a-list-item']",
            "./span[1]//text()",
            "./span[2]/text()",
        )

        return additionalProperties

    def clean_string(self, string):
        if isinstance(string, list):
            string = " ".join(string)
        return (
            string.replace("\n", "")
            .replace("\u200e", "")
            .replace("\u200f", "")
            .strip()
        )

    def get_canonicalUrl(self):
        return self.url.split("?")[0]

    def get_aggregateRating(self):
        ratingValue = float(
            self.xpath(
                "//span[contains(@class,'reviewCountTextLinkedHistogram')]"
                "//a/span/text()"
            ).get()
        )

        number_str = "".join(
            filter(
                str.isdigit,
                self.xpath(
                    "//a[@id='acrCustomerReviewLink']/span/text()"
                ).get(),
            )
        )
        reviewCount = int(number_str)
        return {
            "bestRating": 5,
            "ratingValue": ratingValue,
            "reviewCount": reviewCount,
        }

    def get_brand(self):
        additionalProperties = self.get_additionalProperties()
        return additionalProperties.get("Brand") or additionalProperties.get(
            "Manufacturer"
        )

    def get_breadcrumbs(self):
        breadcrumb_elements = self.xpath(
            "//div[contains(@*, 'breadcrumbs')]//ul/li/span/a"
        )
        breadcrumbs = [
            {
                "url": element.xpath("./@href").get(),
                "name": element.xpath("./text()")
                .get()
                .strip()
                .replace("\n", ""),
            }
            for element in breadcrumb_elements
        ]
        return breadcrumbs

    def get_features(self):
        return []

    def get_description(self):
        product_description = self.xpath(
            "//h3[contains(span, 'Product Description')]"
            "//following::p[1]/span/text()"
        ).getall()
        if not product_description:
            product_description = self.xpath(
                "//div[@id='productDescription']/p/span/text()"
            ).getall()

        return product_description

    def get_descriptionHtml(self):
        product_description_html = self.xpath(
            "//h3[contains(span, 'Product Description')]"
            "//following::p[1]/span"
        ).getall()
        if not product_description_html:
            product_description_html = self.xpath(
                "//div[@id='productDescription']/p/span"
            ).getall()
        return product_description_html

    def get_variants(self):
        return []
