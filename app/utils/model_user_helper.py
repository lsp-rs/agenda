from datetime import datetime, timedelta
from .model_schedule_helper import ScheduleHelper
from .local_debug import debug
from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)
from app.models import (
    Schedule,
    User,
    UserStatus,
    db
)
from sqlalchemy import and_


class UserHelper():

    STATUS = {
        "not_confirmed" : "Pendente de Confirmação",
        "scheduled" : "Agendado",
        "concluded" : "Concluido",
        "unscheduled" : "Cancelado"
    }

    def new_user(self, **kwargs):
        birthday = datetime.strptime(kwargs["birthday"], '%d/%m/%Y')
        password = generate_password_hash(
            kwargs["password"],
            method='sha256'
        )
        new_user = User(
            full_name=kwargs["full_name"],
            birthday=birthday,
            email=kwargs["email"],
            phone=kwargs["phone"],
            password=password,
        )
        db.session.add(new_user)
        db.session.commit()
        return new_user

    def login(self, **kwargs):
        user = User.query.filter_by(
            email=kwargs["email"],
            status=UserStatus.activated
        ).first()

        if (
            not user or not
            check_password_hash(user.password, kwargs["password"])
        ):
            return False
        return user

    def type_user(self, **kwargs):
        user = User.query.filter_by(id=kwargs["user_id"]).first()

        if user.establishment_id:
            return "establishment_user"
        return "common_user"

    def user_scheduling(self, **kwargs):
        schedule_helper = ScheduleHelper()

        date_schedule = datetime.strptime(kwargs["date"], '%d/%m/%Y').date()
        time_schedule = datetime.strptime(kwargs["time"], '%H:%M').time()
        date_and_time = datetime.combine(date_schedule, time_schedule)
        common_user_id = kwargs["common_user_id"]
        establishment_user_id = ""
        if "establishment_user_id" in kwargs:
            establishment_user_id = kwargs["establishment_user_id"]
        else:
            establishment_user = User.query.filter_by(
                establishment_id=1
            ).first()
            establishment_user_id = establishment_user.id

        scheduling_pending = Schedule.query.filter(
            and_(
                Schedule.user_id == common_user_id,
                Schedule.status.in_(
                    [
                        "not_confirmed",
                        "scheduled"
                    ]
                )
            )
        ).all()

        schedules_of_date = Schedule.query.with_entities(
            Schedule.date_and_time
        ).filter(
            and_(
                Schedule.date_and_time.like(f"%{date_and_time.date()}%"),
                Schedule.status.in_(
                    [
                        "not_confirmed",
                        "scheduled"
                    ]
                )
            )
        ).all()

        scheduling_of_date = True

        for schedule_date_time in schedules_of_date:
            verify = (
                not date_and_time < schedule_date_time.date_and_time - timedelta(minutes=45) and
                not date_and_time > schedule_date_time.date_and_time + timedelta(minutes=45)
            )
            if verify:
                scheduling_of_date = False

        if len(scheduling_pending) == 0:
            if (
                scheduling_of_date and
                date_and_time > datetime.now() + timedelta(hours=1) and
                date_and_time < datetime.now() + timedelta(days=45) and
                schedule_helper.service_hour_verify(
                    establishment_user_id,
                    {
                        "weekday" : str(date_and_time.date().weekday()),
                        "hour" : date_and_time.time()
                    }
                )
            ):
                new_schedule = Schedule(
                    date_and_time = date_and_time,
                    user_id = common_user_id,
                    user_establishment_id = establishment_user_id,
                    note = kwargs["note"]
                )
                db.session.add(new_schedule)
                db.session.commit()

                return True

        return False


    def view_schedule(self, **kwargs):
        schedule_data = []

        if kwargs["type_user"] == "establishment_user":
            result_schedules = Schedule.query.with_entities(
                User.id,
                User.full_name,
                Schedule.date_and_time,
                Schedule.status
            ).outerjoin(
                User,
                User.id == Schedule.user_id
            ).filter(
                and_(
                    Schedule.status.in_(
                        [
                            "not_confirmed",
                            "scheduled",
                        ]
                    ),
                    Schedule.date_and_time > datetime.now()
                )
            ).order_by(
                Schedule.created_at
            ).limit(
                10
            ).all()

            debug(f"E = {result_schedules}")

            for schedule in result_schedules:
                schedule_data.append(
                    {
                        "user_id" : schedule.id,
                        "full_name" : schedule.full_name,
                        "date" : schedule.date_and_time.strftime("%d/%m/%Y"),
                        "hour" : schedule.date_and_time.strftime("%H:%M:%S"),
                        "status" : self.STATUS[schedule.status.value],
                    }
                )

        else:
            result_schedules = Schedule.query.with_entities(
                Schedule.date_and_time,
                Schedule.note,
                Schedule.status
            ).outerjoin(
                User,
                User.id == Schedule.user_id
            ).filter(
                Schedule.user_id == kwargs["user_id"]
            ).order_by(
                Schedule.created_at
            ).first()

            if result_schedules:
                schedule_data.append(
                    {
                        "status" : self.STATUS[result_schedules.status.value],
                        "date" : result_schedules.date_and_time.strftime("%d/%m/%Y"),
                        "hour" : result_schedules.date_and_time.strftime("%H:%M:%S"),
                        "note" : result_schedules.note
                    }
                )

        return schedule_data



    def history_schedule(self, **kwargs):
        schedule_data = []

        if kwargs["type_user"] == "establishment_user":
            result_schedules = Schedule.query.with_entities(
                User.id,
                User.full_name,
                Schedule.date_and_time,
                Schedule.status
            ).outerjoin(
                User,
                User.id == Schedule.user_id
            ).filter(
                and_(
                    Schedule.status.in_(
                        [
                            "not_confirmed",
                            "scheduled",
                            "concluded",
                            "unscheduled"
                        ]
                    )
                )
            ).order_by(
                Schedule.created_at
            ).limit(
                10
            ).all()

            for schedule in result_schedules:
                schedule_data.append(
                    {
                        "user_id" : schedule.id,
                        "full_name" : schedule.full_name,
                        "date" : schedule.date_and_time.strftime("%d/%m/%Y"),
                        "hour" : schedule.date_and_time.strftime("%H:%M:%S"),
                        "status" : self.STATUS[schedule.status.value],
                    }
                )

        return schedule_data


    def scheduled_schedule(self, **kwargs):
        schedule_data = []

        if kwargs["type_user"] == "establishment_user":
            result_schedules = Schedule.query.with_entities(
                User.id,
                User.full_name,
                Schedule.date_and_time
            ).outerjoin(
                User,
                User.id == Schedule.user_id
            ).filter(
                Schedule.status == "scheduled"
            ).order_by(
                Schedule.created_at
            ).limit(
                10
            ).all()

            for schedule in result_schedules:
                schedule_data.append(
                    {
                        "user_id" : schedule.id,
                        "full_name" : schedule.full_name,
                        "date" : schedule.date_and_time.strftime("%d/%m/%Y"),
                        "hour" : schedule.date_and_time.strftime("%H:%M:%S"),
                    }
                )

        else:
            result_schedules = Schedule.query.with_entities(
                Schedule.date_and_time,
                Schedule.note,
                Schedule.status
            ).outerjoin(
                User,
                User.id == Schedule.user_id
            ).filter(
                and_(
                    Schedule.user_id == kwargs["user_id"],
                    Schedule.status == "scheduled"
                )
            ).order_by(
                Schedule.created_at
            ).first()

            debug(f"C = {result_schedules}")

            if result_schedules:
                schedule_data.append(
                    {
                        "user_id" : result_schedules.id,
                        "date" : result_schedules.date_and_time.strftime("%d/%m/%Y"),
                        "hora" : result_schedules.date_and_time.strftime("%H:%M:%S"),
                        "nota" : result_schedules.note
                    }
                )

        return schedule_data


    def not_confirmed_schedule(self, **kwargs):
        schedule_data = []

        if kwargs["type_user"] == "establishment_user":
            result_schedules = Schedule.query.with_entities(
                User.id,
                User.full_name,
                Schedule.date_and_time,
            ).outerjoin(
                User,
                User.id == Schedule.user_id
            ).filter(
                and_(
                    Schedule.user_establishment_id == kwargs["user_id"],
                    Schedule.status.in_(
                        [
                            "not_confirmed",
                        ]
                    )
                )
            ).order_by(
                Schedule.created_at
            ).limit(
                10
            ).all()

            for schedule in result_schedules:
                schedule_data.append(
                    {
                        "user_id" : schedule.id,
                        "full_name" : schedule.full_name,
                        "date" : schedule.date_and_time.strftime("%d/%m/%Y"),
                        "hour" : schedule.date_and_time.strftime("%H:%M:%S"),
                    }
                )

        else:
            result_schedules = Schedule.query.with_entities(
                User.id,
                Schedule.date_and_time,
                Schedule.note,
            ).outerjoin(
                User,
                User.id == Schedule.user_id
            ).filter(
                and_(
                    Schedule.user_id == kwargs["user_id"],
                    Schedule.status.in_(
                        [
                            "not_confirmed",
                        ]
                    )
                )
            ).order_by(
                Schedule.created_at
            ).first()

            if result_schedules:
                schedule_data.append(
                    {
                        "user_id" : result_schedules.id,
                        "date" : result_schedules.date_and_time.strftime("%d/%m/%Y"),
                        "hora" : result_schedules.date_and_time.strftime("%H:%M:%S"),
                        "nota" : result_schedules.note
                    }
                )

        return schedule_data


    def scheduling_confirmation(self, **kwargs):
        if "user_id" in kwargs:
            debug(kwargs["user_id"])
            schedule = Schedule.query.filter(
                and_(
                    Schedule.user_id == kwargs["user_id"],
                    Schedule.status == "not_confirmed"
                )
            ).first()
            schedule.status = "scheduled"
            db.session.commit()

        return


    def scheduling_cancelation(self, **kwargs):
        if "user_id" in kwargs:
            debug(kwargs["user_id"])
            schedule = Schedule.query.filter(
                and_(
                    Schedule.user_id == kwargs["user_id"],
                    Schedule.status == "scheduled"
                )
            ).first()
            schedule.status = "unscheduled"
            db.session.commit()

        return
