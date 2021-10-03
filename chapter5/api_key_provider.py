def read() -> str:
    with open('./google_api_key.txt', 'r') as reader:
        api_key = reader.read()
        return api_key.strip()#空白および改行を削除

if __name__ == '__main__':
    api_key = read()
    print(api_key)