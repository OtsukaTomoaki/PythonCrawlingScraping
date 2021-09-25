import lxml.html
from pymongo import MongoClient, collection

client = MongoClient('localhost', 27017)
db = client.scraping #scrapingデータベースを取得する
collection = db.books #booksコレクションを取得する

#このスクリプトを何回実行しても同じ結果になるようにするため、コレクションのドキュメントを全て削除する
collection.delete_many({})

#HTMLファイルを読み込み。getroot()メソッドでHtmlElementオブジェクトを得る
tree = lxml.html.parse('../dp.html')
html = tree.getroot()

#引数のurlを基準として全てのa要素のhref属性を絶対urlに変換する
html.make_links_absolute('https://gihyo.jp/')

for a in html.cssselect('#listBook > li > a[itemprop="url"]'):
    #a要素のhref属性から書籍のurlを取得する
    url = a.get('href')

    #書籍のタイトルはitemprop="name"という属性を持つp要素から取得する
    p = a.cssselect('p[itemprop="name"]')[0]
    title = p.text_content() #wbr要素などが含まれるのでtextではなくtext_content()を使う

    #書籍のurlとタイトルをMongoDBに保存する
    collection.insert_one({ 'url': url, 'title': title })

#コレクションの全てのドキュメントを_idの順にソートして取得する
for link in collection.find().sort('_id'):
    print(link['_id'], link['url'], link['title'])