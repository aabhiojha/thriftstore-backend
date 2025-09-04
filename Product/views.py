from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import PermissionDenied
from .pagination import (
    PageNumberProductPagination,
    LimitOffsetProductPagination,
    CursorProductPaginationWithOrdering,
)

from .models import Category, Product
from .serializers import (
    CategorySerializer,
    ProductSerializerForCreate,
    ProductSerializerForList,
    ProductSerializerForUpdate,
)

from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.mixins import PermissionRequiredMixin

from django.shortcuts import get_object_or_404


class ProductListAPIView(generics.ListAPIView):
    queryset = Product.objects.all().order_by("id")
    serializer_class = ProductSerializerForList
    # pagination_class = PageNumberProductPagination
    # pagination_class = LimitOffsetProductPagination
    pagination_class = CursorProductPaginationWithOrdering


class ProductRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializerForList


class ProductCreateAPIView(generics.CreateAPIView):
    serializer_class = ProductSerializerForCreate
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(seller=self.request.user)


class ProductUpdateAPIView(generics.UpdateAPIView):
    serializer_class = ProductSerializerForUpdate
    queryset = Product.objects.all()
    permission_classes = [IsAuthenticated]

    def get_object(self):
        obj = super().get_object()
        if obj.seller != self.request.user:
            raise PermissionDenied("Cannot update other's products.")
        return obj


class ProductDeleteAPIView(generics.DestroyAPIView):
    queryset = Product.objects.all()
    permission_classes = [IsAuthenticated]

    def get_object(self):
        obj = super().get_object()
        if obj.seller != self.request.user:
            raise PermissionDenied("Cannot delete other's products.")
        return obj

    def destroy(self, request, *args, **kwargs):
        obj = self.get_object()
        self.perform_destroy(obj)
        return Response(
            "Product succesfully deleted", status=status.HTTP_204_NO_CONTENT
        )


class CategoryListAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CategoryCreateAPIView(PermissionRequiredMixin, APIView):
    permission_required = []

    def post(self, request):
        if self.request.user.has_perm("can_create_category"):
            serializer = CategorySerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(
            {"error": "User doesn't has permission"},
            status=status.HTTP_401_UNAUTHORIZED,
        )
