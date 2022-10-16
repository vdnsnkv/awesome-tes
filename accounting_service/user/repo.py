import uuid

from .models import User


class UserRepo:
    def __init__(self, db):
        self.db = db

    def add_user(self, data: dict):
        user = User(**data)
        self.db.session.add(user)
        self.db.session.commit()
        return user

    def get_user(self, public_id: str):
        return self.db.session.query(User).get(uuid.UUID(public_id))

    def get_all_users(self):
        return self.db.session.query(User).all()

    def update_user(self, user: User, new_data: dict):
        for k, v in new_data.items():
            setattr(user, k, v)
        self.db.session.add(user)
        self.db.session.commit()
        return user

    def update_user_balance(self, user: User, amount: int):
        user.balance += amount
        self.db.session.add(user)
        self.db.session.commit()
        return user
