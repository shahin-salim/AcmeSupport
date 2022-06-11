from accounts.models import CustomUser
import jwt
from backend.settings import SECRET_KEY
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist


# decode the jwt token
def decode_jwt(request):
    token = (request.META["HTTP_AUTHORIZATION"]).split(" ")
    if token[0] == "Bearer":
        return jwt.decode(
            token[1], SECRET_KEY, algorithms=["HS256"]
        )


# check user is autorized check jwt if right return user instace
def is_user_is_authenticated(fun):
    def inner(self, request):
        try:
            decoded = decode_jwt(request)
            return fun(self, request, CustomUser.objects.get(id=decoded["userId"]))
        except:
            pass

        return Response(
            {"error": "invalid token"},
            status=status.HTTP_401_UNAUTHORIZED
        )

    return inner
