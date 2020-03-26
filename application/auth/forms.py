from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, validators


class LoginForm(FlaskForm):
    username = StringField("Username")
    password = PasswordField("Password")

class RegisterForm(FlaskForm):
    name = StringField("Name",[validators.Length(min=2)])
    username = StringField("Username",[validators.Length(min=2)])
    password = PasswordField("Password",[validators.Length(min=8)])

#TODO remove
    class Meta:
        csrf = False
