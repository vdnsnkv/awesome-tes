import uuid

from user_service.auth import generate_hash
from user_service.events.user_cud import send_user_cud_event, UserCUDEventType

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

        send_user_cud_event(user, UserCUDEventType.Created)

        return user

    def get_user(self, public_id: str):
        return (
            self.db.session.query(User)
            .filter(
                User.public_id == uuid.UUID(public_id),
            )
            .first()
        )

    def find_user(self, email: str):
        email = normalize_email(email)
        return (
            self.db.session.query(User)
            .filter(
                User.email == email,
            )
            .first()
        )

    def update_user(self, user: User, role: str = None, name: str = None):
        is_updated = False
        if role is not None:
            role = User.Role(role)
            user.role = role.value
            is_updated = True
        if name is not None:
            user.name = name
            is_updated = True
        self.db.session.add(user)
        self.db.session.commit()

        if is_updated:
            send_user_cud_event(user, UserCUDEventType.Updated)

        return user
