import sqlite3
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
    INITIAL_BALANCE = 1000

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

        if not self.__table_exists__('Products'):
            self.db_connection.execute('''
                CREATE TABLE IF NOT EXISTS "Products" (
                    "id"            INTEGER NOT NULL,
                    "title"         TEXT NOT NULL UNIQUE,
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
        if not self.__table_exists__('Users'):
            self.db_connection.execute('''
                CREATE TABLE IF NOT EXISTS "Users" (
                    "id"            INTEGER NOT NULL,
                    "username"      TEXT NOT NULL UNIQUE,
                    "email"         TEXT NOT NULL UNIQUE,
                    "age"           INTEGER NOT NULL,
                    "balance"       INTEGER NOT NULL,
                    PRIMARY KEY ("id" AUTOINCREMENT)
                )
            ''')

        self.db_connection.commit()

    def __del__(self):
        if self.db_connection is None:
            return

        self.db_connection.close()
        self.db_connection = None

    def add_user(self, username, email, age):
        if self.db_connection is None:
            return

        try:
            result = self.db_connection.execute('''
                INSERT INTO Users (username, email, age, balance)
                    VALUES (?, ?, ?, ?)
            ''', (username, email, age, self.INITIAL_BALANCE))

            self.db_connection.commit()
        except sqlite3.Error:
            return -1

        return 1

    def is_included(self, username=None, email=None):
        if self.db_connection is None:
            return

        if username is not None:
            return self.db_connection.execute('''
                SELECT COUNT(*) FROM Users
                    WHERE username = ?
            ''', (username,)).fetchone()[0] > 0

        if email is not None:
            return self.db_connection.execute('''
                SELECT COUNT(*) FROM Users
                    WHERE email = ?
            ''', (email,)).fetchone()[0] > 0

    def get_all_products(self):
        return (
            dict(zip(('title', 'description', 'price', 'image'), product))
            for product in self.db_connection.execute('''
                    SELECT title, description, price, image
                        FROM Products
                            ORDER BY price
                ''').fetchall()
        )
