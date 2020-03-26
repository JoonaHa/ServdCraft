from flask_wtf import FlaskForm
from wtforms import StringField, validators


class GameAccountForm(FlaskForm):
    gametag = StringField("In game username:", [validators.Length(min=2)])
    uuid = StringField("Or in game uuid:", [validators.Length(min=2)])

    class Meta:
        # TODO remove
        csrf = False
