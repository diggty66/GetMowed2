"""
The flask application package.
"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
import os

app = Flask(__name__)

# --- Core configuration ---
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Mowed2.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'devsecret')
app.config['SECURITY_PASSWORD_SALT'] = os.environ.get('SECURITY_PASSWORD_SALT', 'devsalt')

# --- Mail configuration ---
app.config.update(
    MAIL_SERVER=os.environ.get('MAIL_SERVER', 'smtp.gmail.com'),
    MAIL_PORT=int(os.environ.get('MAIL_PORT', 587)),
    MAIL_USE_TLS=True,
    MAIL_USERNAME=os.environ.get('MAIL_USERNAME', ''),
    MAIL_PASSWORD=os.environ.get('MAIL_PASSWORD', ''),
    MAIL_DEFAULT_SENDER=os.environ.get('MAIL_DEFAULT_SENDER', '')
)

mail = Mail(app)
db = SQLAlchemy(app)

# --- Flask-Login setup ---
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# --- Import blueprints ---
from app.articles.views import articles_blueprint
from app.dashboards.views import dashboards_blueprint
from app.emails.views import emails_blueprint
from app.home.views import home_blueprint
from app.profiles.views import profiles_blueprint
from app.users.views import users_blueprint
from app.admin.views import admin_blueprint

# --- Register blueprints ---
app.register_blueprint(articles_blueprint, url_prefix='/articles')
app.register_blueprint(dashboards_blueprint, url_prefix='/dashboards')
app.register_blueprint(emails_blueprint, url_prefix='/emails')
app.register_blueprint(home_blueprint, url_prefix='/home')
app.register_blueprint(profiles_blueprint, url_prefix='/profiles')
app.register_blueprint(users_blueprint, url_prefix='/users')
app.register_blueprint(admin_blueprint, url_prefix='/admin')

# --- Create DB tables if needed ---
with app.app_context():
    db.create_all()
