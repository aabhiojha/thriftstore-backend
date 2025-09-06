from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser, BasePermission
from .serializers import UserListSerializer, UserCreateSerializer, ListRoleSerializer, CreateRoleSerializer, ListPermissionCategorySerializer, CreatePermissionCategorySerializer, ListPermissionSerializer, CreatePermissionSerializer
from rest_framework.response import Response
from rest_framework import status
from account.models import User, Role, Permission, PermissionCategory


class ListCreateUserAPIView(APIView):
    def get(self, request):
        if self.request.user.is_superuser:
            users = User.objects.all()
            serializer = UserListSerializer(users, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(
            {"error": "Unauthroized Request. Not enough permissions"},
            status=status.HTTP_401_UNAUTHORIZED,
        )

    def post(self, request):
        if self.request.user.is_superuser:
            serializer = UserCreateSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(
                {"error": "Malformed request"}, status=status.HTTP_400_BAD_REQUEST
            )
        return Response(
            {"error": "Unauthroized Request. Not enough permissions"},
            status=status.HTTP_401_UNAUTHORIZED,
        )



# Create role and List Roles API View
# Initial thought is to only make it accessible to superusers only.
# I think I should make it accessible to users with specific permission category too.
class ListCreateRoleAPIView(APIView):
    def get(self, request):
        if self.request.user.is_superuser:
            roles = Role.objects.all()
            serializer = ListRoleSerializer(roles, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(
            {"error": "Unauthroized Request. Not enough permissions"},
            status=status.HTTP_401_UNAUTHORIZED,
        )

    def post(self, request):
        if self.request.user.is_superuser:
            serializer = CreateRoleSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(
                {"error": "Malformed request"}, status=status.HTTP_400_BAD_REQUEST
            )
        return Response(
            {"error": "Unauthroized Request. Not enough permissions"},
            status=status.HTTP_401_UNAUTHORIZED,
        )


# Create Permission and List Permissions API View
# Only superusers can create and list permissions for now.
class ListCreatePermissionAPIView(APIView):
    def get(self, request):
        if self.request.user.is_superuser:
            permissions = Permission.objects.all()
            serializer = ListPermissionSerializer(permissions, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(
            {"error": "Unauthroized Request. Not enough permissions"},
            status=status.HTTP_401_UNAUTHORIZED,
        )

    def post(self, request):
        if self.request.user.is_superuser:
            serializer = CreatePermissionSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(
                {"error": "Malformed request"}, status=status.HTTP_400_BAD_REQUEST
            )
        return Response(
            {"error": "Unauthroized Request. Not enough permissions"},
            status=status.HTTP_401_UNAUTHORIZED,
        )


class ListCreatePermissionCategoryAPIView(APIView):
    def get(self, request):
        if self.request.user.is_superuser:
            roles = Role.objects.all()
            serializer = ListPermissionCategorySerializer(roles, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(
            {"error": "Unauthroized Request. Not enough permissions"},
            status=status.HTTP_401_UNAUTHORIZED,
        )

    def post(self, request):
        if self.request.user.is_superuser:
            serializer = CreatePermissionCategorySerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(
                {"error": "Malformed request"}, status=status.HTTP_400_BAD_REQUEST
            )
        return Response(
            {"error": "Unauthroized Request. Not enough permissions"},
            status=status.HTTP_401_UNAUTHORIZED,
        )
