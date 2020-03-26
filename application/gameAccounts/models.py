from application import db

class GameAccount(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    gametag  = db.Column(db.String(144), nullable=True)
    uuid  = db.Column(db.String(144), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('account.id'))
    user = db.relationship("User", back_populates="game_accounts")

    def __init__(self, user, gametag=None, uuid=None):
        self.user_id = user.id
        self.gametag = gametag
        self.uuid = uuid
