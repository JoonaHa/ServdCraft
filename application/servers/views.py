from flask import render_template, request, redirect, url_for
from flask_login import login_required, current_user

from application import app, db
from application.servers.models import Server, Status
from application.auth.models import User
from application.servers.models import Server, Status, GameAccountServer
from application.servers.forms import ServerForm, JoinForm, EditForm
from application.gameAccounts.models import GameAccount


@app.route("/allservers", methods=["GET"])
def server_index():
    if not current_user.is_authenticated:
        return redirect(url_for("auth_login"))
    user = User.query.get(current_user.id)
    if user is None:
        return redirect(url_for("auth_login"))
    else:
        return render_template("servers/list.html", servers=list(Server.query.all()), joined=False, user=user)


@app.route("/joinedservers/", methods=["GET"])
def server_joined():
    if not current_user.is_authenticated:
        return redirect(url_for("auth_login"))
    user = User.query.get(current_user.id)
    if user is None:
        return redirect(url_for("auth_login"))
    else:
        result = db.session.query(Server).filter(
            GameAccount.user_id == user.id).filter(GameAccountServer.game_account_id == GameAccount.id).filter(
                Server.id == GameAccountServer.server_id
        ).all()
        servers = list(result)
        servers.extend(list(Server.query.filter_by(creator_id=user.id)))
        return render_template("servers/list.html", servers=servers, joined=True, user=user)


@login_required
@app.route("/servers/new/", methods=["GET"])
def server_form():
    if not current_user.is_authenticated:
        return redirect(url_for("auth_login"))
    user = User.query.get(current_user.id)
    if user is None:
        return redirect(url_for("auth_login"))
    if not user.isAdmin:
        return redirect(url_for("auth_login"))
    else:
        return render_template("servers/new.html", statuses=Status.__members__.items(), form=ServerForm())


@login_required
@app.route("/server/<server_id>/", methods=["GET"])
def server(server_id):
    if not current_user.is_authenticated:
        return redirect(url_for("auth_login"))
    user = User.query.get(current_user.id)
    if user is None:
        return redirect(url_for("auth_login"))
    else:
        game_accounts = list(user.game_accounts)
        if len(game_accounts) > 0:
            choices = []

            for account in game_accounts:
                if account.gametag is None:
                    choices.append((account.id, account.uuid))
                else:
                    choices.append((account.id, account.gametag))

        form = JoinForm()
        form.accounts.choices = choices
        return render_template("servers/server.html", server=Server.query.get(server_id), accounts=game_accounts, form=form)


@login_required
@app.route("/server/", methods=["POST"])
def server_create():

    if not current_user.is_authenticated:
        return redirect(url_for("auth_login"))
    user = User.query.get(current_user.id)
    if user is None:
        return redirect(url_for("auth_login"))
    if not user.isAdmin:
        return redirect(url_for("auth_login"))

    else:
        form = ServerForm(request.form)
        if not form.validate():
            return render_template("servers/new.html", form=form)
        user = User.query.get(current_user.id)
        server = Server(form.name.data, Status(form.status.data),
                        user, description=form.description.data)

        db.session().add(server)
        db.session().commit()
    server = Server.query.filter_by(name=server.name).first()

    return render_template("servers/server.html", server=server)


@app.route("/servers/<server_id>/join", methods=["POST"])
def server_join(server_id):
    if not current_user.is_authenticated:
        return redirect(url_for("auth_login"))
    user = User.query.get(current_user.id)
    if user is None:
        return redirect(url_for("auth_login"))
    else:
        form = JoinForm(request.form)

    account = GameAccount.query.get(form.accounts.data)
    server = Server.query.get(server_id)

    if account and server and (account.user_id is current_user.id):

        gas = GameAccountServer()
        gas.game_account = account
        server.game_accounts.append(gas)

        db.session().add(gas)
        db.session().commit()
        return redirect (url_for("server_joined"))
    else:
        return redirect(url_for("server, server_id"))


@login_required
@app.route("/server/<server_id>/delete", methods=["POST"])
def server_delete(server_id):

    server = Server.query.get(server_id)
    if server and server.creator_id is current_user.id:

        for gas in list(GameAccountServer.query.filter_by(server_id=server.id)):
            db.session.delete(gas)

        db.session.delete(server)
        db.session().commit()
        return redirect(url_for("server_index"))
    else:
        return


@login_required
@app.route("/server/<server_id>/edit", methods=["GET", "POST"])
def server_update(server_id):
    if not current_user.is_authenticated:
        return redirect(url_for("auth_login"))
    user = User.query.get(current_user.id)
    server = Server.query.get(server_id)
    if user is None or server is None or user.id is not server.creator_id:
        return redirect(url_for("server_index"))
    if request.method == "GET":
        form = EditForm()
        form.status.default = server.status.value
        form.description.default = server.description
        form.process()
        return render_template("servers/edit.html", server=server, form=form)

    if request.method == "POST":
        server = Server.query.get(server_id)
        if server and server.creator_id is current_user.id:

            form = EditForm(request.form)

            server.status = Status(form.status.data)
            server.description = form.description.data
            db.session().commit()
            return redirect(url_for("server_index"))
