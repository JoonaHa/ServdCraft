from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, validators
from application.servers.models import Status, Server


class ServerForm(FlaskForm):
    statuses = [(member) for name, member in Status.__members__.items()]
    choices = [(status.value, status.name)for status in statuses]
    name = StringField("Server's name", [validators.Length(min=2, max=144)])
    description = TextAreaField(
        "Description:", [validators.Length(min=2, max=500)])
    status = SelectField("Current Status:", choices=choices, coerce=int)

    def validate(self):
        if not FlaskForm.validate(self):
            return False
        server = Server.query.filter_by(name=self.name.data).first()
        if server is not None:
            self.username.errors.append("Server name already taken")
            return False
        else:
            return True


class JoinForm(FlaskForm):
    accounts = SelectField("Join server:", coerce=int)


class EditForm(FlaskForm):
    statuses = [(member) for name, member in Status.__members__.items()]
    choices = [(status.value, status.name)for status in statuses]
    description = TextAreaField(
        "Description:", [validators.Length(min=2, max=500)])
    status = SelectField("Current Status:", choices=choices, coerce=int)



class Meta:
    # TODO remove
    csrf = False
