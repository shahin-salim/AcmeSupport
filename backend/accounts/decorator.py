from accounts.models import CustomUser
import jwt
from backend.settings import SECRET_KEY
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist

# check user have a valid jwt token


def is_user_is_authenticated(fun):
    def inner(self, request):
        try:
            token = (request.META["HTTP_AUTHORIZATION"]).split(" ")
            if token[0] == "Bearer":
                decoded = jwt.decode(
                    token[1], SECRET_KEY, algorithms=["HS256"]
                )
                return fun(self, request, CustomUser.objects.get(id=decoded["userId"]))
        except:
            pass

        return Response(
            {"error": "invalid token"},
            status=status.HTTP_401_UNAUTHORIZED
        )

    return inner
