from flask import Flask, render_template, session, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy

import os
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.secret_key = "Le Password"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))


    def __repr__(self):
        return '<User %r>' % self.username

#Conexion a la db

@app.route('/')
def inServer():
    if 'username' not in session:
        return redirect(url_for("login"))

    usersFiles = [f for f in os.listdir('users/') if os.path.isfile(os.path.join('users/', f))]
    players= [uf.split('.')[0] for uf in usersFiles]

    '''
    users=[]
    for uf in userFiles:
        u,f=uf.split('.')
    users.append(u)
    '''
    dicc = {}
    with open(session['shownUser'], 'r') as userFile:
        data = userFile.readlines()[1:]
        for stat in data:
            values = stat.strip("\n").split(",")
            if values[0][0] == '_' and session['shownUser'] == session['username']:
                dicc[values[0][1:]] = values[1]
            elif values[0][0] != '_':
                dicc[values[0]] = values[1]

    return render_template("index.html", dicc=dicc, users=players)

@app.route('/get_user/<user>')
def get_user(user):
    session['shownUser'] = "users/"+user+".data"
    return redirect('/')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        try:
            with open("users/"+request.form['user'] + ".data", 'r') as userFile:
                pwd = userFile.readline().strip()
                if pwd == request.form['pass']:
                    session['username'] = "users/"+ request.form['user'] + ".data"
                    session['shownUser']  = session['username']
                    return redirect('/')
        except FileNotFoundError:
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
        username = request.form['user']
        pwd = request.form['pass']
        #we check the new user is not already registered
        if username not in [uf.split('.')[0] for uf in [f for f in os.listdir('users/') if os.path.isfile(os.path.join('users/', f))]]:
            with open("users/"+username + ".data", 'w') as userFile:
                userFile.write(pwd)
                session['username'] = "users/"+ request.form['user'] + ".data"
                session['shownUser']  = session['username']
            return redirect('/')
        else: #TODO: mensaje de error
            return redirect('/')


if __name__ == "__main__":
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(host="0.0.0.0", port=8080)
