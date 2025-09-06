from rest_framework import serializers

from .models.models import User
from .models.permission_models import PermissionCategory, Permission, Role


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



# Permission related serializers
# Role model Serializers
class ListRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'

class CreateRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'


# Permissions model serializers
class ListPermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = "__all__"
        
class CreatePermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = "__all__"


# Permission Category model serializer
class ListPermissionCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = PermissionCategory
        fields = "__all__"

class CreatePermissionCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = PermissionCategory
        fields = "__all__"