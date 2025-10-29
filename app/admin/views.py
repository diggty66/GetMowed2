"""
Routes and views for the admin blueprint.
"""
from flask import Flask, render_template, flash, redirect, request, session, logging, url_for, Blueprint
from app.forms import UserForm, RegisterForm
from app import app, db, login_manager
from flask_login import login_required, login_user, current_user, logout_user
from app.decorators import check_email_confirmed, admin_required
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import User, Role, Profile, Articles
from datetime import datetime

admin_blueprint = Blueprint(
    'admin_blueprint',
    __name__,
    template_folder='templates')

@login_manager.user_loader
def user_loader(user_id):
    """Given *user_id*, return the associated User object.
    :param unicode user_id: user_id (email) user to retrieve
    """
    return User.query.get(user_id)

@app.route('/admin/')
@login_required
@admin_required
def admin():

    role_required = Role.query.filter_by(id=current_user.id).first()

    profile = db.session.query(Profile).all()

    user = db.session.query(User).all()
    db.session.commit()

    return render_template('admin.html', user=user, profile=profile, year=datetime.now().year)

#articles
@app.route('/admin_listings')
@login_required
@admin_required
def admin_listings():

    listings = db.session.query(Articles).all()

    role_name = db.session.query(Role).filter_by(id=Role.id).first()

    result = db.session.execute
    db.session.commit()
    
    if result:
        return render_template('admin_listings.html', role_name=role_name, listings=listings, year=datetime.now().year)
    else:
        msg = 'No Articles Found'
        return render_template('admin_listings.html', msg=msg, year=datetime.now().year)