from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from myproject.items import Headline

class NewsCrawlSpider(CrawlSpider):
    name = 'news_crawl'
    allowd_domains = ['news.yahoo.co.jp']
    start_urls = ['https://news.yahoo.co.jp/']

    #リンクをたどるためのルールのリスト
    rules = (
        #トピックスのページのリンクをたどり、レスポンスをparse_topics()メソッドで処理する
        Rule(LinkExtractor(allow=r'/pickup/\d+$'), callback='parse_topics'),
    )

    def parse_topics(self, response):
        """
        トピックスのページからタイトルと本文を抜き出す

        Args:
            response ([type]): [description]
        """
        item = Headline()
        item['title'] = response.css('title::text').get() #タイトル
        item['body'] = response.css('article p.sc-inlrYM').xpath('string()').get()#本文
        yield item