from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for
)
import os

blueprint_default = Blueprint("views", __name__)

@blueprint_default.route("/", methods=("GET", "POST"))
def index():
    context = {
        "logged": False
    }
    return render_template("index.html", context=context)


@blueprint_default.route("/cadastro", methods=("GET", "POST"))
def account_create():
    context = {
        "logged": False
    }
    if request.method == "POST":
        return redirect(url_for("views.home"))
    return render_template("account-create.html", context=context)


@blueprint_default.route("/login", methods=("POST",))
def login():
    if request.method == "POST":
        return redirect(url_for("views.home"))
    else:
        return redirect(url_for("views.index"))


@blueprint_default.route("/home", methods=("GET", "POST"))
def home():
    context = {
        "logged": True
    }
    return render_template("home.html", context=context)
