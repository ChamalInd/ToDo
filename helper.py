from flask import session, redirect, render_template
from functools import wraps


def login_required(f):
    @wraps(f)
    def decerated_function(*args, **kwargs):
        if session.get('user_id') is None:
            return redirect('/login')
        return f(*args, **kwargs)
    
    return decerated_function