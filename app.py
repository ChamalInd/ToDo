from flask import Flask, session, render_template, flash, request, redirect
from flask_session import Session
from werkzeug.security import generate_password_hash, check_password_hash

from helper import login_required

import sqlite3


# configure app
app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

# configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# configuring the database
con = sqlite3.connect('todo.db', check_same_thread=False)
cur = con.cursor()


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route('/', methods=['POST', 'GET'])
@login_required
def index():
    return render_template('index.html')


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        username = request.form.get('username')
        password = request.form.get('password')
        confirm = request.form.get('confirm')
        
        usernames = cur.execute('SELECT username FROM users').fetchall()

        # error checking
        if (not name) or (not username) or (not password) or (not confirm):
            flash('All the fields should be filled.')
            return redirect('/register')
        
        if password != confirm:
            flash('Passwords dosen\'t match.')
            return redirect('/register')
        
        if len(password) < 8:
            flash('Password should contain minium 8 characters.')
            return redirect('/register')

        if (password.isnumeric()) or (password.isalpha()):
            flash('Password should have both numbers and letters.')
            return redirect('/register')
        
        if (password.islower()) or (password.isupper()):
            flash('Password should contain both upper and lower characters.')
            return redirect('/register')

        for i in usernames:
            if i[0] == username:
                flash('Username already exits.')
                return redirect('/register')
        
        # generating hash for the password
        password_hash = generate_password_hash(password)

        cur.execute('INSERT INTO users (name, username, hash) VALUES(?, ?, ?)', (name, username, password_hash, ))
        con.commit()

        flash(f'Welcome aboard {name}!')
        session['user_id'] = username
        return redirect('/')
    return render_template('register.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    return render_template('login.html')


# forget about user
@app.route('/logout', methods=['POST', 'GET'])
def logout():
    session.clear()
    return redirect('/')