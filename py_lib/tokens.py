import jwt


def encode_jwt(payload, secret):
    return jwt.encode(payload, secret, algorithm="HS256")


def decode_jwt(token, secret):
    return jwt.decode(token, secret, algorithms=["HS256"])
