import mechanicalsoup

browser = mechanicalsoup.StatefulBrowser() #StatefulBrowserオブジェクトを作成する
browser.open('https://www.google.co.jp/') #open()メソッドでGoogleのトップページを開く

#検索語を入力して送信する
browser.select_form('form[action="/search"]') #検索フォームを選択する
browser['q'] = 'Python' #洗濯したフォームにあるname="q"の入力ボックスに検索後を入力する
browser.submit_selected()

#検索結果のタイトルとURLを抽出して表示する
page = browser.get_current_page() #現在のページのBeautifulSoupオブジェクトを取得する

for a in page.select('a:has(h3)'): #select()でCSSセレクターにマッチする要素のリストを取得する
    print(a.text)
    print(browser.absolute_url(a.get('href')))