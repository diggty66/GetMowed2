"""
Routes and views for the home blueprint.
"""
from flask import Flask, render_template, flash, redirect, request, session, logging, url_for, Blueprint
from datetime import datetime
from GetMowed2 import app

home_blueprint = Blueprint(
    'home_blueprint',
    __name__,
    template_folder='templates')

@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""
    return render_template('index.html', title='Home Page', year=datetime.now().year,)

@app.route('/contact')
def contact():
    """Renders the contact page."""
    return render_template('contact.html', title='Contact', year=datetime.now().year, message='Your contact page.')

@app.route('/about')
def about():
    """Renders the about page."""
    return render_template('about.html', title='About', year=datetime.now().year, message='Your application description page.')

