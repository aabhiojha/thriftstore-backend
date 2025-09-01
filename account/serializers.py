from rest_framework import serializers

from .models import User


class UserListSerializer(serializers.ModelSerializer):
    password = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = [
            "email",
            "name",
            "password",
            "is_active",
            "is_superuser",
            "is_staff",
            "last_login",
        ]


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            "email",
            "name",
            "password",
            "is_active",
            "is_superuser",
            "is_staff",
            "last_login",
        ]

    def create(self, validated_data):
        password = validated_data.pop("password")
        # password = validated_data.get["password"]
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user
