import uuid
import jwt

from datetime import datetime, timezone

from app.core.security import create_access_token
from app.database.connection import settings


def test_create_access_token():
    user_id = str(uuid.uuid4())

    token = create_access_token(user_id)

    print("Token:", token)

    payload = jwt.decode(
        token,
        settings.jwt_secret_key,
        algorithms=[settings.jwt_algorithm],
        # options={"verify_exp": False},
    )

    # print("Payload:", payload)
    # print("Current UTC:", datetime.now(timezone.utc))
    # print("Expiration timestamp:", payload["exp"])

    assert payload["sub"] == user_id
    assert payload["exp"] > datetime.now(timezone.utc).timestamp()