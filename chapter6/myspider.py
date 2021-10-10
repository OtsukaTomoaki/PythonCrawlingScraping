import scrapy

class BlogSpider(scrapy.Spider):
    name = 'blogspider'#spiderの名前
    start_urls = ['https://www.zyte.com/blog/']#クロールを開始するURLのリスト

    def parse(self, response, **kwargs):
        """
        ページから投稿タイトルを全て抜き出し、次のページへのリンクがあればたどる

        Args:
            response ([type]): [description]
        """
        #ページから投稿のタイトルを全て抜き出す
        for title in response.css('.oxy-post-title'):
            yield {'title': title.css('::text').get()}

        #次のページ(OLDER POST)へのリンクがあればたどる
        for next_page in response.css('a.next'):
            yield response.follow(next_page, self.parse)