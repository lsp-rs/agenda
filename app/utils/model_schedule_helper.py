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
        print("ScheduleHelper.service_hour() :: OK")
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
        print("ScheduleHelper.service_hour_verify() :: OK")
        service_hour = self.service_hour(establishment_user)
        if (
            hour_verify["weekday"] in service_hour["weekdays"] and
            hour_verify["hour"] > service_hour["ini_hour"] and
            hour_verify["hour"] < service_hour["end_hour"]
        ):
            print("ScheduleHelper.service_hour_verify().if#1 :: OK")

            if service_hour["interval"] == Interval.yes:
                print("ScheduleHelper.service_hour_verify().if#2 :: OK")
                if(
                    hour_verify["hour"] < service_hour["interval_hour"] and
                    hour_verify["hour"] > service_hour["comeback_hour"]
                ):
                    print("ScheduleHelper.service_hour_verify().if#3 :: OK")
                    return True
            else:
                print("ScheduleHelper.service_hour_verify().else#1 :: OK")
                return True
        print("ScheduleHelper.service_hour_verify().FalseAll :: OK")
        return False


    def calendar_schedules(self, **kwargs):
        schedule_data = {
            "hour_main" : {}
        }

        result_schedules = Schedule.query.with_entities(
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
                        "scheduled",
                    ]
                ),
                Schedule.date_and_time == kwargs["date"]
            )
        ).order_by(
            Schedule.date_and_time
        ).all()

        for schedule in result_schedules:
            schedule_data[
                "hour_main"
            ][
                f"{schedule.date_and_time.strftime('%H')}"
            ].append(
                {
                    "name" : schedule.full_name,
                    "hour" : schedule.date_and_time.strftime("%H:%M")
                }
            )

        print(schedule_data)
