from . import db
from datetime import datetime


class User(db.Model):
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
        db.String(80),
        nullable=False
    )
    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.now()
    )

    def __repr__(self):
        return '<User %r>' % self.full_name


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
        return '<Hour %r>' % self.id


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
        return '<ServiceHours %r>' % self.id


class Establishment(db.Model):
    __tablename__ = "establishment"

    id = db.Column(
        db.Integer,
        primary_key=True
    )
    name = db.Column(
        db.String(80),
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
        db.String(80),
        nullable=False
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
        return '<Establishment %r>' % self.name


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
        db.String(15),
        nullable=False
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
    establishment_id = db.Column(
        db.Integer,
        db.ForeignKey('establishment.id'),
        nullable=False
    )
    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.now()
    )

    def __repr__(self):
        return '<Schedule %r>' % self.date_and_time

