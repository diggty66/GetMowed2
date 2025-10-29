"""
Routes and views for the dashboards blueprint.
"""
from flask import Flask, render_template, flash, redirect, request, session, logging, url_for, Blueprint
from functools import wraps
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from GetMowed2.models import User, Role, Profile, Articles
from GetMowed2.forms import LoginForm, RegisterForm, RegisterMowerForm, RegisterAdminForm
from GetMowed2.emails.token import generate_confirmation_token
from GetMowed2.emails.email import send_email
from GetMowed2 import app, db, login_manager
from flask_login import login_required, login_user, current_user, logout_user

dashboards_blueprint = Blueprint(
    'dashboards_blueprint',
    __name__,
    template_folder='templates'
)

@login_manager.user_loader
def user_loader(user_id):
    """Given *user_id*, return the associated User object.
    :param unicode user_id: user_id (email) user to retrieve
    """
    return User.query.get(user_id)

@app.route('/password_change', methods=["GET", "POST"])
@login_required
def user_password_change():
    form = RegisterForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            user = current_user
            user.password = form.password.data
            db.session.add(user)
            db.session.commit()
            flash('Password has been updated!', 'success')
            return redirect(url_for('users.user_profile'))
 
    return render_template('password_change.html', form=form, year=datetime.now().year)

#register customer
@app.route('/register_mowee', methods=['GET', 'POST'])
def register_mowee():
    # Creating RegistrationForm class object
    form = RegisterForm(request.form)
    # Cheking that method is post and form is valid or not.
    if request.method == 'POST' and form.validate():
    #try:                  
        # if all is fine, generate hashed password
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        # create new user model object
        new_user = User(email = form.email.data, profile = id, _password = hashed_password, email_confirmed=False)
        new_user.authenticated = True
        # saving user object into data base with hashed password
        db.session.add(new_user)
        mowee = Role(name='Mowee')
        new_user.roles = [mowee]
        db.session.add(mowee)
        db.session.commit()

        token = generate_confirmation_token(new_user.email)
        confirm_url = url_for('confirm_email', token=token, _external=True)
        html = render_template('activate.html', confirm_url=confirm_url)
        subject = "Please confirm your email"
        send_email(new_user.email, subject, html)

        flash('You have successfully registered', 'success')
        # if registration successful, then redirecting to login Api
        return redirect(url_for('login'))
    #except Exception as error:
        #db.session.rollback()
        #flash('ERROR! Email ({}) already exists.'.format(form.email.data), "Danger")

            # if method is Get, than render registration form
    return render_template('register_mowee.html', form = form, year=datetime.now().year)

    #register customer
@app.route('/register_mower', methods=['GET', 'POST'])
def register_mower():
    # Creating RegistrationForm class object
    form = RegisterForm(request.form)
    # Cheking that method is post and form is valid or not.
    if request.method == 'POST' and form.validate():
        try:
            # if all is fine, generate hashed password
            hashed_password = generate_password_hash(form.password.data, method='sha256')
            # create new user model object
            new_user = User(email = form.email.data, profile = id, _password = hashed_password, email_confirmed=False)
            new_user.authenticated = True
            # saving user object into data base with hashed password
            db.session.add(new_user)
            mower = Role(name='Mower')
            new_user.roles = [mower]
            db.session.add(mower)
            db.session.commit()

            token = generate_confirmation_token(new_user.email)
            confirm_url = url_for('confirm_email', token=token, _external=True)
            html = render_template('activate.html', confirm_url=confirm_url)
            subject = "Please confirm your email"
            send_email(new_user.email, subject, html)

            flash('You have successfully registered', 'success')
            # if registration successful, then redirecting to login Api
            return redirect(url_for('login'))

        except Exception as error:
            db.session.rollback()
            flash('ERROR! Email ({}) already exists.', "Danger")
    
    # if method is Get, than render registration form
    return render_template('register_mower.html', form = form, year=datetime.now().year)

# Login API endpoint implementation
@app.route('/login/', methods = ['GET', 'POST'])
def login():
    # Creating Login form object
    form = LoginForm(request.form)
    # verifying that method is post and form is valid
    if request.method == 'POST' and form.validate:
        # checking that user is exist or not by email
        user = User.query.filter_by(email = form.email.data).first()
        
        if user is not None:
            # if user exist in database than we will compare our database hased password and password come from login form 
            if check_password_hash(user._password, form.password.data):
                # if password is matched, allow user to access and save email and username inside the session
                flash('You have successfully logged in.', "success")

                user.authenticated = True
                user.last_logged_in = user.current_logged_in
                user.current_logged_in = datetime.now()
                db.session.add(user)
                db.session.commit()
                login_user(user)
                # After successful login, redirecting to home page
                profile = Profile.query.filter_by(id=current_user.id).first()
                if profile is None:
                    return redirect(url_for('add_profile'))
                else:
                    return redirect(url_for('dashboard'))

            else:

                # if password is in correct , redirect to login page
                flash('Username or Password Incorrect', "Danger")

                return redirect(url_for('login'))
    # rendering login page
    return render_template('login.html', form = form, year=datetime.now().year)

#logout
@app.route('/logout/')
@login_required
def logout():
    user = current_user
    user.authenticated = False
    db.session.add(user)
    db.session.commit()
    logout_user()
    flash('You are now logged out', 'success')
    return redirect(url_for('home'))

#dashboard
@app.route('/dashboard')
@login_required
def dashboard():
    
    profile_data = Profile.query.filter_by(id=current_user.id).first()

    if Profile == None:
        return redirect(url_for('add_profile', id=users_id))

    listings = db.session.query(Articles).all()
    db.session.commit()

    return render_template('dashboard.html', profile_data=profile_data, listings=listings, year=datetime.now().year)