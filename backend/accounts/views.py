import datetime
from rest_framework import viewsets
import json
from accounts.decorator import is_user_is_authenticated
from .models import CustomUser
from .serializer import CustomUserSerializer
from rest_framework.views import APIView
from django.db.models import Q
from django.contrib.auth.hashers import check_password
from rest_framework.response import Response
from rest_framework import status
import jwt
from backend.settings import SECRET_KEY
from .generate_jwt import _create_jwt
from rest_framework import generics
from permission_class import FixPermission

# crud of the user custom user model


class UserView(viewsets.ModelViewSet):
    serializer_class = CustomUserSerializer
    queryset = CustomUser.objects.all()
    permission_classes = (FixPermission,)


class LoginView(APIView):
    def post(self, request):

        # find the user
        user = CustomUser.objects.filter(
            Q(email=request.data["email"])
            |
            Q(phone_number=request.data["email"])
        )

        try:
            # check the user entered passwor and model password is same

            if check_password(request.data["password"], user[0].password):
                return Response(
                    {"token": _create_jwt(user[0])},  # create jwt token
                    status=status.HTTP_200_OK
                )

        except IndexError:
            pass

        return Response(
            {"error": "User not found with this given credencails"},
            status=status.HTTP_400_BAD_REQUEST
        )


class GetUser(APIView):

    @is_user_is_authenticated
    def get(self, request, user):
        serializer = CustomUserSerializer(user).data
        del serializer["password"]
        return Response(serializer, status=status.HTTP_200_OK)
