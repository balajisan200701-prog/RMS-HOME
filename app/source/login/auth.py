from functools import wraps
from flask import session, redirect

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):

        if not session.get('logged_in'):
            return redirect('/login')

        return f(*args, **kwargs)

    return decorated

def admin_required(f):

    @wraps(f)
    def decorated(*args, **kwargs):

        if session.get('role') != 'admin':
            return redirect('/admin/bill')

        return f(*args, **kwargs)

    return decorated