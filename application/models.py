from application import db
from werkzeug.security import generate_password_hash, check_password_hash
#from sqlalchemy.orm import relationship

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())

    name = db.Column(db.String(144), nullable=False)
    username = db.Column(db.String(144), nullable=False)
    email = db.Column(db.String(144), nullable=False)
    password_hash = db.Column(db.String(144), nullable=False)
    game_accounts = db.relationship("GameAccount", back_populates="user")
    

    def __init__(self, name, username, email, password):
        self.name = name
        self.username = username
        self.email = email
        self.set_password(password)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class GameAccount(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    gametag  = db.Column(db.String(144), nullable=True)
    uuid  = db.Column(db.String(144), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship("User", back_populates="game_accounts")

    def __init__(self, user, gametag=None, uuid=None):
        self.user_id = user.id
        self.gametag = gametag
        self.uuid = uuid
