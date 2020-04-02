from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, validators
from application.servers.models import Status


class ServerForm(FlaskForm):
    name = StringField("Server's name", [validators.Length(min=2)])
    description = TextAreaField(
        "Description:", [validators.Length(min=2, max=300)])
    status = SelectField("Current Status:", list(Status))

    class Meta:
        # TODO remove
        csrf = False
