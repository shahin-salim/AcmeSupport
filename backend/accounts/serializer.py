from rest_framework import serializers
from .models import CustomUser
from django.contrib.auth.hashers import make_password


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = "__all__"

    # validation for email or phone number
    def validate(self, data):
        print(data)

        if "email" not in data and "phone_number" not in data:
            raise serializers.ValidationError({
                "email": "email or phone number is required",
                "phone_number": "phone number or email is required"
            })

        return data

    # override create method for hash pwd
    def create(self, validated_data):
        validated_data["password"] = make_password(validated_data["password"])
        return CustomUser.objects.create(**validated_data)
