from rest_framework import serializers
from .models import Category, Product, ProductImage


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ["id", "image", "is_primary", "created_at"]


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "description", "image", "is_active", "created_at"]


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(source="Category", read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), source="Category", write_only=True
    )
    images = ProductImageSerializer(many=True, read_only=True)
    seller = serializers.StringRelatedField(read_only=True)

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
