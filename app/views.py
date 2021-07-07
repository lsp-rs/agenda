from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for
)
from app.forms import (
    UserForm,
    LoginForm,
    ScheduleForm
)


blueprint_default = Blueprint("views", __name__)

@blueprint_default.route("/", methods=("GET", "POST"))
def index():
    form = LoginForm()
    context = {
        "logged": False,
        "form": form
    }
    return render_template("/account/index.html", context=context)


@blueprint_default.route("/cadastro", methods=("GET", "POST"))
def account_create():
    user_form = UserForm()
    context = {
        "logged": False,
        "form": user_form
    }
    if request.method == "POST":
        from app.utils.modal_user_helper import UserHelper

        user_helper = UserHelper()

        if user_form.validate_on_submit():
            user_helper.new_user(
                full_name=request.form["full_name"],
                birthday=request.form["birthday"],
                email=request.form["email"],
                phone=request.form["phone"],
                password=request.form["password"],
            )
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
    form = ScheduleForm()
    context = {
        "logged": True,
        "form": form
    }
    if request.method == "POST":
        return redirect(url_for("views.home"))
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
        return redirect(url_for("views.home"))
    else:
        return redirect(url_for("views.home"))


@blueprint_default.route("/calendario", methods=("GET", "POST"))
def calendar():
    context = {
        "logged": True
    }
    return render_template("/calendar/index.html", context=context)
