from flask import Flask, session, render_template, flash, request, redirect
from flask_session import Session
from werkzeug.security import generate_password_hash, check_password_hash
from cryptography.fernet import Fernet

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
    if request.method == 'POST':
        item = request.form.get('item')

        if item:
            # encrypting item
            f = Fernet(session['key'])
            encrypted_item = f.encrypt(item.encode())
            # adding new ongoing task
            cur.execute('INSERT INTO todoitems VALUES(?, 1, ?)', (session['user_id'], encrypted_item))
            con.commit()
        else:
            flash('Task cannot be empty.')
    
    # decrypting items
    _ = cur.execute('SELECT item from todoitems WHERE user_id=? AND category_id=1', (session['user_id'], )).fetchall()
    f = Fernet(session['key'])
    items = []
    for i in _:
        items.append(f.decrypt(i[0]).decode())
        
    return render_template('index.html', items=items)


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

        # generating key for todo item encryptions
        key = Fernet.generate_key()

        cur.execute('INSERT INTO users (name, username, hash, key) VALUES(?, ?, ?, ?)', (name, username, password_hash, key, ))
        con.commit()

        flash(f'Welcome aboard {name}!')
        session['user_id'] = cur.execute('SELECT id FROM users WHERE username=? AND name=?', (username, name)).fetchall()[0][0]
        print(session['user_id'])
        session['user_name'] = username
        session['name'] = name
        session['key'] = key
        return redirect('/')
    return render_template('register.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user_data = cur.execute('SELECT username, hash, name, id, key FROM users').fetchall()
        for i in user_data:
            if i[0] == username and check_password_hash(i[1], password):
                flash(f'Welcome back {i[2]}!')
                session['user_id'] = i[3]
                session['user_name'] = i[0]
                session['name'] = i[2]
                session['key'] = i[4]
                return redirect('/')
            
            if i[0] == username and (not check_password_hash(i[1], password)):
                flash('Incorrect password.')
                return redirect('/login')
        else:
            flash('User not registered.')

    return render_template('login.html')


# forget about user
@app.route('/logout', methods=['POST', 'GET'])
def logout():
    session.clear()
    return redirect('/')