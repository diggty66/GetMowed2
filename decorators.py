from GetMowed2 import app, db, login_manager
from functools import wraps
from GetMowed2.models import Role, User
from flask import flash, redirect, url_for
from flask_login import current_user

def admin_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        role_required = Role.query.filter_by(id=current_user.id).first()
        if role_required.name == 'admin':
            return f(*args, **kwargs)
        else:
            flash("You need to be an admin to view that page.")
            return redirect(url_for('dashboard'))
    return wrap

def check_email_confirmed(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if current_user.email_confirmed is False:
            flash('Please confirm your account!', 'warning')
            return redirect(url_for('unconfirmed'))
        return func(*args, **kwargs)

    return decorated_function
