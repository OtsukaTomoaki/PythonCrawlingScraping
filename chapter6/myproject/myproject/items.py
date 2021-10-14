# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Headline(scrapy.Item):
    """
    ニュースのヘッドラインを表すItem

    Args:
        scrapy ([type]): [description]
    """
    title = scrapy.Field()
    body = scrapy.Field()

class Restaurant(scrapy.Item):
    """
    食べログのレストラン情報

    Args:
        scrapy ([type]): [description]
    """
    name = scrapy.Field()
    address = scrapy.Field()
    latitude = scrapy.Field()
    logitude = scrapy.Field()
    station = scrapy.Field()
    score = scrapy.Field()
