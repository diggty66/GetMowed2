"""
Routes and views for the articles blueprint.
"""
from flask import Flask, render_template, flash, redirect, request, session, logging, url_for, Blueprint
from functools import wraps
from datetime import datetime
from app.models import Articles
from app.forms import ArticleForm
from app import app, db, login_manager
from flask_login import login_required, login_user, current_user, logout_user

articles_blueprint = Blueprint(
    'articles_blueprint',
    __name__,
    template_folder='templates'
)

@login_manager.user_loader
def user_loader(user_id):
    """Given *user_id*, return the associated User object.
    :param unicode user_id: user_id (email) user to retrieve
    """
    return User.query.get(user_id)

#articles
@app.route('/listings')
def listings():

    listings = db.session.query(Articles).all()
    result = db.session.execute
    db.session.commit()
    
    if result:
        return render_template('listings.html', listings=listings, year=datetime.now().year)
    else:
        msg = 'No Articles Found'
        return render_template('listings.html', msg=msg, year=datetime.now().year)

#single article
@app.route('/listing/<string:id>/')
def listing(id):

    #get articles
    listing = Articles.query.get(id)
    db.session.commit()
    
    return render_template('listing.html', listing=listing, year=datetime.now().year)

#add article
@app.route('/add_listing', methods=['GET', 'POST'])
@login_required
def add_listing():

    form = ArticleForm(request.form)

    if request.method == 'POST' and form.validate():        
       
        add_listing = Articles(title=request.form.get("title"), body=request.form.get("body"), author=current_user.email, create_date=datetime.now())
        
        db.session.add(add_listing)
        db.session.commit()
        
        flash('Listing Created', 'success')

        return redirect(url_for('dashboard'))

    return render_template('add_listing.html', form=form, year=datetime.now().year)

#delete article
@app.route('/delete_listing/<string:id>', methods=['GET', 'POST'])
@login_required
def delete_listing(id):
    
    if request.method == 'POST':
        
        # get article
        delete_listing = Articles.query.filter(Articles.id==id).first()
        
        # delete article
        db.session.delete(delete_listing)

        # commit to db
        db.session.commit()

    flash('Listing Deleted', 'success')

    return redirect(request.referrer)
    

#edit article
@app.route('/edit_listing/<string:id>', methods=['GET', 'POST'])
@login_required
def edit_listing(id):

    # get articles
    edit_listing = Articles.query.filter_by(id=id).first()
    
    # populate article form fields
    form = ArticleForm(request.form, obj=edit_listing)
    
    if request.method == 'POST' and form.validate():
        edit_listing.body = form.body.data
        edit_listing.title = form.title.data
        
        db.session.merge(edit_listing)
        
        # commit to db
        db.session.commit()
        
        flash('Article Updated', 'success')

        return redirect(request.referrer)

    return render_template('edit_listing.html', form=form, year=datetime.now().year)