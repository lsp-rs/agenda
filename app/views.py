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
    return render_template("home.html", context=context)


@blueprint_default.route("/agendar", methods=("GET", "POST"))
def scheduling():
    context = {
        "logged": True
    }
    if request.method == "POST":
        return redirect(url_for("views.schedule"))
    return render_template("scheduling.html", context=context)



@blueprint_default.route("/reagendar", methods=("GET", "POST"))
def reschedule():
    context = {
        "logged": True
    }
    if request.method == "POST":
        return redirect(url_for("views.schedule"))
    return render_template("reschedule.html", context=context)


@blueprint_default.route("/horario", methods=("GET", "POST"))
def schedule():
    context = {
        "logged": True
    }
    return render_template("schedule.html", context=context)


@blueprint_default.route("/calendario", methods=("GET", "POST"))
def calendar():
    context = {
        "logged": True
    }
    return render_template("calendar.html", context=context)


@blueprint_default.route("/historico", methods=("GET", "POST"))
def history():
    context = {
        "logged": True
    }
    return render_template("history.html", context=context)


@blueprint_default.route("/visualizar", methods=("GET",))
def view_schedule():
    context = {
        "logged": True
    }
    return render_template("view-schedule.html", context=context)


@blueprint_default.route("/confirmar", methods=("GET",))
def check_schedule():
    context = {
        "logged": True
    }
    return render_template("check-schedule.html", context=context)


@blueprint_default.route("/cancelar", methods=("GET",))
def cancel_schedule():
    context = {
        "logged": True
    }
    return render_template("cancel-schedule.html", context=context)
