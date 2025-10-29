"""
Routes and views for the users blueprint.
"""
from flask import Flask, render_template, flash, redirect, request, session, logging, url_for, Blueprint
from datetime import datetime
from app.models import User, Role, Profile
from flask import Flask, render_template, flash, redirect, request, session, logging, url_for, Blueprint
from app.forms import UserForm, RegisterForm, EditUserForm, EditRoleForm
from app import app, db, login_manager
from flask_login import login_required, login_user, current_user, logout_user
from app.decorators import check_email_confirmed, admin_required
from werkzeug.security import generate_password_hash, check_password_hash

users_blueprint = Blueprint(
    'users_blueprint',
    __name__,
    template_folder='templates'
)

@login_manager.user_loader
def user_loader(user_id):
    """Given *user_id*, return the associated User object.
    :param unicode user_id: user_id (email) user to retrieve
    """
    return User.query.get(user_id)

@app.route('/users', methods=['GET', 'POST'])
@login_required
@admin_required
def users():

    roles = db.session.query(Role).all()
    users = db.session.query(User).all()

    db.session.commit()
    
    return render_template('users.html', users=users, roles=roles, year=datetime.now().year, title="Show Users")

@app.route('/user/<string:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def user(id):
    
    # get user
    user = User.query.get(id)
    db.session.commit()

    return render_template('user.html', user=user, year=datetime.now().year)

# add user
@app.route('/add_user', methods=['GET', 'POST'])
@login_required
@admin_required
def add_user():
    form = UserForm(request.form)
    form1 = EditRoleForm(request.form)
    if request.method == 'POST' and form.validate():
        
        hashed_password = generate_password_hash(form.password.data, method='sha256')
       
        add_user = User(email = form.email.data, profile = id, _password = hashed_password, email_confirmed=False)
        add_role = Role(name = form1.name.data)
        add_user.roles = [add_role]
        db.session.add(add_user)
        db.session.add(add_role)
        db.session.commit()
        db.session.close()
        flash('User Created', 'success')

        return redirect(url_for('users'))
    return render_template('add_user.html', form=form, form1=form1, year=datetime.now().year)

# edit user
@app.route('/edit_user/<string:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_user(id):
    # get user
    edit_user = User.query.filter_by(id=id).first()
    # get user role
    edit_role = Role.query.filter_by(id=id).first()
    # populate user form fields
    form1 = EditUserForm(request.form, obj=edit_user)
    form2 = EditRoleForm(request.form, obj=edit_role)

    if request.method == 'POST' and form1.validate() and form2.validate():
        edit_user.email = form1.email.data
        #edit_user.roles = form1.roles.data
        edit_role.name = form2.name.data
        
        db.session.merge(edit_user)
        db.session.merge(edit_role)
        
        # commit to db
        db.session.commit()
        db.session.close()

        flash('User Updated', 'success')
        
        return redirect(url_for('users'))

    return render_template('edit_user.html', form1=form1, form2=form2, year=datetime.now().year)

#delete user
@app.route('/delete_user/<string:id>', methods=['POST'])
@login_required
@admin_required
def delete_user(id):

    if request.method == 'POST':
        # get user
        delete_user = User.query.filter(User.id==id).first()
        # get profile
        delete_profile = Profile.query.filter(Profile.id==id).first()
        # get role
        delete_role = Role.query.filter(Role.id==id).first()
        if delete_role != None:
            # delete role
            db.session.delete(delete_role)
        if delete_profile != None:
            # delete profile
            db.session.delete(delete_profile)
        # delete user
        db.session.delete(delete_user)

        db.session.commit()

        flash('User Deleted', 'success')
    return redirect(url_for('users'))