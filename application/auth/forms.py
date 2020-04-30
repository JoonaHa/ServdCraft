from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, validators
from application.auth.models import User


class LoginForm(FlaskForm):
    username = StringField("Username")
    password = PasswordField("Password")

class RegisterForm(FlaskForm):
    name = StringField("Name",[validators.Length(min=2)])
    username = StringField("Username",[validators.Length(min=2)])
    password = PasswordField("Password",[validators.Length(min=8)])

    def validate(self):
        if not FlaskForm.validate(self):
            return False
        user = User.query.filter_by(username=self.username.data).first()
        if user is  not None:
            self.username.errors.append("Username already taken")
            return False
        else:
            return True

#TODO remove
    class Meta:
        csrf = False
