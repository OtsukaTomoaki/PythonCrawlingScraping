import sqlite3

conn = sqlite3.connect('top_cities.db')

c = conn.cursor() #カーソルを取得する
c.execute('DROP TABLE IF EXISTS cities')
#citiesテーブルを作成する
c.execute("""
    CREATE TABLE cities (
        rank integer,
        city text,
        population integer
    )
""")

#execute()メソッドの第二引数にはSQL文のパラメータのリストを指定できる
#パラメータで置き換えるプレースホルダーには?で指定する
c.execute('INSERT INTO cities VALUES (?, ?, ?)', (1, 'Foo', 4000))

#パラメーターが辞書の場合、プレースホルダーは :キー名 で指定する
c.execute('INSERT INTO cities VALUES (:rank, :city, :population)', { 'rank': 2, 'city': 'Bar', 'population': 70000 })

#executemany()メソッドでは複数のパラメータをリストで指定できる
c.executemany('INSERT INTO cities VALUES (:rank, :city, :population)', [
    { 'rank': 3, 'city': 'Buz', 'population': 30000 },
    { 'rank': 4, 'city': 'Hoge', 'population': 100 },
    { 'rank': 5, 'city': 'Fuga', 'population': 67000 },
    { 'rank': 6, 'city': 'Piyo', 'population': 900 },
])

conn.commit()#変更をコミットする

c.execute('SELECT * FROM cities')
for row in c.fetchall(): #クエリの結果はfetchall()メソッドで取得できる
    print(row)

conn.close()#コネクションを閉じる
