from flask import Flask, Blueprint
from flask_session import Session
from config import config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager


sess = Session()
db = SQLAlchemy()
migrate = Migrate()

def create_app(config_name, **kwargs):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    sess.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)

    login_manager = LoginManager()
    login_manager.login_view = 'views.index'
    login_manager.init_app(app)

    from . import models

    @login_manager.user_loader
    def load_user(user):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return models.User.query.get(int(user))

    from . import views

    app.register_blueprint(views.blueprint_default, url_prefix='/agenda')

    # Registering static_folder
    static_admin = Blueprint('static_admin', __name__, static_folder='static')
    app.register_blueprint(static_admin, url_prefix='/agenda')

    return app
