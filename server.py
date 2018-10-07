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
get_games = "SELECT * FROM game"
get_user_games = "SELECT game from game_user WHERE myuser = ?"

@app.route('/')
def inServer():
    if 'username' not in session:
        return redirect(url_for("login"))
    dict = { "myGames" : [], "allGames" : [], "game_desc": []}
    myGames = []
    with sqlite3.connect(db) as conn:
        id = conn.cursor().execute(get_id, (session['username'],)).fetchone()[0]
        #We get the games the user is in
        for line in conn.cursor().execute(get_user_games, (id,)):
            myGames.append(line[0])
        #We get all games
        for line in conn.cursor().execute(get_games):
            #if its one of ours we flag it
            if line[0] in myGames: #FIXME: Possible error, we depend on the db schema not changing
                dict['myGames'].append(line[1])
            #if its not we add it to the other list
            #IDEA: public and private games
            else:
                dict['allGames'].append((line[1], line[2]))
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

if __name__ == "__main__":
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(host="0.0.0.0", port=8080)
