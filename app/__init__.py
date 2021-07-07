from flask import Flask, Blueprint
from flask_session import Session
from config import config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


sess = Session()
db = SQLAlchemy()
migrate = Migrate()

def create_app(config_name, **kwargs):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    sess.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)

    from . import models
    from . import views
    app.register_blueprint(views.blueprint_default, url_prefix='/agenda')

    # Registering static_folder
    static_admin = Blueprint('static_admin', __name__, static_folder='static')
    app.register_blueprint(static_admin, url_prefix='/agenda')

    return app
