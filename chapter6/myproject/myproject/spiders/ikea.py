from scrapy.spiders import SitemapSpider
import time

class IkeaSpider(SitemapSpider):
    name = 'ikea'
    allowed_domains = ['www.ikea.com']

    #この設定がないと 504 Gateway Time-out になることがある
    #settings.pyでUSER_AGENTを設定している場合、この設定は削除してよい
    custome_settings = {
        'USER_AGENT': 'ikea_bot',
    }

    #XMLサイトマップのURLのリスト
    #robots.txtのURLを指定すると、SitemapディレクティブからXMLサイトマップのURLを取得する
    sitemap_urls = [
        'https://www.ikea.com/robots.txt',
    ]

    #サイトマップインデックスからたどるサイトマップの正規表現のリスト
    #このリストの正規表現にマッチするURLのサイトマップのみをたどる
    #sitemap_followを指定しない場合は、全てのサイトマップをたどる
    sitemap_follow = [
        r'prod-ja-JP', #日本語の製品のサイトマップのみたどる
    ]

    #サイトマップに含まれるURLを処理するコールバック関数を指定するルールのリスト
    #ルールは（正規表現、正規表現にマッチするURLを処理するコールバック関数）という2要素のタプルで指定する
    #sitemap_rulesを指定しない場合はすべてのURLのコールバック関数はparseメソッドとなる
    sitemap_rules = [
        (r'/', 'parse_product'), #製品ページをparse_productで処理する
    ]

    def parse_product(self, response):
        #製品ページから製品の情報を抜き出す
        chunk_blank = response.text.split()
        for text in chunk_blank:
            if text.find('https://www.ikea.com/') == 0 and '/products/' in text:
                url_without_query = text.split('?')[0]
                print('url_without_query', url_without_query)
                if url_without_query.rfind('.jpg') != (len(url_without_query) - 4) :
                    print('not jpg', text, url_without_query.rfind('.jpg'), (len(url_without_query) - 1))
                # yield {
                #     'url': response.url,
                #     'name': response.css('#name::text').get().strip(),
                #     'type': response.css('#type::text').get().strip(),
                #     #価格は円記号と数値の間に\xa0(HTMLでは&nbsp;)が含まれているのでこれをスペースに置き換える
                #     'price': response.css('#price1::text').re_first('[\S\xa0]+').replace('\xa0', ' ')
                # }