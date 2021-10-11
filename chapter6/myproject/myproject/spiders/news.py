import scrapy


class NewsSpider(scrapy.Spider):
    name = 'news'#Spiderの名前
    allowed_domains = ['news.yahoo.co.jp']#クロール対象とするドメインのリスト
    start_urls = ['https://news.yahoo.co.jp/']#クロールを開始するURLのリスト

    def parse(self, response):
        """
        トップページのトピックス一覧からここのトピックスへのリンクを抜き出して表示する

        Args:
            response ([type]): [description]
        """
        urls = response.css('ul li a::attr("href")')
        print('urls', urls)

        for url in urls.re(r'/pickup/\d+$'):
            yield response.follow(url, self.parse_topics)

    def parse_topics(self, response):
        pass
