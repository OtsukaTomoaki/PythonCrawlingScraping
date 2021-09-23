import csv

#newline=''として改行コードの自動変換を抑制する
with open('top_cities.csv', 'w', newline='') as f:
    writer = csv.writer(f)#ファイルオブジェクトを引数に指定し、csv.writerオブジェクトを生成
    writer.writerow(['rank', 'city', 'population'])#header
    writer.writerows([
        [1, 'Foo', 200000],
        [2, 'Bar', 30000],
        [3, 'Baz', 100000]
    ])