from flask import Flask
from flask_cors import CORS

from py_lib import init_app_logger

from user_service.config import config
from user_service.db import db, migrate

from user_service.auth import auth_api
from user_service.user import UserRepo, user_api


def create_app():
    app = Flask(config.app_name)
    app.config["SQLALCHEMY_DATABASE_URI"] = config.db_connstring

    app.logger = init_app_logger(config.log_level)

    db.init_app(app)
    migrate.init_app(app, db)

    app.user_repo = UserRepo(db)

    app.register_blueprint(auth_api)
    app.register_blueprint(user_api)

    @app.route("/ping")
    def ping():
        return "pong"

    CORS(app, supports_credentials=True)

    return app
