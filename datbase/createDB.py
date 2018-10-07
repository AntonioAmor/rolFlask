import sqlite3

conn = sqlite3.connect('example.db')
c = conn.cursor()

query1 = "CREATE TABLE users (" \
        "user_id integer PRIMARY KEY autoincrement,"\
        "user_name varchar(50) NOT NULL," \
        "user_pswd varchar(50) NOT NULL);"

query2 = "CREATE TABLE game ("\
	   "game_id integer PRIMARY KEY autoincrement,"\
	   "game_name varchar(50) NOT NULL,"\
	   "game_desc text NOT NULL);"

query3 = "CREATE TABLE game_user (" \
    "myuser integer NOT NULL," \
    "game integer NOT NULL," \
    "FOREIGN KEY (myuser) REFERENCES users (user_id)" \
        "ON UPDATE CASCADE ON DELETE NO ACTION," \
    "FOREIGN KEY (game) REFERENCES game (game_id)" \
        "ON UPDATE CASCADE ON DELETE NO ACTION," \
    "CONSTRAINT game_users_pkey PRIMARY KEY (game, myuser));"

c.execute(query1)
c.execute(query2)
c.execute(query3)


conn.commit()
conn.close()