import MySQLdb

#MySQLサーバーに接続し、コネクションを取得する
conn = MySQLdb.connect(db='scraping', user='scraper', password='password', charset='utf8mb4')

c = conn.cursor()
c.execute('DROP TABLE IF EXISTS `cities`')
c.execute("""
    CREATE TABLE `cities` (
        `rank` integer,
        `city` text,
        `population` integer
    )
""")

c.execute('INSERT INTO `cities` VALUES (%s, %s, %s)', (1, 'Foo', 23400))

#パラメータが辞書の場合
c.execute('INSERT INTO `cities` VALUES (%(rank)s, %(city)s, %(population)s)',
    {'rank': 2, 'city': 'Bar', 'population': 75640})

#executemany()メソッドでは、複数のパラメータをリストで指定
c.executemany('INSERT INTO `cities` VALUES (%(rank)s, %(city)s, %(population)s)', [
    {'rank': 3, 'city': 'Buz', 'population': 83000},
    {'rank': 4, 'city': 'Hoge', 'population': 120},
    {'rank': 5, 'city': 'Fuga', 'population': 979000}
    ])

conn.commit()
c.execute('SELECT * FROM `cities`')

for row in c.fetchall():
    print(row)

conn.close()