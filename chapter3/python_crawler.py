from enum import unique
from typing import Iterator #型ヒント
import requests
import lxml.html
import time
import json
import re
from pymongo import MongoClient, collation

def main():
    """
    クローラーのメインの処理
    """
    client = MongoClient('localhost', 27017)
    collection = client.scraping.ebooks

    collection.create_index('key', unique=True)

    session = requests.Session() #複数のページをまたがるのでセッションを取得
    response = session.get('https://gihyo.jp/dp')

    urls = scrape_list_page(response)
    for url in urls:
        key = extract_key(url)#URLからkeyを取得する

        ebook = collection.find_one({ 'key': key })
        if not ebook:
            time.sleep(1)
            response = session.get(url)
            ebook = scrape_detail_page(response)#詳細ページのスクレイピング
            collection.insert_one(ebook)#電子書籍の情報をMongoDBに保存する
        ebook.pop('_id')#不要な列を削除
        print(json.dumps(ebook, indent=2, ensure_ascii=False))#電子書籍の情報を表示

def scrape_list_page(response: requests.Response) -> Iterator[str]:
    """
    一覧ページのResponseから詳細ページのURLを抜き出すジェネレータ関数
    """
    html = lxml.html.fromstring(response.text)
    html.make_links_absolute(response.url)

    for a in html.cssselect('#listBook > li > a[itemprop="url"]'):
        url = a.get('href')
        yield url

def scrape_detail_page(response: requests.Response) -> dict:
    """
    詳細ページのResponseから電子書籍の情報をdictで取得する
    """
    html = lxml.html.fromstring(response.text)
    ebook = {
        'url': response.url,
        'key': extract_key(response.url),
        'title': html.cssselect('#bookTitle')[0].text_content(),
        'price': html.cssselect('.buy')[0].text.strip(),
        'content': [normalize_spaces(h3.text_content()) for h3 in html.cssselect('#content > h3')] #目次
    }
    return ebook

def extract_key(url: str) -> str:
    """
    URLからキー（URLの末尾のISBN）を抜き出す
    """
    m = re.search(r'/([^/]+)$', url) #最後の/から文字列末尾までを正規表現で取得
    return m.group(1)

def normalize_spaces(s: str) -> str:
    """
    連続する空白を１つのスペースに置換し、前後の空白を削除した新しい文字列を取得する
    """
    return re.sub(r'\s+', ' ', s).strip()

if __name__ == '__main__':
    main()