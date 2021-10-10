import logging
from typing import List #型ヒントのため

from selenium.webdriver import Chrome, ChromeOptions, Remote
from selenium.common.exceptions import NoSuchElementException

def main():
    """
    メイン関数
    """
    options = ChromeOptions()
    #options.headless = True

    driver = Chrome(options=options)

    navigate(driver) #noteのトップページに遷移する
    contents = scrape_contents(driver) #コンテンツのリストを取得する
    logging.info(f'Found {len(contents)} contents.')

    #コンテンツの情報を表示する
    for content in contents:
        print(content)


def navigate(driver: Remote):
    """
    目的のページに遷移する
    Args:
        driver (Remote): [description]
    """
    logging.info('Navigating...')
    driver.get('https://note.mu/')#noteのトップページを開く
    assert 'note' in driver.title #タイトルに'note'が含まれていることを確認する

def scrape_contents(driver: Remote) -> List[dict]:

    contents = []#取得したコンテンツを格納するリスト

    #コンテンツを表すdiv要素について反復する
    for div in driver.find_elements_by_css_selector('.m-largeNoteWrapper__card'):
        a = div.find_element_by_css_selector('a')
        like = div.find_element_by_css_selector('.m-noteBody__statusLike .m-noteBody__statusLabel').text

        try:
            description = div.find_element_by_css_selector('p').text
        except NoSuchElementException:
            description = '' #画像コンテンツなどのp要素がない場合はから文字にする

        #url、タイトル、概要、スキの数を取得して、dictとしてリストに追加する
        contents.append({
            'url': a.get_attribute('href'),
            'title': div.find_element_by_css_selector('h3').text,
            'description': description,
            'like': int(like)
        })
    return contents

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO) #INFOレベル以上のログを出力する
    main()