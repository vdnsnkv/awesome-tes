import uuid
from datetime import datetime

import jwt

from user_service.config import config


def _encode_jwt(payload, secret):
    return jwt.encode(payload, secret, algorithm="HS256")


def _decode_jwt(token, secret):
    return jwt.decode(token, secret, algorithms=["HS256"])


def get_user_jwt_token(user_id: uuid.UUID, ttl: int = config.jwt_ttl):
    issued_at = datetime.utcnow().timestamp()
    expires_at = issued_at + ttl
    token = _encode_jwt(
        {
            "user_id": str(user_id),
            "iss": issued_at,
            "exp": expires_at,
        },
        config.shared_secret,
    )
    return token, expires_at


def jwt_token_payload(token):
    payload = _decode_jwt(token, config.shared_secret)

    user_id = payload["user_id"]
    issued_at = payload["iss"]
    expires_at = payload["exp"]

    return user_id, issued_at, expires_at
