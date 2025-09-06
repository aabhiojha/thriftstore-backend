from rest_framework import serializers

from .models.models import User
from .models.permission_models import PermissionCategory, Permission, Role


class UserListSerializer(serializers.ModelSerializer):
    password = serializers.CharField(read_only=True)
    roles = serializers.StringRelatedField(many=True, read_only=True)
    permissions = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id',
            "email",
            "name",
            "password",
            "is_active",
            "is_superuser",
            "is_staff",
            "last_login",
            'roles',
            'permissions'
        ]

    def get_permissions(self, obj):
        return [perm.code_name for perm in obj.get_all_permissions()]


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    role_ids = serializers.ListField(
        child = serializers.IntegerField(),
        write_only=True,
        required=False
    )

    class Meta:
        model = User
        fields = [
            "email",
            "name",
            "password",
            "is_active",
            "is_superuser",
            "is_staff",
            "role_ids"
        ]

    def create(self, validated_data):
        role_ids = validated_data.pop("role_ids", [])
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()

        if role_ids:
            roles = Role.objects.filter(id__in = role_ids, is_active=True)
            user.roles.set(roles)
        return user



# Permission related serializers
# Role model Serializers
class ListRoleSerializer(serializers.ModelSerializer):
    permissions = serializers.StringRelatedField(many=True, read_only=True)    
    user_count = serializers.SerializerMethodField()
    class meta:
        model = Role
        fields = ['id', 'name', 'is_active', 'permissions', 'user_count']
    
    def get_user_count(self, obj):
        return obj.users.count()

class CreateRoleSerializer(serializers.ModelSerializer):
    permission_ids = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True,
        required=False
    )
    
    class Meta:
        model = Role
        fields = ['name', 'is_active', 'permission_ids']
    
    def create(self, validated_data):
        permission_ids = validated_data.pop('permission_ids', [])
        role = Role.objects.create(**validated_data)
        
        if permission_ids:
            permissions = Permission.objects.filter(id__in=permission_ids)
            role.permissions.set(permissions)
        
        return role


# Permissions model serializers
class ListPermissionSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    
    class Meta:
        model = Permission
        fields = ["id", "name", "code_name", "category", "category_name", "is_active"]
        
class CreatePermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ["name", "code_name", "category", "is_active"]


# Permission Category model serializer
class ListPermissionCategorySerializer(serializers.ModelSerializer):
    permissions_count = serializers.SerializerMethodField()
    
    class Meta:
        model = PermissionCategory
        fields = ["id", "name", "is_active", "permissions_count"]
    
    def get_permissions_count(self, obj):
        return obj.permissions.count()

class CreatePermissionCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = PermissionCategory
        fields = ["name", "is_active"]