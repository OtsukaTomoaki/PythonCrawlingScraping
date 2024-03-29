import asyncio
import logging

import aiohttp
import feedparser
from bs4 import BeautifulSoup

async def main():
    """
    メインとなる処理のコルーチン。はてなブックマークの人気エントリーを非同期でクロールする
    """
    #人気エントリーのRSSからURLのリストを取得する
    d = feedparser.parse('https://b.hatena.ne.jp/hotentry.rss')
    urls = [entry.link for entry in d.entries]
    #同時リクエスト数を全体で５に、ホスト単位で１に制限するTCPConnectorオブジェクトを作成
    connector = aiohttp.TCPConnector(limit=5, limit_per_host=1)
    #セッションオブジェクトを作成
    async with aiohttp.ClientSession(connector=connector) as session:
        #URLのリストに対応するコルーチンのリストを作成
        coroutines = []
        for url in urls:
            coroutine = fetch_and_scrape(session, url)
            coroutines.append(coroutine)

        #コルーチンを並列実行し、完了した順に返す
        for coroutine in asyncio.as_completed(coroutines):
            print(await coroutine) #コルーチンの結果を表示する


async def fetch_and_scrape(session: aiohttp.ClientSession, url: str) -> dict:
    """
    引数で指定したURLのページを取得してURLとタイトルを含むdictを返すコルーチン

    Args:
        session (aiohttp.ClientSession): [description]
        url (str): [description]

    Returns:
        dict: [description]
    """
    logging.info(f'Requests queued {url}')
    #非同期にリクエストを送り、レスポンスヘッダを取得する
    async with session.get(url) as response:
        #レスポンスボディを非同期に取得してパースする
        soup = BeautifulSoup(await response.read(), 'lxml')
        return {
            'url' : url,
            'title' : soup
        }

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
