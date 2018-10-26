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
	   "game_desc text NOT NULL,"\
	   "max_users integer NOT NULL,"\
	   "current_users integer NOT NULL DEFAULT 0,"\
	   "private integer NOT NULL);"


query3 = "CREATE TABLE game_user (" \
    "game integer NOT NULL," \
    "myuser integer NOT NULL," \
    "FOREIGN KEY (game) REFERENCES game (game_id)" \
        "ON UPDATE CASCADE ON DELETE NO ACTION," \
    "FOREIGN KEY (myuser) REFERENCES users (user_id)" \
        "ON UPDATE CASCADE ON DELETE NO ACTION," \
    "CONSTRAINT game_users_pkey PRIMARY KEY (game, myuser));"

query4 = "CREATE TABLE game_gm ("\
	"master integer NOT NULL,"\
	"game integer NOT NULL,"\
	"FOREIGN KEY (master) REFERENCES users (user_id)"\
	"	ON UPDATE CASCADE ON DELETE NO ACTION,"\
	"FOREIGN KEY (game) REFERENCES game (game_id)"\
	"	ON UPDATE CASCADE ON DELETE NO ACTION,"\
	"CONSTRAINT game_gm_pkey PRIMARY KEY (game, master));"

query5 = "CREATE TABLE player ("\
	"player_id integer PRIMARY KEY autoincrement,"\
	"player_name varchar(50) NOT NULL,"\
	"player_st integer NOT NULL DEFAULT 10,"\
	"player_dx integer NOT NULL DEFAULT 10,"\
	"player_iq integer NOT NULL DEFAULT 10,"\
	"player_ht integer NOT NULL DEFAULT 10,"\
	"player_hp_max integer NOT NULL DEFAULT 10,"\
	"player_hp_current integer NOT NULL DEFAULT 10,"\
	"player_will integer NOT NULL DEFAULT 10,"\
	"player_per integer NOT NULL DEFAULT 10,"\
	"player_fp_max integer NOT NULL DEFAULT 10,"\
	"player_fp_current integer NOT NULL DEFAULT 10);"

query6 = "CREATE TABLE user_player ("\
	"myuser integer NOT NULL,"\
	"player integer NOT NULL,"\
	"FOREIGN KEY (myuser) REFERENCES users (user_id)"\
	"	ON UPDATE CASCADE ON DELETE NO ACTION,"\
	"FOREIGN KEY (player) REFERENCES player (player_id)"\
	"	ON UPDATE CASCADE ON DELETE NO ACTION,"\
	"CONSTRAINT user_player_pkey PRIMARY KEY (myuser, player));"

query7 = "CREATE TABLE player_gamer ("\
	"player integer NOT NULL,"\
	"game integer NOT NULL,"\
	"FOREIGN KEY (player) REFERENCES player (player_id)"\
	"	ON UPDATE CASCADE ON DELETE NO ACTION,"\
	"FOREIGN KEY (game) REFERENCES game (game_id)"\
	"	ON UPDATE CASCADE ON DELETE NO ACTION,"\
	"CONSTRAINT player_game_pkey PRIMARY KEY (player, game));"


c.execute(query1)
c.execute(query2)
c.execute(query3)
c.execute(query4)
c.execute(query5)
c.execute(query6)
c.execute(query7)

conn.commit()
conn.close()
