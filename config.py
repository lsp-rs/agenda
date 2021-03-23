from logging.config import dictConfig
from redis import Redis
from os import getenv


class Config:
    APP_PORT = 5000

    SESSION_TYPE = 'redis'
    SESSION_REDIS = Redis(host=getenv('REDIS_HOST'), port=getenv('REDIS_PORT'), db=0)

    RESULT_BACKEND = f'redis://{getenv("REDIS_HOST")}:{getenv("REDIS_PORT")}'


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
