from flask import Flask
from flask_cors import CORS

from py_lib import init_app_logger

from accounting_service.config import config
from accounting_service.db import db, migrate
from accounting_service.user import UserRepo
from accounting_service.task import TaskRepo
from accounting_service.accounting import accounting_api


def create_app():
    app = Flask(config.app_name)
    app.config["SQLALCHEMY_DATABASE_URI"] = config.db_connstring

    app.logger = init_app_logger(config.log_level)

    db.init_app(app)
    migrate.init_app(app, db)

    app.user_repo = UserRepo(db)
    app.task_repo = TaskRepo(db)

    app.register_blueprint(accounting_api)

    @app.route("/ping")
    def ping():
        return "pong"

    CORS(app, supports_credentials=True)

    return app
