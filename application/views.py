from flask import render_template, request, redirect, url_for
from application import app, db
from application.models import User, GameAccount


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/game_accounts", methods=["GET"])
def gameaccount_index():
    return render_template("gameaccount/list.html", gameaccounts=GameAccount.query.all())


@app.route("/game_accounts/new/")
def gameaccount_form():
    return render_template("gameaccount/new.html")


@app.route("/game_accounts/<account_id>/", methods=["GET"])
def gameaccount_updateform(account_id):

    return render_template("gameaccount/account.html", account = GameAccount.query.get(account_id))


@app.route("/game_accounts/<account_id>/", methods=["POST"])
def gameaccount_update(account_id):

    account = GameAccount.query.get(account_id)
    account.gametag = request.form.get("gametag")
    account.uuid = request.form.get("uuid")
    db.session().commit()


@app.route("/game_account/", methods=["POST"])
def gameaccount_create():

    user = User.query.filter_by(username ="anonymous").first()
    if user is None:
        user = User("anonymous", "anonymous", "test@example.com", password="1234")
        db.session().add(user)

    gameaccount = GameAccount(user, gametag= request.form.get("gametag"), uuid = request.form.get("uuid"))

    db.session().add(gameaccount)
    db.session().commit()

    return redirect(url_for("gameaccount_index"))
