from flask import render_template, request, redirect, url_for
from flask_login import login_required, current_user

from application import app, db
from application.gameAccounts.models import GameAccount
from application.auth.models import User
from application.gameAccounts.forms import GameAccountForm


@login_required
@app.route("/game_accounts", methods=["GET"])
def gameaccount_index():
    if not current_user.is_authenticated:
        return redirect(url_for("auth_login"))
    user=User.query.get(current_user.id)
    if user is None:
        return redirect(url_for("auth_login"))
    else:    
        return render_template("gameAccount/list.html", gameaccounts=GameAccount.query.filter_by(user_id=current_user.id))


@login_required
@app.route("/game_accounts/new/", methods=["GET"])
def gameaccount_form():
    return render_template("gameAccount/new.html", form=GameAccountForm())

@login_required
@app.route("/game_accounts/<account_id>/", methods=["GET"])
def gameaccount_updateform(account_id):

    account=GameAccount.query.get(account_id)

    if account and account.user_id is current_user.id:
        return render_template("gameAccount/account.html", account=account)
    else:
        return redirect(url_for("index"))



@login_required
@app.route("/game_accounts/<account_id>/", methods=["POST"])
def gameaccount_update(account_id):

    account=GameAccount.query.get(account_id)
    if account and account.user_id is current_user.id:

        account.gametag=request.form.get("gametag")
        account.uuid=request.form.get("uuid")
        db.session().commit()
        return redirect(url_for("gameaccount_index"))
    else:
        return


@login_required
@app.route("/game_account/", methods=["POST"])
def gameaccount_create():

    form=GameAccountForm(request.form)

    if not form.validate():
        return render_template("gameAccount/new.html", form=form)

    user=User.query.get(current_user.get_id())

    gameaccount=GameAccount(
        user, gametag=form.gametag.data, uuid=form.uuid.data)

    db.session().add(gameaccount)
    db.session().commit()
    gameaccount=GameAccount.query.filter_by(gametag=gameaccount.gametag, uuid = gameaccount.uuid).first()

    return render_template("gameAccount/account.html", account=gameaccount)
