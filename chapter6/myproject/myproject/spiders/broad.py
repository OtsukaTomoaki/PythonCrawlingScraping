import scrapy

from myproject.items import Page
from myproject.utils import get_content

class BroadSpider(scrapy.Spider):
    name = 'broad'
    #はてなブックマークの新着エントリーページ
    start_urls = ['http://b.hatena.ne.jp/entrylist/all']

    def parse(self, resoponse):
        """
        はてなブックマークの新着エントリーページをパースする

        Args:
            resoponse ([type]): [description]
        """
        #個別のWebページへのリンクをたどる
        for url in resoponse.css('.entrylist-contents-title > a::attr("href")').getall():
            #parse_page()メソッドをコールバック関数として指定する
            yield scrapy.Request(url, callback=self.parse_page)

    def parse_page(self, response):
        """
        個別のwebページをパースする

        Args:
            response ([type]): [description]
        """
        #utils.pyに定義したget_content()関数でタイトルと本文を抽出する
        title, content = get_content(response.text)
        #Pageオブジェクトを作成してyieldする
        yield Page(url=response.url, title=title, content=content)