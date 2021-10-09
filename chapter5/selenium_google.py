from selenium.webdriver import Chrome, ChromeOptions, Remote
from selenium.webdriver.common.keys import Keys

options = ChromeOptions()
#ヘッドレストモードを有効にするには、次の行のコメントアウトを解除する
options.headless = True

#googleのトップ画面を開く
with Chrome(options=options) as driver:
    driver.get('https://www.google.co.jp')

    #タイトルに'Google'が含まれていることを確認する
    assert 'Google' in driver.title

    #検索後を入力して送信する
    input_element = driver.find_element_by_name('q')
    input_element.send_keys('Python')
    input_element.send_keys(Keys.RETURN)

    assert 'Python' in driver.title

    #スクリーンショットをとる
    driver.save_screenshot('search_results.png')

    #検索結果を表示する
    for h3 in driver.find_elements_by_css_selector('a > h3'):
        a = h3.find_element_by_xpath('..') #h3の親要素を取得
        print(h3.text)
        print(a.get_attribute('href'))

    driver.quit()