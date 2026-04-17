from flask import Flask, session, render_template, flash, request, redirect
from flask_session import Session
from werkzeug.security import generate_password_hash, check_password_hash
from cryptography.fernet import Fernet

from helper import login_required, is_good_password

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
    # adding new items action
    if request.method == 'POST' and request.form.get('action') == 'add-new':
        item = request.form.get('item')

        if item:
            # encrypting item
            f = Fernet(session['key'])
            encrypted_item = f.encrypt(item.encode())
            # adding new ongoing task
            cur.execute('INSERT INTO todoitems(user_id, category_id, item) VALUES(?, 1, ?)', (session['user_id'], encrypted_item))
            con.commit()
        else:
            flash('Task cannot be empty.')
    
    # complete tasks action
    if request.method == 'POST':
        task = request.form.get('task-ongoing')

        if task:
            cur.execute('UPDATE todoitems SET category_id=2 WHERE id=?', (task, ))
            con.commit()
    
    # remove completed tasks action
    if request.method == 'POST' and request.form.get('action') == 'delete':
        task = request.form.get('task-completed')

        if task:
            cur.execute('DELETE FROM todoitems WHERE id=?', (task, ))
            con.commit()
    
    # decrypting items
    _ = cur.execute('SELECT item, id, category_id FROM todoitems WHERE user_id=?', (session['user_id'], )).fetchall()
    f = Fernet(session['key'])
    ongoing = []
    completed = []
    for i in _:
        task = f.decrypt(i[0]).decode()
        if i[2] == 1:
            ongoing.append([task, i[1]])
        else:
            completed.append([task, i[1]])

    # checking user progress 
    done = cur.execute('SELECT COUNT(*) FROM todoitems WHERE user_id=? AND category_id=2', (session['user_id'], )).fetchall()[0][0]
    total = cur.execute('SELECT COUNT(*) FROM todoitems WHERE user_id=?', (session['user_id'], )).fetchall()[0][0]

    if total > 0:
        progress = done / total * 100
    else:
        progress = 0

    return render_template('index.html', ongoing=ongoing, completed=completed, progress=progress)


@app.route('/profile', methods=['POST', 'GET'])
@login_required
def profile():
    if request.method == 'POST':
        # change name action 
        if request.form.get('action') == 'change-name':
            new_name = request.form.get('name')

            if new_name:
                if new_name == session['name']:
                    flash('New name cannot be same as the old name.')
                    return redirect('/profile')
                if new_name == session['user_name']:
                    flash('Name cannot be same as the username.')
                    return redirect('/profile')
                
                session['name'] = new_name
                flash('Successfully updated the name.')
                cur.execute('UPDATE users SET name=? WHERE id=?', (new_name, session['user_id'], ))
                con.commit()
                return redirect('/profile')
            
            else:
                flash('Name cannot be empty.')
                return redirect('/profile')
        
        # change password 
        if request.form.get('action') == 'change-password':
            current_pass = request.form.get('current-password')
            new_pass = request.form.get('new-password')
            confirm_pass = request.form.get('confirm-password')

            if current_pass and new_pass and confirm_pass:
                pass_hash = cur.execute('SELECT hash FROM users WHERE id=?', (session['user_id'], )).fetchall()[0][0]

                if not check_password_hash(pass_hash, current_pass):
                    flash('Current password is incorrect.')
                    return redirect('/profile')
                
                if current_pass == new_pass:
                    flash('New password cannot be the current password')
                    return redirect('/profile')
                
                if not is_good_password(new_pass, confirm_pass, session['user_name'])[0]:
                    flash(is_good_password(new_pass, confirm_pass, session['user_name'])[1])
                    return redirect('/profile')
                
                flash('Successfully updated the password.')
                cur.execute('UPDATE users SET hash=? WHERE id=?', (generate_password_hash(new_pass), session['user_id'], ))
                con.commit()
                return redirect('/profile')
                
            else:
                flash('Passwords fields cannot be empty.')
                return redirect('/profile')
        
        # delete user profile 
        if request.form.get('action') == 'delete-user':
            cur.execute('DELETE FROM users WHERE id=?', (session['user_id'], ))
            con.commit()
            session.clear()
            return redirect('/')

    # checking user progress 
    done = cur.execute('SELECT COUNT(*) FROM todoitems WHERE user_id=? AND category_id=2', (session['user_id'], )).fetchall()[0][0]
    total = cur.execute('SELECT COUNT(*) FROM todoitems WHERE user_id=?', (session['user_id'], )).fetchall()[0][0]

    remaining = total - done

    return render_template('profile.html', tasks=[total, done, remaining])


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
        
        if not is_good_password(password, confirm, username)[0]:
            flash(is_good_password(password, confirm, username)[1])
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