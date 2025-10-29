from flask_wtf import FlaskForm
from wtforms import Form, BooleanField, StringField, PasswordField, validators, TextAreaField, IntegerField
from wtforms.validators import DataRequired, Email, EqualTo



# Creating Login Form contains email and password
class LoginForm(Form):
    email = StringField("Email", validators=[validators.Length(min=7, max=50), validators.DataRequired(message="Please Fill This Field")])
    password = PasswordField("Password", validators=[validators.DataRequired(message="Please Fill This Field")])

# Creating Registration Form contains username, name, email, password and confirm password.
class RegisterForm(Form):
    email = StringField("Email", validators=[validators.Email(message="Please enter a valid email address")])
    password = PasswordField("Password", validators=[
        validators.DataRequired(message="Please Fill This Field"),
        validators.EqualTo(fieldname="confirm", message="Your Passwords Do Not Match")
    ])
    confirm = PasswordField("Confirm Password", validators=[validators.DataRequired(message="Please Fill This Field")])

class RegisterMowerForm(Form):
    email = StringField("Email", validators=[validators.Email(message="Please enter a valid email address")])
    password = PasswordField("Password", validators=[
        validators.DataRequired(message="Please Fill This Field"),
        validators.EqualTo(fieldname="confirm", message="Your Passwords Do Not Match")
    ])
    confirm = PasswordField("Confirm Password", validators=[validators.DataRequired(message="Please Fill This Field")])

class RegisterAdminForm(Form):
    email = StringField("Email", validators=[validators.Email(message="Please enter a valid email address")])
    password = PasswordField("Password", validators=[
        validators.DataRequired(message="Please Fill This Field"),
        validators.EqualTo(fieldname="confirm", message="Your Passwords Do Not Match")])
    confirm = PasswordField("Confirm Password", validators=[validators.DataRequired(message="Please Fill This Field")])

# user form class
class UserForm(Form):
     email = StringField('Email', [validators.Length(min=6, max=50)])
     roles = StringField('Role', [validators.Optional(), validators.Length(min=0, max=25)])
     password = PasswordField("Password", validators=[
        validators.DataRequired(message="Please Fill This Field"),
        validators.EqualTo(fieldname="confirm", message="Your Passwords Do Not Match")])
     confirm = PasswordField("Confirm Password", validators=[validators.DataRequired(message="Please Fill This Field")])

# edit user form class
class EditUserForm(Form):
     email = StringField('Email', [validators.Length(min=6, max=50)])
     roles = StringField('Role', [validators.Optional(), validators.Length(min=0, max=25)])
# edit user form class
class EditRoleForm(Form):
     name = StringField('Role', [validators.Optional(), validators.Length(min=0, max=25)])

# profile form class
class ProfileForm(Form):
     username = StringField("Username", [validators.Length(min=0, max=25)])
     first_name = StringField("First Name", [validators.Length(min=0, max=50)])
     last_name = StringField("Last Name", [validators.Length(min=0, max=50)])
     address = StringField("Address", [validators.Length(min=0, max=50)])
     address2 = StringField("Address2", [validators.Length(min=0, max=50)])
     town = StringField("Town", [validators.Length(min=0, max=50)])
     state = StringField("State", [validators.Length(min=0, max=55)])
     zip_code = StringField("Zip Code", [validators.Length(min=0, max=5)])


# article form class
class ArticleForm(Form):
    title = StringField('Title', [validators.Length(min=1, max=200)])
    body = TextAreaField('Body', [validators.Length(min=30)])
    #author = StringField('Author', [validators.Length(min=1, max=200)])
