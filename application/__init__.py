from flask import Flask
app = Flask(__name__)


from flask_sqlalchemy import SQLAlchemy

import os
if os.environ.get("HEROKU"):
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
else:
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///servedCraftTest.db"

db = SQLAlchemy(app)

from os import urandom
app.config["SECRET_KEY"] = urandom(32)

from application import views
from application.auth import models
from application.auth import views
from application.gameAccounts import models
from application.gameAccounts import views

from application.servers import models
from application.servers import views

from application.auth.models import User
from application.gameAccounts.models import GameAccount
from flask_login import current_user



from flask_login import LoginManager
login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view = "auth_login"
login_manager.login_message = "Please login to use this functionality."

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

try: 
    db.create_all()
except:
    pass

user = User.query.filter_by(username="test").first()
if user is None:
    user = User("test_account","test","1234")
    user.isAdmin = True
    db.session().add(user)
    db.session().commit()
    account = GameAccount(user,"xxx_test_xx", "1234")
    db.session().add(account)
    db.session().commit()





