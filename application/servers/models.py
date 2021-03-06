from application import db
from application.gameAccounts.models import GameAccount
from enum import Enum


class Status(Enum):
    Online = 1
    Offline = -1
    Updating = 0


class Server(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(),
                              onupdate=db.func.current_timestamp())
    name = db.Column(db.String(144), nullable=False)
    description = db.Column(db.String(500), nullable=True)
    status = db.Column(db.Enum(Status), default=Status.Offline)
    creator_id = db.Column(db.Integer, db.ForeignKey('account.id'))
    creator = db.relationship("User", back_populates="ownServers")

    game_accounts = db.relationship(
        "GameAccountServer", back_populates="server")

    def __init__(self, name, status, creator, description=""):
        self.name = name
        self.status = status
        self.creator_id = creator.id
        self.description = description


class GameAccountServer(db.Model):
    __tablename__ = 'GameAccountServer'
    id = db.Column(db.Integer, primary_key=True)
    isOwner = db.Column(db.Boolean, nullable=False, default=False)
    isModerator = db.Column(db.Boolean, nullable=False, default=False)
    server_id = db.Column(db.Integer, db.ForeignKey(Server.id))
    game_account_id = db.Column(
        db.Integer, db.ForeignKey(GameAccount.id))

    server = db.relationship("Server", back_populates="game_accounts")
    game_account = db.relationship("GameAccount", back_populates="servers")
