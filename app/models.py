from app import db, login_manager
from flask_login import UserMixin
from datetime import datetime
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Boolean
from sqlalchemy.orm import relationship

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

class Articles(db.Model):
    __tablename__='articlestable'
    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)
    body = Column(String(1000), nullable=False)
    author = Column(String(200), nullable=False)
    create_date = Column(DateTime)

    def __repr__ (self):
        return '<Articles {}>'.format(self.listing)

# Profile data model
class Profile(db.Model, UserMixin):
    __tablename__ = 'profiletable'
    id = Column(Integer, primary_key=True)
    users_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)

    # User fields
    username = Column(String(50), nullable=True)
    first_name = Column(String(50), nullable=True)
    last_name = Column(String(50), nullable=True)

    # Address fields
    address = Column(String(50), nullable=True)
    address2 = Column(String(50), nullable=True)
    town = Column(String(50), nullable=True)
    state = Column(String(50), nullable=True)
    zip_code = Column(String(10), nullable=True)

    def __init__(self, users_id, username, first_name, last_name, address, address2, town, state, zip_code):
        self.users_id = users_id
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.address = address
        self.address2 = address2
        self.town = town
        self.state = state
        self.zip_code = zip_code

# Define the UserRoles association table
UserRoles = db.Table('user_roles',
     Column('user_id', Integer(), db.ForeignKey('users.id', ondelete='CASCADE'), primary_key=True, nullable=False),
     Column('role_id', Integer(), db.ForeignKey('roles.id', ondelete='CASCADE'), primary_key=True, nullable=False))

# Define User data-model
class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    roles = relationship('Role', secondary='user_roles', backref=db.backref('users', lazy=True))
    profile = relationship('Profile', backref='users', lazy=True)

    # User Authentication fields
    email = Column(String, unique=True, nullable=False)
    _password = Column(String(60), nullable=False)
    authenticated = Column(Boolean, default=False)
    email_confirmation_sent_on = Column(DateTime, nullable=True)
    email_confirmed = Column(Boolean, nullable=True, default=False)
    email_confirmed_on = Column(DateTime, nullable=True)
    registered_on = Column(DateTime, nullable=True)
    last_logged_in = Column(DateTime, nullable=True)
    current_logged_in = Column(DateTime, nullable=True)
    create_date = Column(DateTime)

    def __init__(self, profile, email, _password, email_confirmed, email_confirmation_sent_on=None):
        self.email = email
        self._password = _password
        self.authenticated = False
        self.email_confirmation_sent_on = email_confirmation_sent_on
        self.email_confirmed = False
        self.email_confirmed_on = None
        self.registered_on = datetime.now()
        self.last_logged_in = None
        self.current_logged_in = datetime.now()

# Define the Role data-model
class Role(db.Model):
    __tablename__ = 'roles'
    id = Column(Integer(), primary_key=True)
    name = Column(String(50), unique=False)

    def __str__(self):
        return self.name
