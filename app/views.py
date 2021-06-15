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
    return render_template("/account/index.html", context=context)


@blueprint_default.route("/cadastro", methods=("GET", "POST"))
def account_create():
    context = {
        "logged": False
    }
    if request.method == "POST":
        return redirect(url_for("views.home"))
    return render_template("/account/account-create.html", context=context)


@blueprint_default.route("/login", methods=("POST",))
def login():
    if request.method == "POST":
        return redirect(url_for("views.home"))
    else:
        return redirect(url_for("views.index"))


@blueprint_default.route("/logout", methods=("GET",))
def logout():
    context = {
        "logged": False
    }
    return redirect(url_for("views.index", context=context))


@blueprint_default.route("/inicio", methods=("GET", "POST"))
def home():
    context = {
        "logged": True
    }
    return render_template("/home/index.html", context=context)


@blueprint_default.route("/agendar", methods=("GET", "POST"))
def scheduling():
    context = {
        "logged": True
    }
    if request.method == "POST":
        return redirect(url_for("views.schedule"))
    return render_template("/schedule/scheduling.html", context=context)


@blueprint_default.route("/horario", methods=("GET", "POST"))
def schedule():
    context = {
        "logged": True
    }
    return render_template("/schedule/index.html", context=context)


@blueprint_default.route("/confirmar", methods=("POST",))
def schedule_check():
    if request.method == "POST":
        return redirect(url_for("views.home"))
    else:
        return redirect(url_for("views.index"))


@blueprint_default.route("/cancelar", methods=("POST",))
def schedule_cancel():
    if request.method == "POST":
        return redirect(url_for("views.schedule"))
    else:
        return redirect(url_for("views.home"))


@blueprint_default.route("/calendario", methods=("GET", "POST"))
def calendar():
    context = {
        "logged": True
    }
    return render_template("/home/calendar.html", context=context)
