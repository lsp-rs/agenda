# from datetime import datetime
from app.models import (
    User,
    db
)


class UserHelper():

    user_attr = {
        "full_name" : str(),
        "birthday" : str(),
        "email" : str(),
        "phone" : str(),
        "password" : str(),
    }

    def new_user(self, **kwargs):
        if kwargs.keys() == self.user_attr.keys():
            new_user = User(
                full_name=kwargs["full_name"],
                birthday=kwargs["birthday"],
                email=kwargs["email"],
                phone=kwargs["phone"],
                password=kwargs["password"],
            )
            db.session.add(new_user)
            db.session.commit()

