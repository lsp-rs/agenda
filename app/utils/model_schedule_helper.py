from datetime import datetime
from app.models import (
    Establishment,
    User,
    Hour,
    Interval,
    Schedule,
    ServiceHours
)
from sqlalchemy import and_


class ScheduleHelper():

    def service_hour(self, establishment_user):
        return ServiceHours.query.with_entities(
            ServiceHours.weekdays,
            Hour.ini_hour,
            Hour.end_hour,
            Hour.interval,
            Hour.interval_hour,
            Hour.comeback_hour
        ).outerjoin(
            Hour, Hour.id == ServiceHours.hour_id
        ).outerjoin(
            Establishment, Establishment.servicehours_id == ServiceHours.id
        ).filter(
            User.id == establishment_user
        ).first()


    def service_hour_verify(self, establishment_user, hour_verify):
        service_hour = self.service_hour(establishment_user)

        if (
            hour_verify["weekday"] in service_hour["weekdays"] and
            hour_verify["hour"] > service_hour["ini_hour"] and
            hour_verify["hour"] < service_hour["end_hour"]
        ):
            if service_hour["interval"] == Interval.yes:
                if(
                    hour_verify["hour"] < service_hour["interval_hour"] and
                    hour_verify["hour"] > service_hour["comeback_hour"]
                ):
                    return True
            else:
                return True

        return False


    def calendar_schedules(self, **kwargs):
        schedule_data = {
            "hour_main" : {}
        }

        if "date" in kwargs:
            date_filter  = datetime.strptime(kwargs["date"], '%d/%m/%Y')
        else:
            date_filter = datetime.today()

        result_schedules = Schedule.query.with_entities(
            User.id,
            User.full_name,
            Schedule.date_and_time,
        ).outerjoin(
            User,
            User.id == Schedule.user_id
        ).filter(
            and_(
                Schedule.status.in_(
                    [
                        "scheduled",
                        "not_confirmed"
                    ]
                ),
                Schedule.date_and_time.like(f"%{date_filter.date()}%")
            )
        ).order_by(
            Schedule.date_and_time
        ).all()

        schedule_data["hour_main"] = {}
        list_schedules = []

        hour_aux = ""

        for schedule in result_schedules:

            hour_aux = schedule.date_and_time.strftime('%H')

            if hour_aux == schedule.date_and_time.strftime('%H'):
                list_schedules.append(
                    {
                        "name" : schedule.id,
                        "name" : schedule.full_name,
                        "hour" : schedule.date_and_time.strftime("%H:%M")
                    }
                )
            else:
                list_schedules = []
                list_schedules.append(
                    {
                        "name" : schedule.id,
                        "name" : schedule.full_name,
                        "hour" : schedule.date_and_time.strftime("%H:%M")
                    }
                )

            schedule_data[
                "hour_main"
            ][
                f"{schedule.date_and_time.strftime('%H')}"
            ] = list_schedules

        return schedule_data
