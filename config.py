from logging.config import dictConfig
from redis import Redis
from os import getenv


class Config:
    APP_PORT = 5000

    SECRET_KEY = "L0r3W#&#1p5um"

    SESSION_TYPE = 'redis'
    SESSION_REDIS = Redis(host=getenv('REDIS_HOST'), port=getenv('REDIS_PORT'), db=0)

    RESULT_BACKEND = f'redis://{getenv("REDIS_HOST")}:{getenv("REDIS_PORT")}'

    DB_HOST = getenv('DB_HOST')
    DB_BASE = getenv('DB_BASE')
    DB_USER = getenv('DB_USER')
    DB_PASS = getenv('DB_PASS')
    DB_PORT = getenv('DB_PORT')
    SQLALCHEMY_DATABASE_URI = f'mysql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_BASE}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


    dictConfig({
        'version': 1,
        'formatters': {'default': {
            'format': '[%(asctime)s][%(levelname)s]%(message)s',
        }},
        'handlers': {'wsgi': {
            'class': 'logging.StreamHandler',
            'stream': 'ext://flask.logging.wsgi_errors_stream',
            'formatter': 'default'
        }},
        'root': {
            'level': 'DEBUG',
            'handlers': ['wsgi']
        }
    })


class DevelopmentConfig(Config):
    DEBUG = True
    FLASK_DEBUG = 1
    FLASK_ENV = 'development'

    RECEIVERS_EMAIL = [
        'lucas.pereira.244@gmail.com'
    ]


class ProductionConfig(Config):
    DEBUG = False
    FLASK_DEBUG = 0
    FLASK_ENV = 'production'

    RECEIVERS_EMAIL = [
        'lucas.pereira.244@gmail.com'
    ]


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig
}
