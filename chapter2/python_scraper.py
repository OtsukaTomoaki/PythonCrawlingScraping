import csv
from typing import List #型ヒントのためにインポート

import requests
import lxml.html

def main():
    """
    メイン処理。fetch(), scrape(), save()の３つの関数を呼び出す
    """
    url = 'https://gihyo.jp/dp'
    html = fetch(url)
    books = scrape(html, url)
    save('books.csv', books)

def fetch(url: str) -> str:
    """
    引数urlで与えられたURLのwebページを取得する
    webページのエンコーディングはContent-Typeヘッダーから取得する
    戻り値: str型のhtml
    """
    r = requests.get(url)
    #HTTPヘッダーから取得したエンコーディングでデコードした文字列を渡す
    return r.text

def scrape(html: str, base_url: str) -> List[dict]:
    """
    引数htmlで与えられたHTMLから正規表現で書籍の情報を抜き出す
    引数base_urlは絶対urlに変換する際の基準となるURLを指定する。
    戻り値: 書籍(dict)のリスト
    """

    books =[]
    html = lxml.html.fromstring(html)
    #絶対URLに変換
    html.make_links_absolute(base_url)

    for a in html.cssselect('#listBook > li > a[itemprop="url"]'):
        url = a.get('href')
        #書籍のタイトルはitemprop="name"という属性を持つ要素から取得する
        p = a.cssselect('p[itemprop="name"]')[0]
        title = p.text_content()
        books.append({ 'url': url, 'title': title })
    return books

def save(file_path: str, books: List[dict]):
    """
    引数booksで与えられた書籍のリストをCSV形式のファイルに保存する
    ファイルのパスは引数file_pathで与えられる
    """

    with open(file_path, 'w', newline='') as f:
        writer = csv.DictWriter(f, ['url', 'title'])
        writer.writeheader() #1行目のヘッダーを出力する
        #writerows()で複数の行を一度に出力する。引数は辞書のリスト
        writer.writerows(books)

if __name__ == '__main__':
    main()