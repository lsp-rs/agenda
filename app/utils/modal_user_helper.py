from datetime import datetime
from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)
from app.models import (
    User,
    UserStatus,
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
        return new_user

    def login(self, **kwargs):
        user = User.query.filter_by(email=kwargs["email"],status=UserStatus.activated).first()

        if not user or not check_password_hash(user.password, kwargs["password"]):
            return False
        return user

    def type_user(self, **kwargs):
        user = User.query.filter_by(id=kwargs["user_id"]).first()

        if user.establishment_id:
            return "establishment_user"
        return "common_user"
