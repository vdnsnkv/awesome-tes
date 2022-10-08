import time
import datetime

import jwt
from secrets import token_hex

import config
from logger import logger

TOKEN_TYPE_ACCESS = "access"
TOKEN_TYPE_ACCESS_LEGACY = "access_legacy"
TOKEN_TYPE_API = "api"
TOKEN_TYPE_PARTNER_API = "partner_api"
TOKEN_TYPE_REDIRECT = "redirect"
TOKEN_TYPE_ORGANIZATION_INVITE = "organization_invite"
TOKEN_TYPE_SHARE_PATIENT = "share_patient"


class TokenError(Exception):
    pass


def simple_random_token():
    return token_hex(32)


def _encode_jwt(payload):
    return jwt.encode(payload, config.SECRET, algorithm="HS256")


def _decode_jwt(token, required_keys: list = None):
    try:
        payload = jwt.decode(token, config.SECRET, algorithms=["HS256"])
    except (
        jwt.exceptions.ExpiredSignatureError,
        jwt.exceptions.DecodeError,
        jwt.InvalidTokenError,
    ) as e:
        logger.exception(e)
        raise TokenError()

    if required_keys is not None and any(
        [k not in payload.keys() for k in required_keys]
    ):
        raise TokenError(
            f'Invalid payload: token_type={payload.get("token")}, keys={payload.keys()}'
        )

    return payload


def jwt_access_token(email, organization_id, ttl: int = config.ACCESS_TOKEN_TTL):
    issued_at = int(time.time())
    expires_at = issued_at + ttl
    token = _encode_jwt(
        {
            "email": email.lower(),
            "organization_id": organization_id,
            "token": TOKEN_TYPE_ACCESS,
            "iss": issued_at,
            "exp": expires_at,
        }
    )
    return token, expires_at


def access_token_payload(token):
    payload = _decode_jwt(token)

    email = payload["email"]
    token_type = payload.get("token")
    if token_type is None:
        token_type = payload.get("token_type")
    organization_id = payload.get("organization_id")
    issued_at = payload.get("iss")
    expires_at = payload.get("exp")
    ts = payload.get("ts")

    return email, token_type, organization_id, issued_at, expires_at, ts


def jwt_access_token_legacy(email, organization_id):
    issued_at = int(time.time())
    expires_at = issued_at + 604800  # 7 days
    token = _encode_jwt(
        {
            "email": email.lower(),
            "organization_id": organization_id,
            "token": TOKEN_TYPE_ACCESS_LEGACY,
            "iss": issued_at,
            "exp": expires_at,
        }
    )
    return token


def jwt_api_access_token(
    email, organization_id, client_host_id, ttl: int = config.API_ACCESS_TOKEN_TTL
):
    issued_at = int(time.time())
    expires_at = issued_at + ttl
    token = _encode_jwt(
        {
            "email": email.lower(),
            "organization_id": organization_id,
            "client_host_id": client_host_id,
            "token": TOKEN_TYPE_API,
            "iss": issued_at,
            "exp": expires_at,
        }
    )
    return token, expires_at


def jwt_partner_api_token(email, organization_id, user_id):
    issued_at = int(time.time())
    return _encode_jwt(
        {
            "organization_id": organization_id,
            "user_id": user_id,
            "email": email.lower(),
            "token_type": TOKEN_TYPE_PARTNER_API,
            "token": TOKEN_TYPE_PARTNER_API,
            "iss": issued_at,
            "ts": issued_at,
        }
    )


def jwt_redirect_token(email, ttl: int = config.REDIRECT_TOKEN_TTL):
    issued_at = int(time.time())
    expires_at = issued_at + ttl
    token = _encode_jwt(
        {
            "email": email.lower(),
            "token": TOKEN_TYPE_REDIRECT,
            "iss": issued_at,
            "exp": expires_at,
        }
    )
    return token, expires_at


def redirect_token_payload(token):
    payload = _decode_jwt(token)

    if set(payload.keys()) != {"email", "token", "iss", "exp"}:
        logger.error(
            "invalid redirect token payload",
            extra={
                "payload_keys": payload.keys(),
            },
        )
        raise TokenError()

    token_type = payload["token"]
    if token_type != TOKEN_TYPE_REDIRECT:
        logger.error(
            "invalid redirect token type",
            extra={
                "token_type": token_type,
            },
        )
        raise TokenError()

    return payload["email"], token_type, payload["exp"]


INVITE_TOKEN_PAYLOAD_KEYS = ["email", "organization_id", "invited_user_id"]


def jwt_organization_invite_token(organization, invited_user, target_email):
    issued_at = int(time.time())
    return _encode_jwt(
        {
            "email": target_email.lower(),
            "organization_id": organization.id,
            "invited_user_id": invited_user.id,
            "token": TOKEN_TYPE_ORGANIZATION_INVITE,
            "iss": issued_at,
        }
    )


def organization_invite_token_payload(token):

    payload = _decode_jwt(token, required_keys=INVITE_TOKEN_PAYLOAD_KEYS)

    return payload["email"], payload["organization_id"], payload["invited_user_id"]


def jwt_share_patient_token(from_organization, from_user, to_email, patient_id):
    issued_at = int(time.time())
    return _encode_jwt(
        {
            "from": from_user.email,
            "to": to_email.lower(),
            "organization_id": from_organization.id,
            "patient_id": int(patient_id),
            "token": TOKEN_TYPE_SHARE_PATIENT,
            "iss": issued_at,
        }
    )


REQUIRED_PAYLOAD_KEYS = ["from", "to", "patient_id"]


def share_token_payload(token):

    payload = _decode_jwt(token, required_keys=REQUIRED_PAYLOAD_KEYS)

    return (
        payload["from"],
        payload["to"],
        payload.get("organization_id"),
        payload["patient_id"],
    )
