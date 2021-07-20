from sqlalchemy.orm import defaultload
from . import db
from datetime import datetime
from flask_login import UserMixin
import enum


class OpenStatus(enum.Enum):
    opened = "opened"
    closed = "closed"


class UserStatus(enum.Enum):
    activated = "activated"
    disabled = "disabled"


class Interval(enum.Enum):
    yes = "yes"
    no = "no"


class ScheduleStatus(enum.Enum):
    not_confirmed = "not_confirmed"
    scheduled = "scheduled"
    concluded = "concluded"
    unscheduled = "unscheduled"


class User(UserMixin, db.Model):
    __tablename__ = "user"

    id = db.Column(
        db.Integer,
        primary_key=True
    )
    full_name = db.Column(
        db.String(80),
        nullable=False
    )
    birthday = db.Column(
        db.DateTime,
        nullable=False
    )
    email = db.Column(
        db.String(120),
        unique=True,
        nullable=False
    )
    phone = db.Column(
        db.String(11),
        unique=True,
        nullable=True
    )
    password = db.Column(
        db.String(100),
        nullable=False
    )
    establishment_id = db.Column(
        db.Integer,
        db.ForeignKey('establishment.id'),
        nullable=True
    )
    status = db.Column(
        db.Enum(UserStatus),
        nullable=True,
        default=UserStatus.activated
    )
    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.now()
    )

    def __repr__(self):
        return self.full_name


class Hour(db.Model):
    __tablename__ = "hour"

    id = db.Column(
        db.Integer,
        primary_key=True
    )
    ini_hour = db.Column(
        db.Time,
        nullable=False,
    )
    end_hour = db.Column(
        db.Time,
        nullable=False,
    )
    interval = db.Column(
        db.Enum(Interval),
        nullable=False,
    )
    interval_hour = db.Column(
        db.Time,
        nullable=False,
    )
    comeback_hour = db.Column(
        db.Time,
        nullable=False,
    )
    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.now()
    )

    def __repr__(self):
        return 'Hour %r' % self.id


class ServiceHours(db.Model):
    __tablename__ = "servicehours"

    id = db.Column(
        db.Integer,
        primary_key=True
    )
    weekdays = db.Column(
        db.String(80),
        nullable=False
    )
    hour_id = db.Column(
        db.Integer,
        db.ForeignKey('hour.id'),
        nullable=False
    )
    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.now()
    )

    def __repr__(self):
        return 'ServiceHours id %r' % self.id


class Establishment(db.Model):
    __tablename__ = "establishment"

    id = db.Column(
        db.Integer,
        primary_key=True
    )
    open_status = db.Column(
        db.Enum(OpenStatus),
        nullable=True,
        default=OpenStatus.opened
    )
    servicehours_id = db.Column(
        db.Integer,
        db.ForeignKey('servicehours.id'),
        nullable=False
    )
    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.now()
    )

    def __repr__(self):
        return 'Establishment id %r' % self.id


class Schedule(db.Model):
    __tablename__ = "schedule"

    id = db.Column(
        db.Integer,
        primary_key=True
    )
    date_and_time = db.Column(
        db.DateTime,
        nullable=False
    )
    status = db.Column(
        db.Enum(ScheduleStatus),
        nullable=False,
        default=ScheduleStatus.not_confirmed
    )
    note = db.Column(
        db.Text,
        nullable=False
    )
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('user.id'),
        nullable=False
    )
    user_establishment_id = db.Column(
        db.Integer,
        db.ForeignKey('user.id'),
        nullable=False
    )
    created_by = db.Column(
        db.Integer,
        db.ForeignKey('user.id'),
        nullable=False
    )
    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.now()
    )

    def __repr__(self):
        return 'Schedule %r' % self.date_and_time

