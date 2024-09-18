import os
import sqlite3 as db

DB_FILE = 'not_telegram.db'

if not os.path.exists(DB_FILE):
    try:
        open(DB_FILE, "w")
    except OSError:
        exit(1)

db_connection = db.connect(DB_FILE)

db_connection.execute('''
CREATE TABLE IF NOT EXISTS "Users"(
	"id"	INTEGER NOT NULL,
	"username"	TEXT NOT NULL,
	"email"	TEXT NOT NULL COLLATE NOCASE,
	"age"	INTEGER,
	"balance"	INTEGER NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
)
''')


db_connection.executemany('''
    INSERT INTO Users (username, email, age, balance)
        VALUES (CONCAT('User', ?), CONCAT('example', ?, '@gmail.com'), ? * 10, 1000
    )
''', ((i, i, i) for i in range(1, 11))
)

db_connection.execute('''
    UPDATE Users SET balance = 500
        WHERE MOD(SUBSTR(username, 5), 2) <> 0
''')

db_connection.execute('''
    DELETE FROM Users
        WHERE MOD(SUBSTR(username, 5) - 1, 3) = 0
''')

db_connection.commit()

db_cursor = db_connection.execute('''
    SELECT username, email, age, balance
        FROM Users
            WHERE age <> 60
''')

for db_row in db_cursor.fetchall():
    print(f'Имя: {db_row[0]} | Почта: {db_row[1]} | Возраст: {db_row[2]} | Баланс: {db_row[3]}')

db_connection.close()
