from user_service.password import generate_hash

from .models import User
from .utils import normalize_email


class UserRepo:
    def __init__(self, db):
        self.db = db

    def add_user(self, email: str, password: str):
        hashed_password = generate_hash(password)

        user = User(
            email=normalize_email(email),
            bcrypt_hash=hashed_password,
        )

        self.db.session.add(user)
        self.db.session.commit()
        return

    def find_user(self, email: str):
        email = normalize_email(email)
        return User.query.filter(
            User.email == email,
        ).first()
