from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.shortcuts import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from rest_framework.exceptions import PermissionDenied

from .models import Category, Product
from .serializers import (
    CategorySerializer,
    ProductSerializerForCreate,
    ProductSerializerForList,
    ProductSerializerForUpdate,
)

from django.shortcuts import get_object_or_404


class ProductListAPIView(generics.ListAPIView):
    queryset = Product.objects.all().order_by("id")
    serializer_class = ProductSerializerForList


class ProductRetrieveAPIView(generics.ListAPIView):
    # queryset = Product.objects.filter(id=pk)
    serializer_class = ProductSerializerForList

    def get_queryset(self):
        product_id = self.kwargs.get("pk")
        return Product.objects.filter(id=product_id)


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


# class ProductListCreate(generics.ListCreateAPIView):
#     queryset = Product.objects.all().order_by("id")
#     serializer_class = ProductSerializer

#     def get_permissions(self):
#         if self.request.method == "POST":
#             return [IsAuthenticated()]
#         return [AllowAny()]


# class ProductListCreateAPIView(APIView):
#     permission_classes = [AllowAny]

#     def get(self, request):
#         products = Product.objects.all().order_by("-created_at")
#         paginator = PageNumberPagination()
#         paginator.page_size = 5
#         page = paginator.paginate_queryset(products, request)
#         serializer = ProductSerializer(page, many=True)
#         return paginator.get_paginated_response(serializer.data)

#     def post(self, request):
#         if not request.user.is_authenticated:
#             return Response(
#                 {"error": "Authentication required"},
#                 status=status.HTTP_401_UNAUTHORIZED,
#             )
#         data = request.data
#         serializer = ProductSerializer(data=data)
#         if serializer.is_valid():
#             serializer.save(seller=request.user)
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class ProductRetriveUpdateDestroyAPIView(APIView):
#     permission_classes = [AllowAny]

#     def get(self, request, pk):
#         product = get_object_or_404(Product, pk=pk)
#         product.views_count += 1
#         product.save()

#         serializer = ProductSerializer(product)
#         return Response(serializer.data, status=status.HTTP_200_OK)

#     def put(self, request, pk):
#         if not request.user.is_authenticated:
#             return Response(
#                 {"error": "Authentication required"},
#                 status=status.HTTP_401_UNAUTHORIZED,
#             )

#         product = get_object_or_404(Product, pk=pk)

#         if product.seller != request.user:
#             return Response(
#                 {"error": "You can only update your own products."},
#                 status=status.HTTP_403_FORBIDDEN,
#             )

#         serializer = ProductSerializer(product, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def patch(self, request, pk):
#         if not request.user.is_authenticated:
#             return Response(
#                 {"error": "Authentication required"},
#                 status=status.HTTP_401_UNAUTHORIZED,
#             )

#         product = get_object_or_404(Product, pk=pk)

#         if product.seller != request.user:
#             return Response(
#                 {"error": "You can only update your own products."},
#                 status=status.HTTP_403_FORBIDDEN,
#             )

#         serializer = ProductSerializer(product, data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def delete(self, request, pk):
#         if not request.user.is_authenticated:
#             return Response(
#                 {"error": "Authentication required"},
#                 status=status.HTTP_401_UNAUTHORIZED,
#             )

#         product = get_object_or_404(Product, pk=pk)

#         if product.seller != request.user:
#             return Response(
#                 {"error": "You can only delete your own products."},
#                 status=status.HTTP_403_FORBIDDEN,
#             )

#         product.delete()
#         return Response(
#             {"message": "Product deleted successfully"},
#             status=status.HTTP_204_NO_CONTENT,
#         )


class CategoryListAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
