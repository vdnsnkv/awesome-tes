from flask import request, Blueprint, current_app

from task_tracker.user import is_user_manager, is_user_admin
from task_tracker.responses import RESPONSE_404
from task_tracker.decorators import admin_or_manager_role_required, auth_token_required
from task_tracker.events import TaskStreamingEventType

from .status import is_task_done
from .utils import select_random_element


blueprint = Blueprint("tasks", __name__)


@blueprint.route("/tasks", methods=["POST"])
@auth_token_required
def create_task():
    title = request.json["title"]
    desc = request.json["desc"]

    all_users = current_app.user_repo.get_all_users()

    assignee_candidates = [
        u for u in all_users if not is_user_manager(u) and not is_user_admin(u)
    ]

    assignee = select_random_element(assignee_candidates)

    task = current_app.task_repo.add_task(title, desc, assignee.public_id)

    current_app.task_streaming.send_event(task, TaskStreamingEventType.Created)

    return {
        "ok": True,
        "task_id": str(task.public_id),
        "title": task.title,
        "desc": task.description,
        "status": task.status,
    }


@blueprint.route("/tasks/<public_id>", methods=["GET"])
@auth_token_required
def read_task(public_id):
    task = current_app.task_repo.get_task(public_id)
    if task is None:
        return RESPONSE_404

    return {
        "ok": True,
        "task_id": str(task.public_id),
        "title": task.title,
        "desc": task.description,
        "status": task.status,
        "user_id": str(task.user_id),
    }


@blueprint.route("/tasks", methods=["GET"])
@auth_token_required
def read_all_tasks():
    all_tasks = current_app.task_repo.get_all_tasks()

    return [
        {
            "task_id": str(task.public_id),
            "title": task.title,
            "desc": task.description,
            "status": task.status,
            "user_id": str(task.user_id),
        }
        for task in all_tasks
    ]


@blueprint.route("/tasks", methods=["PATCH"])
@admin_or_manager_role_required
def reassign_tasks():
    tasks = current_app.task_repo.get_all_tasks()

    todo_tasks = [t for t in tasks if not is_task_done(t)]

    all_users = current_app.user_repo.get_all_users()

    assignee_candidates = [
        u for u in all_users if not is_user_manager(u) and not is_user_admin(u)
    ]

    updated_tasks = []
    for t in todo_tasks:
        new_assignee = select_random_element(assignee_candidates)
        task = current_app.task_repo.update_task(t, user_id=new_assignee.public_id)
        updated_tasks.append(task)

    for t in updated_tasks:
        current_app.task_streaming.send_event(t, TaskStreamingEventType.Updated)

    return [
        {
            "task_id": str(task.public_id),
            "title": task.title,
            "desc": task.description,
            "status": task.status,
            "user_id": str(task.user_id),
        }
        for task in updated_tasks
    ]
