import functools


def admin_access_required(f):
    @functools.wraps(f)
    def wrapper(self, info, *args, **kwargs):
        current_user = getattr(info.context, "user", None)
        if current_user is None or not is_diagnocat_admin(current_user):
            raise AccessDeniedError()
        return f(self, info, *args, **kwargs)

    return wrapper
