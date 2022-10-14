from flask import request, Blueprint, current_app

from user_service.responses import RESPONSE_404
from user_service.decorators import admin_role_required

from user_service.events import UserStreamingEventType


blueprint = Blueprint("users", __name__)


@blueprint.route("/users", methods=["POST"])
@admin_role_required
def create_user():
    email = request.json["email"]
    password = request.json["password"]

    user = current_app.user_repo.add_user(email, password)

    current_app.user_streaming.send_event(user, UserStreamingEventType.Created)

    return {"ok": True, "user_id": str(user.public_id), "email": user.email}


@blueprint.route("/users/<public_id>", methods=["GET"])
@admin_role_required
def read_user(public_id):
    user = current_app.user_repo.get_user(public_id)
    if user is None:
        return RESPONSE_404

    return {"ok": True, "user_id": str(user.public_id), "email": user.email}


@blueprint.route("/users/<public_id>", methods=["PATCH"])
@admin_role_required
def update_user(public_id):
    user = current_app.user_repo.get_user(public_id)
    if user is None:
        return RESPONSE_404

    role = request.json.get("role")
    name = request.json.get("name")
    if role is None and name is None:
        return {"ok": True}

    user = current_app.user_repo.update_user(user, role, name)

    current_app.user_streaming.send_event(user, UserStreamingEventType.Updated)

    return {
        "ok": True,
        "user_id": str(user.public_id),
        "name": user.name,
        "role": user.role,
    }
