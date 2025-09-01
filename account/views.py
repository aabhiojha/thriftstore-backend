from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser
from .serializers import UserListSerializer, UserCreateSerializer
from rest_framework.response import Response
from rest_framework import status
from account.models import User


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
