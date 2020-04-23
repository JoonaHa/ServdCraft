from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, validators
from application.servers.models import Status


class ServerForm(FlaskForm):
    statuses = [(member) for name, member in Status.__members__.items()]
    choices=[(status.value, status.name)for status in statuses]
    name = StringField("Server's name", [validators.Length(min=2)])
    description = TextAreaField(
        "Description:", [validators.Length(min=2, max=300)], render_kw={"rows": 4, "cols":50})
    status = SelectField("Current Status:", choices=choices)

    class Meta:
        # TODO remove
        csrf = False
