import jwt
from backend.settings import SECRET_KEY
import datetime

# create jwt token and 1 day exp for jwt token
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