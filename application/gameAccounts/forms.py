from flask_wtf import FlaskForm
from wtforms import StringField, validators


class GameAccountForm(FlaskForm):
    gametag = StringField("In game username:", [validators.Optional(), validators.Length(min=2, max=144)])
    uuid = StringField("Or in game uuid:", [validators.Optional(),validators.Length(min=2, max=144)])

    def validate(self):
        if not FlaskForm.validate(self):
            return False
        if not self.gametag.data and not self.uuid.data:
            self.gametag.errors.append("In game username or uuid required")
            return False
        else:
            return True

    class Meta:
        # TODO remove
        csrf = False
