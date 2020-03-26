from flask import render_template, request, redirect, url_for
from application import app, db



@app.route("/")
def index():
    return redirect(url_for("gameaccount_index"))
