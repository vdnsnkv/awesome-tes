from datetime import datetime
from flask import request, Response, jsonify, Blueprint, Request

import config
import models
import errors
import redis_cache
import tokens
from auth_api import (
    check_login_credentials,
    current_user,
)
from organization.views import get_organization_for_user
from user.controllers import clear_first_login_status


URL_PREFIX = f"{config.API_PREFIX}/auth"

blueprint = Blueprint("auth", __name__, url_prefix=URL_PREFIX)


@blueprint.route("/login", methods=["POST"])
def login():
    email = request.json["email"]
    password = request.json["password"]

    try:
        user = check_login_credentials(email, password)
    except (errors.NotFoundError, errors.NotAuthenticatedError) as e:
        resp: Response = jsonify(
            {"ok": False, "error": e.default_message, "code": e.code}
        )
        resp.status_code = e.status

        return resp

    refresh_token = tokens.simple_random_token()

    resp: Response = jsonify({"ok": True})

    is_secure_cookie = config.ENVIRONMENT not in ["local", "test"]
    samesite = "Strict"
    if config.ENVIRONMENT in ["development", "test"] and is_secure_cookie:
        samesite = "None"

    resp.set_cookie(
        "refresh-token",
        value=refresh_token,
        max_age=60 * 60 * 24 * 365,
        path=URL_PREFIX,
        secure=is_secure_cookie,
        samesite=samesite,
        httponly=True,
    )

    create_user_auth_record(
        request, user, models.UserAuth.EventType.LOGIN, refresh_token
    )

    clear_first_login_status(user)

    return resp


def access_token_response(r: Request, ttl=config.ACCESS_TOKEN_TTL) -> Response:
    refresh_token = r.cookies.get("refresh-token")
    if refresh_token is None:
        resp: Response = jsonify({"ok": False, "error": "missing refresh-token"})
        resp.status_code = 401
        return resp

    auth_record = get_user_auth_record(refresh_token)
    if auth_record is None:
        resp: Response = jsonify({"ok": False, "error": "invalid refresh-token"})
        resp.status_code = 401
        return resp

    organization = get_organization_for_user(auth_record.user)
    organization_id = organization.id if organization is not None else None

    access_token, expires_at = tokens.jwt_access_token(
        auth_record.user.email, organization_id, ttl=ttl
    )

    resp: Response = jsonify(
        {"ok": True, "token": access_token, "expires_at": expires_at}
    )

    update_user_auth_record(auth_record, last_access_token_issued_at=datetime.now())

    return resp


@blueprint.route("/access-token", methods=["GET"])
def access_token():
    return access_token_response(request)


@blueprint.route("/access-token-short", methods=["GET"])
def access_token_short():
    return access_token_response(request, ttl=5 * 60)


@blueprint.route("/check", methods=["GET"])
def check():
    user, _ = current_user()
    if user is None:
        resp: Response = jsonify({"ok": False, "error": "not authenticated"})
        resp.status_code = 401
        return resp
    else:
        resp: Response = jsonify({"ok": True, "email": user.email})
        return resp


@blueprint.route("/logout", methods=["POST"])
def logout():
    user, _ = current_user()
    if user is None:
        resp: Response = jsonify({"ok": False, "error": "not authenticated"})
        resp.status_code = 401
        return resp

    auth_records = get_all_active_user_auth_records(user)

    for rec in auth_records:
        rec.revoked = True
        rec.revoked_at = datetime.now()

    resp: Response = jsonify({"ok": True})

    redis_cache.cache_logout_timestamp(user)
    create_user_auth_record(request, user, models.UserAuth.EventType.LOGOUT)

    return resp
