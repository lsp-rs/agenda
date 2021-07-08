from flask.globals import session
from app.utils.modal_user_helper import UserHelper
from flask_login import (
    login_user,
    logout_user,
    login_fresh,
    login_required
)
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

user_helper = UserHelper()

@blueprint_default.route("/", methods=("GET", "POST"))
def index():
    if "_id" in session:
        return redirect(url_for("views.home"))

    form = LoginForm()

    context = {
        "form": form,
        "logged": False
    }

    return render_template("/account/index.html", context=context)


@blueprint_default.route("/cadastro", methods=("GET", "POST"))
def account_create():
    if "_id" in session:
        return redirect(url_for("views.home"))

    user_form = UserForm()

    context = {
        "form": user_form,
        "logged": False
    }

    if request.method == "POST":
        print(user_form['birthday'])
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
        user = user_helper.login(email=request.form["email"],password=request.form["password"])

        if user:
            login_user(user)
            return redirect(url_for("views.home"))

    return redirect(url_for("views.index"))


@blueprint_default.route("/logout", methods=("GET",))
@login_required
def logout():
    logout_user()
    return redirect(url_for("views.index"))


@blueprint_default.route("/inicio", methods=("GET", "POST"))
@login_required
def home():
    context = {
        "logged": True
    }
    return render_template("/home/index.html", context=context)


@blueprint_default.route("/agendar", methods=("GET", "POST"))
@login_required
def scheduling():
    form = ScheduleForm()

    context = {
        "form": form,
        "logged": True
    }

    if request.method == "POST":
        return redirect(url_for("views.home"))

    return render_template("/schedule/index.html", context=context)


@blueprint_default.route("/confirmar", methods=("POST",))
@login_required
def schedule_check():
    if request.method == "POST":
        return redirect(url_for("views.home"))
    else:
        return redirect(url_for("views.index"))


@blueprint_default.route("/cancelar", methods=("POST",))
@login_required
def schedule_cancel():
    if request.method == "POST":
        return redirect(url_for("views.home"))
    else:
        return redirect(url_for("views.home"))


@blueprint_default.route("/calendario", methods=("GET", "POST"))
@login_required
def calendar():
    context = {
        "logged": True
    }
    return render_template("/calendar/index.html", context=context)
