import logging
from abc import ABC
from typing import Any, Iterable
from urllib import parse

import scrapy
from scrapy.http import Request, TextResponse

from scrapy_project.settings import (
    SCRAPEOPS_API_KEY,
)


class GoogleSearchLinksSpider(scrapy.Spider, ABC):
    """
    Collect links from google search, no older than 7 days.
    Spider gets initial domain links from google sheets by google api.

    Use spider arguments to start gathering links of exact domain
    or provide the spider with args in case it runs on Zyte.
    Example: scrapy crawl google_search_links_parser -a domain_link="https://www.example.com"

    see https://scrapeops.io/docs/proxy-aggregator/advanced-functionality/auto-extract/ for reference
    """

    name = "google_search_links_parser"

    custom_settings = {
        "DOWNLOADER_MIDDLEWARES": {},
        "ITEM_PIPELINES": {},
        "CONCURRENT_REQUESTS": 5,
        "DOWNLOAD_TIMEOUT": 120,
        "DOWNLOAD_DELAY": 0,
        "RETRY_TIMES": 1,
    }

    def start_requests(self) -> Iterable[Request]:
        domain_links = ["bbc.com", "cnn.com"]
        for domain_link in domain_links:
            yield from self.generate_request_to_google_search(
                domain=parse.urlparse(domain_link).netloc,
                initial_link=domain_link,
            )

    def generate_request_to_google_search(
        self, domain: str, initial_link: str
    ) -> Iterable[Request]:
        url = self.get_google_url(page=0, domain=domain)
        yield scrapy.Request(
            url=url,
            cb_kwargs=dict(
                domain=domain,
                initial_link=initial_link,
            ),
        )

    def parse(self, response: TextResponse, **cb_kwargs: Any) -> Any:
        data = response.json().get("data")
        if data:
            results = data.get("organic_results") or data.get("articles")
            logging.info(f"found {len(results)} results")
            for result in results:
                if not self.is_valid_link(
                    initial_link=cb_kwargs.get("initial_link"),
                    link=result.get("link"),
                ):
                    continue
                yield {
                    "url": result.get("link"),
                    "domain": cb_kwargs.get("domain"),
                }
            page = self.get_page_number(data)
            if page > 0:
                url = self.get_google_url(
                    page=page, domain=cb_kwargs.get("domain")
                )
                yield scrapy.Request(
                    url=url,
                    cb_kwargs=cb_kwargs,
                )
        else:
            logging.warning(
                "api.scraperapi.com did NOT return relevant results"
            )

    @staticmethod
    def get_google_url(page: int, domain: str) -> str:
        """
        Find results from specific dates:
            as_qdr=x
        Swap out x for the following to limit the search to only files first indexed in:
            d - the previous 24 hours
            w - the previous seven days
            m - the previous month
            y - past year
            mn - the previous n number of months. So m2 would be the previous two, m3 would be three, and so on.
        Does work into double digits
        """
        # feel free to edit google url to fit your use case
        google_url = (
            f"https://www.google.com/search?q=site:{domain}&"
            f"as_qdr=w&tbm=nws&start={page}&num=100"
        )
        url = (
            f"https://proxy.scrapeops.io/v1/?api_key={SCRAPEOPS_API_KEY}"
            f"&url={parse.quote_plus(google_url)}"
            "&auto_extract=google"
        )
        return url

    def get_page_number(self, data: dict) -> int:
        pagination = data.get("pagination")
        pagination_url = pagination.get("load_more_url")
        page = 0
        if pagination_url:
            page = pagination_url.split("start%3D")[1].split(
                "%26sa%3DN&autoparse="
            )[0]
        else:
            if pagination.get("next_page_url"):
                page = (int(pagination.get("current_page")) + 1) * 10
        return int(page)

    @staticmethod
    def is_valid_link(initial_link, link):
        return (
            link != initial_link
            and parse.urlparse(link).path
            and parse.urlparse(link).path != "/"
        )
