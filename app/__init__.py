"""
The flask application package.
"""
from flask import Flask, Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail, Message
import json
 
app = Flask(__name__)
app.config.from_object(__name__)
# from GetMowed2 import app as application

#with open('/etc/config.json') as config_file:
#  config = json.load(config_file)

app.config.from_file("/etc/config.json", load=json.load)

# Magic that creates everything, including Base (db.Model), engine (db.engine), and session >
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Mowed2.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = 'SQLALCHEMY_TRACK_MODIFICATIONS'
app.config['SECRET_KEY'] = 'SECRET_KEY'
app.config['SECURITY_PASSWORD_SALT'] = 'SECURITY_PASSWORD_SALT'

# mail settings
app.config['MAIL_SERVER']= 'MAIL_SERVER'
app.config['MAIL_PORT'] = 'MAIL_PORT'
app.config['MAIL_USE_TLS'] = 'MAIL_USE_TLS'
app.config['MAIL_USE_SSL'] = 'MAIL_USE_SSL'
app.config['TESTING'] = 'TESTING'
app.config['MAIL_SUPPRESS_SEND'] = 'MAIL_SUPPRESS_SEND'
app.config['MAIL_FAIL_SILENTLY'] = 'MAIL_FAIL_SILENTLY' 

# gmail authentication
app.config['MAIL_USERNAME'] = 'MAIL_USERNAME'
app.config['MAIL_PASSWORD'] = 'MAIL_PASSWORD'

# mail accounts
app.config['MAIL_DEFAULT_SENDER'] = 'MAIL_DEFAULT_SENDER'
mail = Mail(app)

db = SQLAlchemy(app)

# flask-user
login_manager = LoginManager(app)
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_view = 'admin'

# import a blueprints
from GetMowed2.articles.views import articles_blueprint
from GetMowed2.dashboards.views import dashboards_blueprint
from GetMowed2.emails.views import emails_blueprint
from GetMowed2.home.views import home_blueprint
from GetMowed2.profiles.views import profiles_blueprint
from GetMowed2.users.views import users_blueprint
from GetMowed2.admin.views import admin_blueprint

# register blueprints with the application
app.register_blueprint(articles_blueprint, url_prefix='/articles')
app.register_blueprint(dashboards_blueprint, url_prefix='/dashboards')
app.register_blueprint(emails_blueprint, url_prefix='/emails')
app.register_blueprint(home_blueprint, url_prefix='/home')
app.register_blueprint(profiles_blueprint, url_prefix='/profiles')
app.register_blueprint(users_blueprint, url_prefix='/users')
app.register_blueprint(admin_blueprint, url_prefix='/admin')

# create all tables
models.db.create_all()
