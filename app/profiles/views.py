"""
Routes and views for the profile blueprint.
"""
from flask import Flask, render_template, flash, redirect, request, session, logging, url_for, Blueprint
from datetime import datetime
from GetMowed2.models import User, Profile
from GetMowed2.forms import ProfileForm
from GetMowed2 import app, db, login_manager
from flask_login import login_required, login_user, current_user, logout_user
from GetMowed2.decorators import check_email_confirmed

profiles_blueprint = Blueprint(
    'profiles_blueprint',
    __name__,
    template_folder='templates'
)

@login_manager.user_loader
def user_loader(user_id):
    """Given *user_id*, return the associated User object.
    :param unicode user_id: user_id (email) user to retrieve
    """
    return User.query.get(user_id)

@app.route('/profile/<string:id>', methods=['GET', 'POST'])
@login_required
@check_email_confirmed
def profile(id):

    # get user email
    user_email = User.query.get(id)
    # get user profile
    profile_data = Profile.query.filter_by(id=current_user.id).first()
    db.session.commit()

    return render_template('profile.html', user_email=user_email, profile_data=profile_data, year=datetime.now().year)

#add article
@app.route('/profile/add_profile', methods=['GET', 'POST'])
@login_required
def add_profile():

    form = ProfileForm(request.form)

    if request.method == 'POST' and form.validate():

        users_id = Profile.get_id

        add_profile = Profile(users_id = current_user.id, username=request.form.get("username"), first_name=request.form.get("first_name"), last_name=request.form.get("last_name"), address=request.form.get("address"), address2=request.form.get("address2"), town=request.form.get("town"), state=request.form.get("state"), zip_code=request.form.get("zip_code"))
        
        db.session.add(add_profile)
        db.session.commit()
        db.session.close()
        flash('Profile Created', 'success')

        return redirect(url_for('profile', id=users_id))

    return render_template('add_profile.html', form=form, year=datetime.now().year)

#edit profile
@app.route('/profile/edit_profile/<string:id>', methods=['GET', 'POST'])
@login_required
def edit_profile(id):

    # get user
    edit_profile = Profile.query.filter_by(id=id).first()
    
    # populate profile form fields
    form = ProfileForm(request.form, obj=edit_profile)
    
    if request.method == 'POST' and form.validate():
        edit_profile.username = form.username.data
        edit_profile.first_name = form.first_name.data
        edit_profile.last_name = form.last_name.data
        edit_profile.address = form.address.data
        edit_profile.address2 = form.address2.data
        edit_profile.town = form.town.data
        edit_profile.state = form.state.data
        edit_profile.zip_code = form.zip_code.data

        db.session.merge(edit_profile)
        
        # commit to db
        db.session.commit()
        db.session.close()
        flash('Profile Updated', 'success')
        
        return redirect(url_for('edit_profile', id=id))

    return render_template('edit_profile.html', edit_profile=edit_profile, form=form, year=datetime.now().year)