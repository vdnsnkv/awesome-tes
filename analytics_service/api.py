from collections import defaultdict
from datetime import datetime

from flask import Blueprint, current_app

from analytics_service.task.models import Task
from analytics_service.decorators import (
    admin_role_required,
)
from analytics_service.responses import RESPONSE_400

blueprint = Blueprint("analytics", __name__)


def task_to_response_data(task: Task):
    if not task:
        return
    return {
        "task_id": str(task.public_id),
        "title": task.title,
        "description": task.description,
        "status": task.status,
        "assign_price": task.assign_price,
        "done_price": task.done_price,
        "meta": task.meta,
        "created_at": task.created_at.isoformat(),
        "updated_at": task.updated_at.isoformat(),
    }


@blueprint.route("/analytics/dashboard", methods=["GET"])
@admin_role_required
def get_dashboard(day):
    today_transactions = current_app.transaction_repo.get_today_transactions()

    user_earnings = defaultdict(int)
    total_amount = 0
    for tr in today_transactions:
        if tr.task_id is None:
            # skip, since this is not a task-assigned or task-done transaction
            continue
        user_earnings[tr.user_id] += tr.amount
        total_amount += tr.amount

    negative_sum_users_count = len([v for v in user_earnings.values() if v < 0])

    return {
        "total_earnings": (-1) * total_amount,
        "negative_sum_users_count": negative_sum_users_count,
    }


@blueprint.route("/analytics/tasks/<start_date>/<end_date>", methods=["GET"])
@admin_role_required
def get_tasks_analytics(start_date, end_date):
    try:
        start_date = datetime.strptime(start_date, "%Y-%m-%d")
        end_date = datetime.strptime(end_date, "%Y-%m-%d")
    except ValueError:
        return RESPONSE_400

    transactions = current_app.transaction_repo.get_date_range_transactions(
        start_date, end_date
    )

    biggest_amount_transaction_by_date = {}
    for tr in transactions:
        if tr.task_id is None:
            # skip, since this is not a task-assigned or task-done transaction
            continue

        date = tr.created_at.date()

        if date not in biggest_amount_transaction_by_date:
            biggest_amount_transaction_by_date[date] = tr
            continue

        current_tr = biggest_amount_transaction_by_date[date]
        if tr.amount > current_tr.amount:
            biggest_amount_transaction_by_date[date] = tr

    most_expensive_task_by_date = {
        d: current_app.task_repo.get_task(tr.task_id)
        for d, tr in biggest_amount_transaction_by_date.items()
    }

    return {
        d.strftime("%Y-%m-%d"): task_to_response_data(task)
        for d, task in most_expensive_task_by_date.items()
    }
