import os
from urllib.parse import urlencode

import scrapy
import time

FLICKR_API_KEY = os.environ['FLICKR_API_KEY']

class FlickrSpider(scrapy.Spider):
    name = 'flickr'
    #Files Pipelineでダウンロードされる画像ファイルはallowed_domainsに
    #制限されないので、allowed_domainsに'staticflickr.com'を追加する必要はない
    allowed_domains = ['api.flickr.com']

    #キーワード引数でSpider引数の値を受け取る
    def __init__(self, text='oasis'):
        super().__init__() #親クラスの__init__を実行

        #環境変数とSpider引数の値を使ってstart_urlsを組み立てる
        #urlencode()関数は、引数に指定したdictのキーと値をURLエンコードして
        #key1=value1&key2=value2という形式の文字列を返す
        self.start_urls = [
            'https://api.flickr.com/services/rest/?' + urlencode({
                'method' : 'flickr.photos.search',
                'api_key' : FLICKR_API_KEY,
                'text' : text,
                'sort' : 'relevance',
                'license' : '4,5,9', #CC BY 2.0, CC BY-SA 2.0, CC0 を指定
            }),
        ]
    def parse(self, response):
        """
        APIのレスポンスをパースしてfile_urlsというキーを含むdictをyieldする

        Args:
            response ([type]): [description]
        """
        for photo in response.css('photo'):
            yield {'file_urls' : [flickr_photo_url(photo)]}

def flickr_photo_url(photo: scrapy.Spider) -> str:
    """
    Flickrの写真のURLを組み立てる
    参考：https://www.flickr.com/services/api/misc.urls.html

    Args:
        photo (scrapy.Spider): [description]
    """
    attrib = dict(photo.attrib) #photo要素の属性をdictとして取得
    attrib['size'] = 'b' #サイズの値を追加
    return 'https://farm{farm}.staticflickr.com/{server}/{id}_{secret}_{size}.jpg'.format(**attrib)
