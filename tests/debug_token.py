import jwt

from app.database.connection import settings

token = input("Вставь JWT из ответа POST /users/token: ").strip()

try:
    payload = jwt.decode(
        token,
        settings.jwt_secret_key,
        algorithms=[settings.jwt_algorithm],
    )
    print("JWT valid:", payload)
except jwt.InvalidTokenError as error:
    print("JWT error:", type(error).__name__, str(error))
