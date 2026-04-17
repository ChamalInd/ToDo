from flask import session, redirect
from functools import wraps


def login_required(f):
    @wraps(f)
    def decerated_function(*args, **kwargs):
        if session.get('user_id') is None:
            return redirect('/login')
        return f(*args, **kwargs)
    
    return decerated_function


def is_good_password(password, confirm, username):
    if password != confirm:
        return [False, 'Passwords dosen\'t match.']
    
    if password == username:
        return [False, 'Password cannot be the same as username.']
    
    if len(password) < 8:
        return [False, 'Password should contain minium 8 characters.']

    if (password.isnumeric()) or (password.isalpha()):
        return [False, 'Password should have both numbers and letters.']
                
    if (password.islower()) or (password.isupper()):
        return [False, 'Password should contain both upper and lower characters.']

    return [True, 'Good']