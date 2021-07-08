from datetime import datetime
from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)
from app.models import (
    User,
    db
)


class UserHelper():

    def new_user(self, **kwargs):
        birthday = datetime.strptime(kwargs["birthday"], '%d/%m/%Y')
        password = generate_password_hash(kwargs["password"], method='sha256')
        new_user = User(
            full_name=kwargs["full_name"],
            birthday=birthday,
            email=kwargs["email"],
            phone=kwargs["phone"],
            password=password,
        )
        db.session.add(new_user)
        db.session.commit()

    def login(self, **kwargs):
        user = User.query.filter_by(email=kwargs["email"]).first()

        if not user or not check_password_hash(user.password, kwargs["password"]):
            return False
        return user
