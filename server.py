from flask import Flask, render_template, session, redirect, url_for, request
import sqlite3
import hashlib
import os


app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.secret_key = "Le Password"

db = 'example.db'
#conn = sqlite3.connect('example.db')
#cursor = conn.cursor()

#TODO: sacar queries a otro fichero
find_users = "SELECT * FROM users WHERE user_name = ?"
get_id = "SELECT user_id FROM users WHERE user_name = ?"
register_users = "INSERT INTO users (user_name, user_pswd) VALUES (?,?)"

get_available_games = "SELECT * FROM game WHERE current_users < max_users AND private = 0 AND game_id NOT IN (SELECT game FROM game_user WHERE myuser = ?)"


get_user_games = "SELECT * FROM game WHERE game_id IN (SELECT game from game_user WHERE myuser = ?)"

new_game = "INSERT INTO game (game_name, game_desc, max_users, private) VALUES (?,?,?,?)"

add_user_to_game = "INSERT INTO game_user (myuser, game) VALUES (?,?)"

add_gm_to_gamer = "INSERT INTO game_gm (master, game) VALUES (?,?)"

current_users_plus_one = "UPDATE game SET current_users = current_users + 1 WHERE game_id = ?"

get_all_players_in_game = "SELECT player from player_games NATURAL JOIN user_player WHERE game = ?"
get_players_in_game = "SELECT player from player_games NATURAL JOIN user_player WHERE  game = ? AND myuser = ?"

@app.route('/')
def inServer():
    if 'username' not in session:
        return redirect(url_for("login"))
    dict = { "myGames" : [], "availableGames" : [], "game_desc": []}
    with sqlite3.connect(db) as conn:
        #We get the games the user is in
        for line in conn.cursor().execute(get_user_games, (session['user_id'],)):
            dict['myGames'].append(line[1:-1])
        #We get all available and public games
        for line in conn.cursor().execute(get_available_games,(session['user_id'],)):
            dict['availableGames'].append(line[:-1])
    return render_template("index.html", dict=dict)


@app.route('/get_user/<user>')
def get_user(user):
    session['shownUser'] = "users/"+user+".data"
    return redirect('/')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        with sqlite3.connect(db) as conn:
            username = request.form['user']
            hashedPwd = hashlib.sha224(request.form['pass'].encode("utf-8")).hexdigest()
            #we check the new user is not already registered
            for line in conn.cursor().execute(find_users, (username,)):
                if hashedPwd in line:
                    session['user_id'] = line[0]
                    session['username'] = str(request.form['user'])
                    session['shownUser']  = session['username']
                    return redirect('/')
            return render_template('login.html')
    if 'username' in session:
        return redirect('/')
    return render_template('login.html')

@app.route('/logout')
def logout():
    if 'username' in session:
        session.pop('username')
    if 'shownUser' in session:
        session.pop('shownUser')
    if 'user_id' in session:
        session.pop('user_id')
    return redirect('/')

@app.route('/register', methods=['POST'])
def register():
    if request.method == 'POST':
        with sqlite3.connect(db) as conn:
            username = request.form['user']
            pwd = request.form['pass']
            #we check the new user is not already registered
            for line in conn.cursor().execute(find_users, (username,)):
                #If the user exists we cant create it
                #TODO: add error page
                return redirect('/')
            #Else we create the user
            hashedPwd = hashlib.sha224(pwd.encode("utf-8")).hexdigest()
            conn.cursor().execute(register_users, (username, hashedPwd))
            conn.commit()
            session['username'] = str(request.form['user'])
            session['shownUser']  = session['username']
            return redirect('/')


# NOT TESTED
@app.route('/newGame', methods=['POST'])
def newGame():
    if request.method == 'POST':
        with sqlite3.connect(db) as conn:
            game_name= request.form['game_name']
            game_desc= request.form['game_desc']
            max_users=request.form['max_users']
            priv=request.form['private']

            #Create the game
            res=conn.cursor().execute(new_game, (game_name, game_desc, max_users, priv))

            find_game="SELECT game_id FROM game WHERE game_name= ? AND game_desc = ? AND current_users = 0"
            res=conn.cursor().execute(find_game, (game_name, game_desc))

            for line in res:
                game_id=line[0]

                #Add user to game
                conn.cursor().execute(add_user_to_game,(session['user_id'],game_id))
                conn.cursor().execute(current_users_plus_one,(game_id,))
                #Add user as GM
                conn.cursor().execute(add_gm_to_gamer,(session['user_id'], game_id))

            return redirect('/')


@app.route('/joinGame', methods=['POST'])
def joinGame():
    if request.method == 'POST':
        with sqlite3.connect(db) as conn:
            game_id=request.form['game_id']
            #Add user to game
            conn.cursor().execute(add_user_to_game,(session['user_id'],game_id))
            conn.cursor().execute(current_users_plus_one,(game_id,))

            return redirect('/')

@app.route('/game', methods=['POST'])
def game():
    if request.method=='POST':
        with sqlite3.connect(db) as conn:

            ans= conn.cursor().execute(get_all_players_in_game,(game_id,))
            for l in ans:
                pass



if __name__ == "__main__":
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(host="0.0.0.0", port=8080)
