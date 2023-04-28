import jwt
from datetime import datetime, timedelta
from app.common.constants import JWT_SECRET, JWT_ALGORITHM
from app.database.schema import User


async def is_email_exist(email: str):
    get_email = User.get(email=email)
    if get_email:
        return True
    return False


def create_access_token(*, data: dict = None, expires_delta: int = None):
    to_encode = data.copy()
    if expires_delta:
        to_encode.update({"exp": datetime.utcnow() + timedelta(hours=expires_delta)})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return encoded_jwt
