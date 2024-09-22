import sqlite3 as db


# DB = 'not_telegram.db'

class Storage:
    DB = ':memory:'
    INITIAL_PRODUCTS = [
        {'title': 'Улыбнись!',
         'description': 'Для бодрости духа',
         'price': 100,
         'image': 'https://img5tv.cdnvideo.ru/webp/shared/files/202112/1_1449241.jpg'
         }, {
            'title': 'Развеселись!',
            'description': 'Для смелых поступков',
            'price': 200,
            'image': 'https://posamogonu.ru/wp-content/uploads/2019/05/foto-1.png'
        }, {
            'title': 'Погуляй!',
            'description': 'Для душевной компании',
            'price': 300,
            'image': 'https://avatars.dzeninfra.ru/get-zen_doc/5253732/pub_62a256b1195e6c03d36e573b_62a36a19976862692aa54c63/scale_1200'
        }, {
            'title': 'Идиллия',
            'description': 'Комплексное решение всех накопившихся проблем',
            'price': 400,
            'image': 'https://46tv.ru/uploads/posts/2020-09/1599749657_1595606483_9-p-samogonshchiki-film-55.jpg'
        }
    ]

    def __init__(self):
        self.db_connection = None

        with db.connect(self.DB) as db_connection:
            self.db_connection = db_connection
            self.initiate_db()

    def __table_exists__(self, table_name):
        if self.db_connection is None:
            return

        return len(self.db_connection.execute('''
            SELECT *
                FROM sqlite_master
                    WHERE type='table' AND tbl_name=?
        ''', (table_name,)).fetchall())

    def initiate_db(self):
        if self.db_connection is None:
            return

        if self.__table_exists__('Products'):
            return

        self.db_connection.execute('''
            CREATE TABLE IF NOT EXISTS "Products" (
                "id"            INTEGER NOT NULL,
                "title"         TEXT NOT NULL,
                "description"   TEXT,
                "price"         INTEGER NOT NULL,
                "image"         TEXT,
                PRIMARY KEY ("id" AUTOINCREMENT)
            )
        ''')

        self.db_connection.executemany('''
            INSERT INTO Products (title, description, price, image)
                VALUES (?, ?, ?, ?)
        ''', (tuple(product[field] for field in ('title', 'description', 'price', 'image'))
              for product in self.INITIAL_PRODUCTS)
                                       )
        self.db_connection.commit()

    def __del__(self):
        if self.db_connection is None:
            return

        self.db_connection.close()

    def get_all_products(self):
        return (
            dict(zip(('title', 'description', 'price', 'image'), product))
            for product in self.db_connection.execute('''
                    SELECT title, description, price, image
                        FROM Products
                            ORDER BY price
                ''').fetchall()
        )
