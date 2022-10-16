import uuid
from datetime import datetime

from .models import Transaction


def _filter_data(data: dict):
    return {k: v for k, v in data.items() if k in Transaction.__table__.c}


class TransactionRepo:
    def __init__(self, db):
        self.db = db

    def add_transaction(self, data: dict):
        transaction = Transaction(**_filter_data(data))
        self.db.session.add(transaction)
        self.db.session.commit()
        return transaction

    def get_transaction(self, public_id: str):
        return self.db.session.query(Transaction).get(uuid.UUID(public_id))

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

    def get_date_range_transactions(self, start_date: datetime, end_date: datetime):
        return (
            self.db.session.query(Transaction)
            .filter(
                Transaction.created_at >= start_date.date(),
                Transaction.created_at < end_date.date(),
            )
            .all()
        )

    def update_transaction(self, tr: Transaction, data: dict):
        for k, v in _filter_data(data).items():
            setattr(tr, k, v)
        self.db.session.add(tr)
        self.db.session.commit()
        return tr
