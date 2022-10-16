import uuid
from datetime import datetime

from .models import Transaction


class TransactionRepo:
    def __init__(self, db):
        self.db = db

    def add_transaction(self, user_id: str, amount: int, task_id: str = None):
        transaction = Transaction(user_id=user_id, amount=amount, task_id=task_id)
        self.db.session.add(transaction)
        self.db.session.commit()
        return transaction

    def get_user_transactions(self, user_id: str):
        return (
            self.db.session.query(Transaction)
            .filter(
                Transaction.user_id == uuid.UUID(user_id),
            )
            .all()
        )

    def get_today_transactions(self):
        utc_today = datetime.utcnow().date()
        return (
            self.db.session.query(Transaction)
            .filter(
                Transaction.created_at >= utc_today,
            )
            .all()
        )
