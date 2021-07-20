from flask import session
from app.utils.model_user_helper import UserHelper
from app.utils.model_schedule_helper import ScheduleHelper
from flask_login import (
    login_user,
    logout_user,
    login_required
)
from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    jsonify,
    flash,
    url_for
)
import json


blueprint_default = Blueprint("views", __name__)

user_helper = UserHelper()
schedule_helper = ScheduleHelper()

@blueprint_default.route("/", methods=("GET", "POST"))
def index():
    from .forms import LoginForm
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
    from .forms import UserForm
    user_form = UserForm()

    context = {
        "form": user_form,
        "logged": False
    }

    if "_id" in session:
        context["logged"] = True
        return redirect(url_for("views.home"))

    if request.method == "POST":
        if user_form.validate_on_submit():
            user_helper.new_user(
                full_name=request.form["full_name"],
                birthday=request.form["birthday"],
                email=request.form["email"],
                phone=request.form["phone"],
                password=request.form["password"],
            )

            user = user_helper.login(
                email=request.form["email"],
                password=request.form["password"]
            )

            if user:
                login_user(user)
                flash('Conta criada com sucesso!', 'success')
                return redirect(url_for("views.home"))

    return render_template("/account/account-create.html", context=context)


@blueprint_default.route("/login", methods=("POST",))
def login():
    from .forms import LoginForm
    user_form = LoginForm()

    if request.method == "POST":
        if user_form.validate_on_submit():
            user = user_helper.login(
                email=request.form["email"],
                password=request.form["password"]
            )

            if user:
                login_user(user)
                flash('Login efetuado com sucesso!', 'info')
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
        "user_id": session["_user_id"],
        "view_schedule": [],
        "not_confirmed": [],
        "scheduled": [],
        "history": [],
    }
    type_user = user_helper.type_user(
        user_id=session["_user_id"]
    )
    context["type_user"] = type_user
    context["view_schedule"] = user_helper.view_schedule(
        user_id = session["_user_id"],
        type_user = type_user
    )
    context["not_confirmed"] = user_helper.not_confirmed_schedule(
        user_id = session["_user_id"],
        type_user = type_user
    )
    context["scheduled"] = user_helper.scheduled_schedule(
        user_id = session["_user_id"],
        type_user = type_user
    )
    context["history"] = user_helper.history_schedule(
        user_id = session["_user_id"],
        type_user = type_user
    )

    return render_template("/home/index.html", context=context)


@blueprint_default.route("/agendar", methods=("GET", "POST"))
@login_required
def scheduling(date_calendar=None):
    form_schedule = ""
    type_user = user_helper.type_user(user_id=session["_user_id"])
    hour_schedule = schedule_helper.hour_of_schedule()

    if type_user == "establishment_user":
        from .forms import ScheduleFormeEstablishmentUser
        form_schedule = ScheduleFormeEstablishmentUser()
    else:
        from .forms import ScheduleFormCommonUser
        form_schedule = ScheduleFormCommonUser()

    context = {
        "form": form_schedule,
        "logged": True,
        "hour_schedule": hour_schedule
    }

    if request.method == "POST":
        if form_schedule.validate_on_submit():
            if type_user == "establishment_user":
                schedule = user_helper.user_scheduling(
                    date=request.form["date"],
                    time=request.form["time"],
                    common_user_id=request.form["user"],
                    establishment_user_id=session["_user_id"],
                    note=request.form["note"],
                )
            else:
                schedule = user_helper.user_scheduling(
                    date=request.form["date"],
                    time=request.form["time"],
                    common_user_id=session["_user_id"],
                    note=request.form["note"],
                )

            if schedule:
                flash(
                    'Agendamento enviado com sucesso! Pendente de confirmação.',
                    'info'
                )
            else:
                if type_user == "establishment_user":
                    flash(
                        (
                            'Não foi possível agendar. '
                            'Cliente já possui um agendamento '
                            'pendente ou date e hora indisponível.'
                        ),
                        'warning'
                    )
                else:
                    flash(
                        (
                            'Não foi possível agendar. '
                            'Agendamento pendente ou '
                            'data e hora indisponível'
                        ),
                        'warning'
                    )
            return redirect(url_for("views.home"))

    return render_template(
        "/schedule/index.html",
        context=context,
        date_calendar=date_calendar
    )


@blueprint_default.route("/confirmar", methods=("GET","POST"))
@login_required
def schedule_check():
    context = {
        "logged": True,
        "type_user" : "",
        "not_confirmed": [],
    }
    type_user = user_helper.type_user(
        user_id=session["_user_id"]
    )
    context["type_user"] = type_user

    if request.method == "POST":
        user_helper.scheduling_confirmation(user_id=request.form["user_id"])

    context["not_confirmed"] = user_helper.not_confirmed_schedule(
        user_id = session["_user_id"],
        type_user = type_user
    )

    if not context["not_confirmed"]:
        return redirect(url_for("views.home"))

    return render_template("/home/schedule-check.html", context=context)


@blueprint_default.route("/cancelar", methods=("GET", "POST"))
@login_required
def schedule_cancel():
    context = {
        "logged": True,
        "type_user" : "",
        "scheduled": [],
    }
    type_user = user_helper.type_user(
        user_id=session["_user_id"]
    )
    context["type_user"] = type_user

    if request.method == "POST":
        user_helper.scheduling_cancelation(user_id=request.form["user_id"])

    context["scheduled"] = user_helper.scheduled_schedule(
        user_id = session["_user_id"],
        type_user = type_user
    )

    if not context["scheduled"]:
        return redirect(url_for("views.home"))

    return render_template("/home/schedule-cancel.html", context=context)


@blueprint_default.route("/visualizar", methods=("GET", "POST"))
@login_required
def schedule_view():
    context = {
        "logged": True,
        "type_user" : "",
        "view_schedule": [],
    }
    type_user = user_helper.type_user(
        user_id=session["_user_id"]
    )
    context["type_user"] = type_user

    context["view_schedule"] = user_helper.view_schedule(
        user_id = session["_user_id"],
        type_user = type_user
    )

    if not context["view_schedule"]:
        return redirect(url_for("views.home"))

    return render_template("/home/schedule-view.html", context=context)


@blueprint_default.route("/historico", methods=("GET","POST"))
@login_required
def history():
    context = {
        "logged": True,
        "type_user" : "",
        "history": [],
    }
    type_user = user_helper.type_user(
        user_id=session["_user_id"]
    )
    context["type_user"] = type_user

    context["history"] = user_helper.history_schedule(
        user_id = session["_user_id"],
        type_user = type_user
    )

    if not context["history"]:
        return redirect(url_for("views.home"))

    return render_template("/home/schedule-history.html", context=context)

@blueprint_default.route("/calendario", methods=("GET", "POST"))
@login_required
def calendar():
    context = {
        "logged" : True,
    }

    calendar_level = schedule_helper.schedules_day_level()

    levels = []

    for key, item in calendar_level.items():
        levels.append((key, item))

    return render_template(
        "/calendar/index.html",
        context=context,
        levels=json.dumps(levels)
    )


@blueprint_default.route("/calendario/detalhes", methods=("POST",))
@login_required
def calendar_detail():
    context = {
        "logged": True,
        "schedules": {},
        "date_picked" : ""
    }
    if request.method == "POST":
        if "date-picked" in request.form:
            date_picked = request.form["date-picked"]
            context["date_picked"] = date_picked

            if date_picked:
                calendar_info = schedule_helper.calendar_schedules(
                    date=date_picked
                )
            else:
                calendar_info = schedule_helper.calendar_schedules()

            context["schedules"] = calendar_info
    return render_template("/calendar/detail.html", context=context)
