from flask import request, Blueprint, current_app

from accounting_service.decorators import (
    auth_token_required,
    admin_or_accountant_role_required,
)
from accounting_service.responses import RESPONSE_403, RESPONSE_404

from accounting_service.transaction.models import Transaction
from accounting_service.task.models import Task


blueprint = Blueprint("accounting", __name__)


def transaction_to_response_data(tr: Transaction):
    return {
        "transaction_id": str(tr.public_id),
        "user_id": str(tr.user_id),
        "amount": tr.amount,
        "meta": tr.meta,
        "created_at": tr.created_at.isoformat(),
        "updated_at": tr.updated_at.isoformat(),
    }


def task_to_response_data(task: Task):
    if not task:
        return
    return {
        "task_id": str(task.public_id),
        "title": task.title,
        "assign_price": task.assign_price,
        "done_price": task.done_price,
        "meta": task.meta,
        "created_at": task.created_at.isoformat(),
        "updated_at": task.updated_at.isoformat(),
    }


@blueprint.route("/accounting/dashboard/<day>", methods=["GET"])
@admin_or_accountant_role_required
def get_dashboard(day):
    if day == "today":
        today_transactions = current_app.transaction_repo.get_today_transactions()
        return [transaction_to_response_data(tr) for tr in today_transactions]

    return RESPONSE_404


@blueprint.route("/accounting/user/<user_id>", methods=["GET"])
@auth_token_required
def get_user_transactions():

    user_id = request.args.get("user_id")
    if user_id != request.user_id:
        return RESPONSE_403

    user_transactions = current_app.transaction_repo.get_user_transactions(user_id)

    task_ids = [tr.task_id for tr in user_transactions]
    tasks = {t.public_id: t for t in current_app.task_repo.get_tasks(task_ids)}
    return [
        {
            **transaction_to_response_data(tr),
            "task": task_to_response_data(
                tasks.get(tr.task_id),
            ),
        }
        for tr in user_transactions
    ]
