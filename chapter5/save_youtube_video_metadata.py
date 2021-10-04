import os
import logging
from typing import Collection, Iterator, List

from googleapiclient.discovery import build
from pymongo import DESCENDING, MongoClient, ReplaceOne


YOUTUBE_API_KEY = os.environ['YOUTUBE_API_KEY']#環境変数からAPIキーを取得する
logging.getLogger('googleapiclient.discovery_cache').setLevel(logging.DEBUG) #不要なログを出力しないように設定する

def main():
    """
    メインの処理
    """
    mongo_client = MongoClient('localhost', 27017) #MongoDBのクライアントオブジェクトを取得する
    collection = mongo_client.youtube.videos #youtubeデータベースのvideosコレクションを取得する

    #動画を検索し、ページ単位でアイテムのリストを保存する
    for item_per_page in search_videos('oasis'):
        save_to_mongodb(collection, item_per_page)

    show_top_videos(collection) #閲覧数の多い動画を表示する

def search_videos(query: str, max_pages: int=5) -> Iterator[List[dict]]:
    '''
    引数queryで動画を検索して、ページ単位でアイテムのリストをyieldする
    最大max_pagesページまでを検索する
    '''
    youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY, cache_discovery=False)

    #search.listメソッドで最初のページを取得するためのリクエストを取得
    search_request = youtube.search().list(
        part = 'id', #search.listでは動画IDだけを取得できれば良い
        q = query,
        type = 'video',
        maxResults = 50 #1ページあたり最大50件の動画を取得する
    )

    #リクエストが有効、かつページ数がmax_pages以内の間、繰り返す
    #ページ数を制限しているのは実行時間が長くなりすぎないようにするため
    i = 0
    while search_request and i < max_pages:
        search_response = search_request.execute() #リクエストを送る
        video_ids = [item['id']['videoId'] for item in search_response['items']] #動画IDのリストを得る

        #video.listメソッドで動画の詳細な情報を得る
        videos_response = youtube.videos().list(
            part = 'snippet,statistics',
            id = ','.join(video_ids)
        ).execute()

        yield videos_response['items'] #現在のページに対応するアイテムのリストをyieldする

        #list_next()メソッドで次のページを取得するためのリクエスト（次のページがない場合はNone）を得る
        search_request = youtube.search().list_next(search_request, search_response)
        i += 1

def save_to_mongodb(collection: Collection, items: List[dict]):
    '''
    MongoDBのコレクションにアイテムのリストを保存する
    '''
    #MongoDBに保存する前に、後で使いやすいようにアイテムを置き換える
    for item in items:
        item['_id'] = item['id'] #各アイテムのid属性をMongoDBの_id属性として使う

        #statisticsに含まれるviewCountプロパティなどの値が文字列になっているので数値に変換する
        for key, value in item['statistics'].items():
            item['statistics'][key] = int(value)

    #単純にcollection.insert_many()を使うと_idが重複した場合にエラーになる
    #代わりにcollection.bulk_write()で複数のupsert(insert or update)をまとめて行う
    operations = [ReplaceOne({'_id': item['_id']}, item, upsert=True) for item in items]
    result = collection.bulk_write(operations)
    logging.info(f'Upserted {result.upserted_count} documents.')

def show_top_videos(collection: Collection):
    '''
    MongoDBのコレクション内でビュー数の上位5件を表示する
    '''
    for item in collection.find().sort('statistics.viewCount', DESCENDING).limit(5):
        print(item['statistics']['viewCount'], item['snippet']['title'])

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO) #INFOレベル以上のログを出力する
    main()