from flask import render_template, request, redirect, url_for
from flask_login import login_required, current_user

from application import app, db
from application.servers.models import Server
from application.auth.models import User
from application.servers.forms import ServerForm


@app.route("/servers", methods=["GET"])
def server_index():
    return render_template("servers/list.html", servers=Server.query.all())


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
        return render_template("servers/new.html", form=ServerForm())


@login_required
@app.route("/server/<server_id>/", methods=["GET"])
def server(server_id):
    return render_template("servers/server.html", server=Server.query.get(server_id))


@login_required
@app.route("/servers/", methods=["POST"])
def server_create():

    if not current_user.is_authenticated:
        return redirect(url_for("auth_login"))
    user = User.query.get(current_user.id)
    if user is None:
        return redirect(url_for("auth_login"))
    if not user.isAdmin:
        return redirect(url_for("auth_login"))
    else:
        #TODO Finih server creation 
        return redirect(url_for("auth_login"))
