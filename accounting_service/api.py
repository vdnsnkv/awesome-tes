from flask import request, Blueprint, current_app

from accounting_service.decorators import (
    auth_token_required,
    admin_or_accountant_role_required,
)
from accounting_service.responses import RESPONSE_404, RESPONSE_403

from .models import Transaction


blueprint = Blueprint("transactions", __name__)


def transaction_to_response_data(tr: Transaction):
    return {
        "transaction_id": str(tr.public_id),
        "user_id": str(tr.user_id),
        "amount": tr.amount,
        "meta": tr.meta,
        "created_at": tr.created_at.isoformat(),
        "updated_at": tr.updated_at.isoformat(),
    }


@blueprint.route("/transactions/today", methods=["GET"])
@admin_or_accountant_role_required
def get_today_transactions(public_id):
    today_transactions = current_app.transaction_repo.get_today_transactions()
    return [transaction_to_response_data(tr) for tr in today_transactions]


@blueprint.route("/transactions", methods=["GET"])
@auth_token_required
def get_user_transactions():

    user_id = request.args.get("user_id")
    if user_id != request.user_id:
        return RESPONSE_403

    user_transactions = current_app.transaction_repo.get_user_transactions(user_id)
    return [transaction_to_response_data(tr) for tr in user_transactions]
