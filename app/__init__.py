"""
The flask application package.
"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
from dotenv import load_dotenv        # NEW: load .env variables
import os

# --- Load environment variables from .env ---
load_dotenv()

app = Flask(__name__)

# --- Core configuration ---
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI', 'sqlite:///Mowed2.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'devsecret')
app.config['SECURITY_PASSWORD_SALT'] = os.getenv('SECURITY_PASSWORD_SALT', 'devsalt')

# --- Mail configuration ---
app.config.update(
    MAIL_SERVER=os.getenv('MAIL_SERVER', 'smtp.gmail.com'),
    MAIL_PORT=int(os.getenv('MAIL_PORT', 587)),
    MAIL_USE_TLS=os.getenv('MAIL_USE_TLS', 'True') == 'True',
    MAIL_USERNAME=os.getenv('MAIL_USERNAME', ''),
    MAIL_PASSWORD=os.getenv('MAIL_PASSWORD', ''),
    MAIL_DEFAULT_SENDER=os.getenv('MAIL_DEFAULT_SENDER', '')
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
