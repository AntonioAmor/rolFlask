import sqlite3
import hashlib


conn = sqlite3.connect('example.db')
c = conn.cursor()

#hashedPwd = hashlib.sha224('gamer'.encode("utf-8")).hexdigest()
#c.execute("INSERT INTO users (user_name, user_pswd) VALUES ('alpha',hashedPwd)")
c.execute("INSERT INTO game (game_name, game_desc,max_users,current_users, private) VALUES ('prueba', 'esto es una prueba',2,0,0)")
c.execute("INSERT INTO game_user (myuser, game) VALUES (1, 1)")
c.execute("UPDATE game SET current_users = current_users + 1 WHERE game_id=1")
#segunda partida, no esta el user_id 1 y es publica
c.execute("INSERT INTO game (game_name, game_desc, max_users, current_users, private) VALUES ('prueba2', 'esta partida es publica',5,0,0)")
c.execute("INSERT INTO game (game_name, game_desc, max_users, current_users, private) VALUES ('prueba2.5', 'esta partida es publica',5,0,0)")
c.execute("INSERT INTO game (game_name, game_desc, max_users, current_users, private) VALUES ('prueba2.9', 'esta partida es publica',5,0,0)")

#tercera partida, no esta el user_id 1 y es privada
c.execute("INSERT INTO game (game_name, game_desc, max_users, current_users, private) VALUES ('prueba3', 'esta partida es privada',3,0,1)")

#cuarta partida, no esta el user_id 1 y es publica pero esta llena
c.execute("INSERT INTO game (game_name, game_desc, max_users, current_users, private) VALUES ('prueba4', 'esta partida es publixa',3,3,1)")


conn.commit()
conn.close()
