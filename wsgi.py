from app import create_app
from os import getenv


app = create_app(getenv('FLASK_ENV'))

if __name__ == '__main__':
    host = '0.0.0.0'
    debug = app.config['DEBUG']
    port = app.config['APP_PORT']

    app.run(
        host=host, debug=debug, port=port, use_reloader=debug
    )
