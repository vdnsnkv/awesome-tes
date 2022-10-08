from flask import request, Response, jsonify, Blueprint

from user_service.config import config
from user_service.token import get_user_jwt_token
from user_service.password import check_password
from user_service.user import UserRepo
from user_service.db import db

user_repo = UserRepo(db)

blueprint = Blueprint("auth", __name__, url_prefix=config.api_prefix)


@blueprint.route("/login", methods=["POST"])
def login():
    email = request.json["email"]
    password = request.json["password"]

    user = user_repo.find_user(email)
    if user is None:
        resp: Response = jsonify({"ok": False, "error": "not authenticated"})
        resp.status_code = 401
        return resp

    is_ok = check_password(password, user.bcrypt_hash)
    if not is_ok:
        resp: Response = jsonify({"ok": False, "error": "not authenticated"})
        resp.status_code = 401
        return resp

    token, expires_at = get_user_jwt_token(user.public_id)

    return jsonify({"ok": True, "token": token, "expires_at": expires_at})
