import requests
from tenacity import retry, stop_after_attempt, wait_exponential

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

#@retryデコーターのキーワード引数stopにリトライを終了する条件を、waitにウェイトの取り方を指定する
#stop_after_attemptは回数を条件に終了することを表し、引数に最大リトライ回数wp指定する
#wait_exponentialは指数関数的なウェイトを表し、キーワード引数multiplierに初回のウェイトを秒単位で指定する
@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1))
def fetch(url: str) -> requests.Response:
    """
    指定したURLにリクエストを送り、Responseオブジェクトを返す
    一時的なエラーが起きた場合には最大３回リトライする
    ３回リトライしても成功しなかった場合は例外を発生させる
    """

    print(f'Retrieving {url}...')
    response = requests.get(url)
    print(f'status: {response.status_code}')
    if response.status_code not in TEMPORARY_ERROR_CODES:
        return response #一時的なエラーでなければresponseを返して終了
    raise Exception(f'Temporary Error: {response.status_code}')


if __name__ == '__main__':
    main()