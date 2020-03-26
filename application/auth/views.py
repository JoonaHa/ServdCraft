from flask import render_template, request, redirect, url_for
from flask_login import login_user, logout_user

from application import app, db
from application.auth.models import User
from application.auth.forms import LoginForm, RegisterForm


@app.route("/auth/login", methods=["GET", "POST"])
def auth_login():
    if request.method == "GET":
        return render_template("auth/loginform.html", form=LoginForm())

    form = LoginForm(request.form)

    # Find by unique username
    user = User.query.filter_by(
        username=form.username.data).first()
    # Check for nonexistent username or wrong password
    if not user or not user.check_password(form.password.data):
        return render_template("auth/loginform.html", form=form, error="No such username or password")

    login_user(user)
    return redirect(url_for("index"))


@app.route("/auth/logout")
def auth_logout():
    logout_user()
    return redirect(url_for("index"))


@app.route("/auth/register", methods=["GET", "POST"])
def auth_register():
    if request.method == "GET":
        return render_template("auth/registerform.html", form=RegisterForm())

    form = RegisterForm(request.form)
    if not form.validate():
        return render_template("auth/registerform.html", form=form)

    # Find if unique username
    user = User.query.filter_by(username=form.username.data).first()

    if user is None:
        user = User(form.name.data, form.username.data, form.password.data)
        db.session().add(user)
        db.session().commit()
        login_user(user)
        return redirect(url_for("index"))
    else:
        return render_template("auth/registerform.html", form=form, error="Username already taken")

