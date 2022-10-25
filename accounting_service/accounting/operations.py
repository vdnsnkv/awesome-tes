from flask import current_app

from accounting_service.user.models import User


def deposit_money_to_user_account(user: User, amount: int, task_id: str = None):
    tr = current_app.transation_repo.add_transaction(
        user_id=user.public_id,
        task_id=task_id,
        amount=amount,
    )

    current_app.transaction_streaming.send_event(tr)

    current_app.user_repo.update_user_balance(user, amount)
    return


def withdraw_money_from_user_account(user: User, amount: int, task_id: str = None):
    if amount > 0:
        amount = -1 * amount

    tr = current_app.transation_repo.add_transaction(
        user_id=user.public_id,
        task_id=task_id,
        amount=amount,
    )

    current_app.transaction_streaming.send_event(tr)

    current_app.user_repo.update_user_balance(user, amount)
    return


def pay_user_balance(user: User):
    amount = (-1) * user.balance

    tr = current_app.transation_repo.add_transaction(
        user_id=user.public_id,
        amount=amount,
    )

    current_app.transaction_streaming.send_event(tr)

    current_app.user_repo.update_user_balance(user, amount)
    return tr
