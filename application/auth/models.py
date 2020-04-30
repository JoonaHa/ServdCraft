from application import db
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):

    __tablename__ = "account"

    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(),
                              onupdate=db.func.current_timestamp())

    name = db.Column(db.String(144), nullable=False)
    isAdmin = db.Column(db.Boolean, default=False)
    username = db.Column(db.String(144), nullable=False)
    password_hash = db.Column(db.String(144), nullable=False)
    game_accounts = db.relationship("GameAccount", back_populates="user")
    ownServers =db.relationship("Server", back_populates="creator")

    def __init__(self, name, username, password):
        self.name = name
        self.username = username
        self.set_password(password)

    def get_id(self):
        return self.id

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def is_authenticated(self):
        return self._authenticated

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
