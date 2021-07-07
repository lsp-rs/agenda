from re import I
from flask_wtf import FlaskForm
from wtforms import (
    DateField,
    TimeField,
    StringField,
    PasswordField,
    TextAreaField
)
from wtforms.fields.html5 import (
    EmailField,
    TelField
)
from wtforms.validators import (
    InputRequired,
    DataRequired,
    EqualTo,
    length
)


class LoginForm(FlaskForm):
    email = EmailField(
        "E-mail",
        validators=[
            length(max=120),
            DataRequired()
        ],
        render_kw={
            "class":"form-control"
        }
    )
    password = PasswordField(
        "Senha",
        validators=[
            length(max=80),
            InputRequired(),
            EqualTo(
                "confirm_pass",
                message="As senhas devem corresponder."
            )
        ],
        render_kw={
            "class":"form-control"
        }
    )


class UserForm(FlaskForm):
    full_name = StringField(
        "Nome Completo",
        validators=[
            length(max=80),
            DataRequired()
        ],
        render_kw={
            "class":"form-control"
        }
    )
    birthday = DateField(
        "Data de Nascimento",
        validators=[
            DataRequired()
        ],
        render_kw={
            "class":"form-control"
        },
        format='%d-%m-%Y'
    )
    email = EmailField(
        "E-mail",
        validators=[
            length(max=120),
            DataRequired()
        ],
        render_kw={
            "class":"form-control"
        }
    )
    phone = TelField(
        "Telefone/Celular",
        validators=[
            length(max=11),
            DataRequired()
        ],
        render_kw={
            "class":"form-control"
        }
    )
    password = PasswordField(
        "Senha",
        validators=[
            length(max=80),
            InputRequired(),
            EqualTo(
                "confirm_pass",
                message="As senhas devem corresponder."
            )
        ],
        render_kw={
            "class":"form-control"
        }
    )
    confirm_pass = PasswordField(
        "Repita a Senha",
        render_kw={
            "class":"form-control"
        }
    )


class ScheduleForm(FlaskForm):
    date = DateField(
        "Data de Agendamento",
        validators=[
            DataRequired()
        ],
        format="%d/%m/%Y",
        render_kw={
            "class":"form-control"
        }
    )
    time = TimeField(
        "Horario de Agendamento",
        validators=[
            DataRequired()
        ],
        format="%H:%M",
        render_kw={
            "class":"form-control"
        }
    )
    note = TextAreaField(
        "Observações",
        validators=[
            length(max=250),
            DataRequired()
        ],
        render_kw={
            "class":"form-control"
        }
    )
