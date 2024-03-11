from web_poet import ApplyRule
from .page_objects import *


_SCRAPY_POET_OVERRIDES = [
    ApplyRule("amazon.com", use=AmazonProductPage, instead_of=ProductPage),
]
