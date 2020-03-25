from flask import render_template, request, redirect, url_for
from application import app, db
from application.models import User, GameAccount
from application.tasks.forms import GameAccountForm


@app.route("/")
def index():
    return redirect(url_for("gameaccount_index"))


@app.route("/game_accounts", methods=["GET"])
def gameaccount_index():
    return render_template("gameaccount/list.html", gameaccounts=GameAccount.query.all())


@app.route("/game_accounts/new/")
def gameaccount_form():
    return render_template("gameaccount/new.html", form=GameAccountForm())


@app.route("/game_accounts/<account_id>/", methods=["GET"])
def gameaccount_updateform(account_id):

    return render_template("gameaccount/account.html", account = GameAccount.query.get(account_id))


@app.route("/game_accounts/<account_id>/", methods=["POST"])
def gameaccount_update(account_id):

    account = GameAccount.query.get(account_id)
    account.gametag = request.form.get("gametag")
    account.uuid = request.form.get("uuid")
    db.session().commit()
    return redirect(url_for("gameaccount_index"))


@app.route("/game_account/", methods=["POST"])
def gameaccount_create():

    form = GameAccountForm(request.form)
    
    if not form.validate():
        return render_template("gameaccount/new.html", form = form)
    
    
    user = User.query.filter_by(username ="anonymous").first()
    if user is None:
        user = User("anonymous", "anonymous", "test@example.com", password="1234")
        db.session().add(user)

    gameaccount = GameAccount(user, gametag= form.gametag.data, uuid = form.uuid.data)

    db.session().add(gameaccount)
    db.session().commit()

    return redirect(url_for("gameaccount_index"))
