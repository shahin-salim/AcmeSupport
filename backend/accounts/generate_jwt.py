import jwt
from backend.settings import SECRET_KEY
import datetime


def _create_jwt(user):
    return jwt.encode(
        {
            "userId": user.id,
            "role": user.role,
            "exp": datetime.timedelta(days=1) + datetime.datetime.now()
        },
        SECRET_KEY,
        algorithm="HS256"
    )