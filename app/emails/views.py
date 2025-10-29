"""
Routes and views for the emails blueprint.
"""
from flask import Flask, render_template, flash, redirect, request, session, logging, url_for, Blueprint
from functools import wraps
from datetime import datetime
from app.models import User
from app import app, db, login_manager
from flask_login import login_required, login_user, current_user, logout_user
from app.emails.token import generate_confirmation_token, confirm_token
from app.emails.email import send_email
from app.decorators import check_email_confirmed

emails_blueprint = Blueprint(
    'emails_blueprint',
    __name__,
    template_folder='templates'
)

@login_manager.user_loader
def user_loader(user_id):
    """Given *user_id*, return the associated User object.
    :param unicode user_id: user_id (email) user to retrieve
    """
    return User.query.get(user_id)

def send_async_email(msg):
    with app.app_context():
        mail.send(msg)

def send_confirmation_email(user_email):
    confirm_serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
 
    confirm_url = url_for(
        'email_confirmation',
        token=confirm_serializer.dumps(user_email, salt='email-confirmation-salt'),
        _external=True)
 
    html = render_template(
        'email_confirmation.html',
        confirm_url=confirm_url)
 
    send_email('Confirm Your Email Address', [user_email], html)

@app.route('/confirm/<token>')
@login_required
def confirm_email(token):
    try:
        email = confirm_token(token)
    except:
        flash('The confirmation link is invalid or has expired.', 'danger')
    user = User.query.filter_by(email=email).first_or_404()
    if user.email_confirmed:
        flash('Account already confirmed. Please login.', 'success')
    else:
        user.email_confirmed = True
        user.email_confirmed_on = datetime.now()
        db.session.add(user)
        db.session.commit()
        flash('You have confirmed your account. Thanks!', 'success')
    return redirect(url_for('dashboard'))

@app.route('/resend_confirmation')
@login_required
def resend_email_confirmation():
    token = generate_confirmation_token(current_user.email)
    confirm_url = url_for('confirm_email', token=token, _external=True)
    html = render_template('activate.html', confirm_url=confirm_url)
    subject = "Please confirm your email"
    send_email(current_user.email, subject, html)
    flash('A new confirmation email has been sent.', 'success')
    return redirect(url_for('unconfirmed'))

@app.route('/email_change', methods=["GET", "POST"])
@login_required
def user_email_change():
    form = UserForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            try:
                user_check = User.query.filter_by(email=form.email.data).first()
                if user_check is None:
                    user = current_user
                    user.email = form.email.data
                    user.email_confirmed = False
                    user.email_confirmed_on = None
                    user.email_confirmation_sent_on = datetime.now()
                    db.session.add(user)
                    db.session.commit()
                    send_confirmation_email(user.email)
                    flash('Email changed!  Please confirm your new email address (link sent to new email).', 'success')
                    return redirect(url_for('users.user_profile'))
                else:
                    flash('Sorry, that email already exists!', 'error')
            except IntegrityError:
                flash('Error! That email already exists!', 'error')
    return render_template('email_change.html', form=form, year=datetime.now().year)

@app.route('/unconfirmed')
@login_required
def unconfirmed():
    if current_user.email_confirmed:
        if Profile is None:
            return redirect(url_for('add_profile'))
        else:
            return redirect(url_for('dashboard'))
    flash('Please confirm your account!', 'warning')
    return render_template('unconfirmed.html', year=datetime.now().year)