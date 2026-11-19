from datetime import datetime, timedelta, timezone

import math
import jwt

from pwdlib import PasswordHash

from app.database.connection import settings

# Password Hashing Block

password_hash = PasswordHash.recommended()

def hash_password(password: str) -> str:
    return password_hash.hash(password)

def verify_password(
        password: str, 
        hashed_password: str
) -> bool:
    return password_hash.verify(password, hashed_password)

# Access Token

def create_access_token(user_id: str) -> str:
    expires_at = datetime.now(timezone.utc) + timedelta(
        minutes=settings.access_token_expire_minutes
    )

    payload = {
        "sub": user_id,
        "exp": math.ceil(expires_at.timestamp()),
    }

    return jwt.encode(
        payload,
        settings.jwt_secret_key,
        algorithm=settings.jwt_algorithm,
    )