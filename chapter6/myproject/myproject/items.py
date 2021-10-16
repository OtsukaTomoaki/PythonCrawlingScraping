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

class Page(scrapy.Item):
    """
    Webページ

    Args:
        scrapy ([type]): [description]
    """

    url = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()

    def __repr__(self):
        """
        ログへの出力時に長くなりすぎないように、contentを省略する

        Returns:
            [type]: [description]
        """
        p = Page(self) #このPageを複製したPageを得る
        if len(p['content']) > 100:
            p['content'] = p['content'][:100] + '...'#100文字よりも長い場合は省略する

        return super(Page, p).__repr__() #複製したPageの文字列表現を返す