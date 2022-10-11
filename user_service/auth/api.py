from flask import request, Blueprint, current_app

from user_service.responses import RESPONSE_401

from .token import get_user_jwt_token
from .password import check_password


blueprint = Blueprint("auth", __name__, url_prefix="/auth")


@blueprint.route("/login", methods=["POST"])
def login():
    email = request.json["email"]
    password = request.json["password"]

    user = current_app.user_repo.find_user(email)
    if user is None:
        return RESPONSE_401

    is_ok = check_password(password, user.bcrypt_hash)
    if not is_ok:
        return RESPONSE_401

    token, expires_at = get_user_jwt_token(user.public_id)

    return {"ok": True, "token": token, "expires_at": expires_at}
