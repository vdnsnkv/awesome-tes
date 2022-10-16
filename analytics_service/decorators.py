from functools import wraps

from flask import request, current_app

from py_lib import decode_jwt

from analytics_service.config import config
from analytics_service.user import is_user_admin

from .responses import RESPONSE_401, RESPONSE_403


def jwt_token_payload(token):
    payload = decode_jwt(token, config.shared_secret)

    user_id = payload["user_id"]
    issued_at = payload["iss"]
    expires_at = payload["exp"]

    return user_id, issued_at, expires_at


def authorization_header_token():
    """
    Expected Authorization header format:

    Token <JWT_TOKEN>
    """
    header = request.headers.get("Authorization")
    if header is None:
        return

    try:
        _, token = header.split(" ")
        return token
    except Exception:
        return


def auth_token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = authorization_header_token()
        if not token:
            return RESPONSE_401

        user_id, _, _ = jwt_token_payload(token)

        request.user_id = user_id

        return f(*args, **kwargs)

    return decorated


def admin_role_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = authorization_header_token()
        if not token:
            return RESPONSE_401

        user_id, _, _ = jwt_token_payload(token)

        user = current_app.user_repo.get_user(user_id)
        if not is_user_admin(user):
            return RESPONSE_403

        return f(*args, **kwargs)

    return decorated
