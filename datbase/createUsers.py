import sqlite3

conn = sqlite3.connect('example.db')

query = "CREATE TABLE users (" \
        "user_id integer PRIMARY KEY AUTOINCREMENT,"\
        "user_name varchar(50) NOT NULL," \
        "user_pswd varchar(50) NOT NULL);"

c = conn.cursor()
c.execute(query)
conn.commit()
conn.close()
