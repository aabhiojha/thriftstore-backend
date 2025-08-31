from rest_framework import serializers

from account.models import User
from .models import Category, Product, ProductImage


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ["id", "image", "is_primary", "created_at"]


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "description", "image", "is_active", "created_at"]


class ProductSerializerForCreate(serializers.ModelSerializer):
    # category = CategorySerializer(read_only=True)
    category = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), write_only=True
    )
    images = ProductImageSerializer(many=True, read_only=True)
    seller = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "description",
            "price",
            "condition",
            "seller",
            "is_available",
            "category",
            "category_id",
            "is_featured",
            "views_count",
            "created_at",
            "updated_at",
            "images",
        ]
        read_only_fields = [
            "id",
            "seller",
            "created_at",
            "updated_at",
            "views_count",
            "images",
        ]


class ProductSerializerForList(serializers.ModelSerializer):
    # category = CategorySerializer(read_only=True)
    category = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), write_only=True
    )
    images = ProductImageSerializer(many=True, read_only=True)
    seller = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "description",
            "price",
            "condition",
            "seller",
            "is_available",
            "category",
            "category_id",
            "is_featured",
            "views_count",
            "created_at",
            "updated_at",
            "images",
        ]
        read_only_fields = [
            "id",
            "seller",
            "created_at",
            "updated_at",
            "views_count",
            "images",
        ]


class ProductSerializerForUpdate(serializers.ModelSerializer):
    # category = CategorySerializer(read_only=True)
    category = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), write_only=True
    )
    images = ProductImageSerializer(many=True, read_only=True)
    seller = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "description",
            "price",
            "condition",
            "seller",
            "is_available",
            "category",
            "category_id",
            "is_featured",
            "views_count",
            "created_at",
            "updated_at",
            "images",
        ]
        read_only_fields = [
            "id",
            "seller",
            "created_at",
            "updated_at",
            "views_count",
            "images",
        ]
