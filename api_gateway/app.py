from flask import Flask
from flask_cors import CORS

from py_lib import init_app_logger

import db
import config

# from api import blueprint as auth_api


def create_app():
    app = Flask(config.APP_NAME)

    app.logger = init_app_logger(config.LOG_LEVEL)

    # @app.teardown_appcontext
    # def shutdown_session(exception=None):
    #     db.db_session.remove()

    # configure_settings(app, settings_overrides)

    # app.register_blueprint(auth_api)

    @app.route(f"{config.API_PREFIX}/ping")
    def ping():
        return "pong"

    CORS(app, supports_credentials=True)

    return app
