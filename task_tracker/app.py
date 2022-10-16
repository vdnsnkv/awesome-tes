from flask import Flask
from flask_cors import CORS

from py_lib import init_app_logger

from task_tracker.config import config
from task_tracker.db import db, migrate
from task_tracker.user import UserRepo
from task_tracker.task import TaskRepo, task_api


def create_app():
    app = Flask(config.app_name)
    app.config["SQLALCHEMY_DATABASE_URI"] = config.db_connstring

    # app.logger = init_app_logger(config.log_level)

    db.init_app(app)
    migrate.init_app(app, db)

    app.user_repo = UserRepo(db)
    app.task_repo = TaskRepo(db)

    app.register_blueprint(task_api)

    @app.route("/ping")
    def ping():
        return "pong"

    CORS(app, supports_credentials=True)

    return app
