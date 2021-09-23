import lxml.html

#HTMLファイルを読み込み。getroot()メソッドでHtmlElementオブジェクトを得る
tree = lxml.html.parse('dp.html')
html = tree.getroot()

#引数のurlを基準として全てのa要素のhref属性を絶対urlに変換する
html.make_links_absolute('https://gihyo.jp/')

for a in html.cssselect('#listBook > li > a[itemprop="url"]'):
    #a要素のhref属性から書籍のurlを取得する
    url = a.get('href')

    #書籍のタイトルはitemprop="name"という属性を持つp要素から取得する
    p = a.cssselect('p[itemprop="name"]')[0]
    title = p.text_content() #wbr要素などが含まれるのでtextではなくtext_content()を使う

    #書籍のurlとタイトルを出力する
    print(url, title)