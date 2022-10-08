import bcrypt


def password_utf8(password):
    if isinstance(password, str):
        password = password.encode("utf-8")
    return password


def check_password(password, password_hash):
    password = password_utf8(password)
    return bcrypt.checkpw(password, password_hash)


def generate_hash(password):
    salt = bcrypt.gensalt()
    bc_hash = bcrypt.hashpw(password_utf8(password), salt)
    return bc_hash
