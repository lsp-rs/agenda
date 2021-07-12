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


blueprint_default = Blueprint("views", __name__)

user_helper = UserHelper()

@blueprint_default.route("/", methods=("GET", "POST"))
def index():
    form = LoginForm()

    context = {
        "form": form,
        "logged": False
    }

    if "_id" in session:
        context["logged"] = True
        return redirect(url_for("views.home"))

    return render_template("/account/index.html", context=context)


@blueprint_default.route("/cadastro", methods=("GET", "POST"))
def account_create():
    user_form = UserForm()

    context = {
        "form": user_form,
        "logged": False
    }

    if "_id" in session:
        context["logged"] = True
        return redirect(url_for("views.home"))

    if request.method == "POST":
        print(user_form['birthday'])
        if user_form.validate_on_submit():
            new_user = user_helper.new_user(
                full_name=request.form["full_name"],
                birthday=request.form["birthday"],
                email=request.form["email"],
                phone=request.form["phone"],
                password=request.form["password"],
            )

            user = user_helper.login(email=request.form["email"],password=request.form["password"])

            if user:
                login_user(user)
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
        "logged": True,
        "type_user": "",
    }
    type_user = user_helper.type_user(user_id=session["_user_id"])
    context["type_user"] = type_user

    return render_template("/home/index.html", context=context)


@blueprint_default.route("/agendar", methods=("GET", "POST"))
@login_required
def scheduling():
    form = ""
    type_user = user_helper.type_user(user_id=session["_user_id"])

    if type_user == "establishment_user":
        from .forms import ScheduleFormeEstablishmentUser
        form = ScheduleFormeEstablishmentUser()
    else:
        from .forms import ScheduleFormCommonUser
        form = ScheduleFormCommonUser()

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


@blueprint_default.route("/historico", methods=("POST",))
@login_required
def history():
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
