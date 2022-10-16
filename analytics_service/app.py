from flask import Flask
from flask_cors import CORS

from py_lib import init_app_logger

from analytics_service.config import config
from analytics_service.db import db, migrate
from analytics_service.user import UserRepo
from analytics_service.task import TaskRepo
from analytics_service.transaction import TransactionRepo

from analytics_service.api import blueprint as analytics_api


def create_app():
    app = Flask(config.app_name)
    app.config["SQLALCHEMY_DATABASE_URI"] = config.db_connstring

    # app.logger = init_app_logger(config.log_level)

    db.init_app(app)
    migrate.init_app(app, db)

    app.user_repo = UserRepo(db)
    app.task_repo = TaskRepo(db)
    app.transation_repo = TransactionRepo(db)

    app.register_blueprint(analytics_api)

    @app.route("/ping")
    def ping():
        return "pong"

    CORS(app, supports_credentials=True)

    return app
