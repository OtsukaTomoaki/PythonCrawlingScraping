import time
import requests

TEMPORARY_ERROR_CODES = (408, 500, 502, 503, 504) #一時的なエラー

def main():
    """
    メイン関数
    """
    response = fetch('http://httpbin.org/status/200,404,503')
    if 200 <= response.status_code < 300:
        print('success!')
    else:
        print('error!')

def fetch(url: str) -> requests.Response:
    """
    指定したURLにリクエストを送り、Responseオブジェクトを返す
    一時的なエラーが起きた場合には最大３回リトライする
    ３回リトライしても成功しなかった場合は例外を発生させる
    """
    max_retries = 3 #最大で３回リトライする
    retries = 0 #現在のリトライ回数

    while True:
        try:
            print(f'Retrieving {url}...')
            response = requests.get(url)
            print(f'status: {response.status_code}')
            if response.status_code not in TEMPORARY_ERROR_CODES:
                return response #一時的なエラーでなければresponseを返して終了
        except requests.exceptions.RequestException as ex:
            #ネットワークレベルのエラーの場合はログを出力してリトライする
            print(f'Netwok-level exception eccured: {ex}')

        #リトライ処理
        retries += 1
        if retries >= max_retries:
            raise Exception('Too many retries.')

        wait = 2**(retries - 1) #指数関数的なリトライ間隔を求める
        print(f'Waiting {wait} seconds...')
        time.sleep(wait)

if __name__ == '__main__':
    main()