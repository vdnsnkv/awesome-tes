from .models import User


def is_user_admin(user: User):
    return User.Role(user.role) == User.Role.ADMIN


def is_user_manager(user: User):
    return User.Role(user.role) == User.Role.MANAGER
