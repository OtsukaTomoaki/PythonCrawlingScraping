import logging
from typing import List #型ヒントのため
import time
import os
from io import BytesIO
import requests

from selenium.webdriver import Chrome, ChromeOptions, Remote
from selenium.common.exceptions import NoSuchElementException

LINE_ACCESS_TOKEN = os.environ['LINE_ACCESS_TOKEN']

def main():
    """
    メイン関数
    """
    options = ChromeOptions()
    #options.headless = True

    driver = Chrome(options=options)
    try:
        navigate(driver) #noteのトップページに遷移する
        contents = scrape_contents(driver) #コンテンツのリストを取得する
        logging.info(f'Found {len(contents)} contents.')

        contents.sort(key= lambda content: content['like'], reverse=True)
        contents = contents[0:5]
        #コンテンツの情報を表示する
        for content in contents:
            print(content)
        notify_line(contents)
    finally:
        driver.quit()


def navigate(driver: Remote):
    """
    目的のページに遷移する
    Args:
        driver (Remote): [description]
    """
    logging.info('Navigating...')
    driver.get('https://note.mu/')#noteのトップページを開く
    assert 'note' in driver.title #タイトルに'note'が含まれていることを確認する

    for _ in range(3):
        driver.execute_script('scroll(0, document.body.scrollHeight)')
        logging.info('Waiting for contents to be loaded...')
        time.sleep(2)

def scrape_contents(driver: Remote) -> List[dict]:

    contents = []#取得したコンテンツを格納するリスト

    #コンテンツを表すdiv要素について反復する
    for div in driver.find_elements_by_css_selector('.m-largeNoteWrapper__card'):
        a = div.find_element_by_css_selector('a')
        like = div.find_element_by_css_selector('.m-noteBody__statusLike .m-noteBody__statusLabel').text
        like = int(like) if like.isdecimal() else 0
        try:
            description = div.find_element_by_css_selector('p').text
        except NoSuchElementException:
            description = '' #画像コンテンツなどのp要素がない場合はから文字にする

        try:
            image_src = div.find_element_by_css_selector('img').get_attribute('src')
        except NoSuchElementException:
            image_src = '' #画像コンテンツなどのp要素がない場合はから文字にする

        #url、タイトル、概要、スキの数を取得して、dictとしてリストに追加する
        contents.append({
            'url': a.get_attribute('href'),
            'title': div.find_element_by_css_selector('h3').text,
            'description': description,
            'like': like,
            'image_src': image_src
        })
    return contents

def notify_line(contents: List[dict]):
    for content in contents:
        url = 'https://notify-api.line.me/api/notify'
        headers = {
            'Contents-Type': 'application/x-www-form-urlencoded',
            'Authorization': f'Bearer {LINE_ACCESS_TOKEN}'
        }
        body = {
            'message' : f"""
            {content['title']}
            {content['url']}
            """,
            'notificationDisabled' : False
        }
        image_src = content['image_src']
        if image_src.find('https://') == 0:
            #うまいことLINE上で表示されない（要調査。一旦ローカルに保存しないとだめ？）
            print(image_src)
            response = requests.get(image_src)
            body['imageFile'] = BytesIO(response.content)
            time.sleep(2)
        response = requests.post(url, headers=headers, data=body)
        print(response.status_code, response.text)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO) #INFOレベル以上のログを出力する
    main()