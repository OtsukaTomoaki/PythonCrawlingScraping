# coding: utf-8
import os
from googleapiclient.discovery import build #pip install google-api-python-client
import api_key_provider

YOUTUBE_API_KEY = os.environ['YOUTUBE_API_KEY']
#YOUTUBE_API_KEY = api_key_provider.read()
print(YOUTUBE_API_KEY)

#YoutubeのAPIクライアントを組み立てる。build()関数の第一引数にはAPI名を
#第二引数にはAPIのバージョンを指定し、キーワード引数developerKeyでx APIキーを指定する
#この関数は内部的にhttps://www.googleapis.com/discovery/v1/apis/youtube/v3/rest という
#URLにアクセスし、APIのリソースやメソッドの情報を取得する
youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY, cache_discovery=False)
print(youtube)
#キーワード引数で引数を指定し、search.listメソッドを呼び出す
#list()メソッドでgoogleapisclient.http.HttpRequestオブジェクトが得られ、
#execute()メソッドを実行すると実際にHTTPリクエストが送られてAPIのレスポンスが得られる
search_response = youtube.search().list(
    part='snippet',
    q='oasis',
    type='video'
).execute()
print(search_response)
#search_responseはAPIのレスポンスのJSONをパースしたdict
for item in search_response['items']:
    print(item['snippet']['title']) #動画のタイトルを表示する