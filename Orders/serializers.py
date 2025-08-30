from rest_framework import serializers

from Orders.models import Order, OrderItems
from Product.models import Product
from Product.serializers import ProductSerializer


class OrderItemsSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = OrderItems
        fields = ["id", "product", "product_id", "quantity", "price"]
        read_only_fields = ["id", "product", "price"]


class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemsSerializer(many=True, read_only=True)
    buyer = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Order
        fields = [
            "id",
            "buyer",
            "order_number",
            "status",
            "order_items",
            "total_amount",
            "shipping_address",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "buyer", "order_number", "created_at", "updated_at"]


class OrderCreateSerializer(serializers.ModelSerializer):
    items = OrderItemsSerializer(many=True, write_only=True)

    class Meta:
        model = Order
        fields = ["shipping_address", "items"]

    def create(self, validated_data):
        items_data = validated_data.pop("items")
        order = Order.objects.create(**validated_data)

        total_amount = 0
        for item_data in items_data:
            product = Product.objects.get(id=item_data["product_id"])
            order_item = OrderItems.objects.create(
                order=order,
                product=product,
                quantity=item_data["quantity"],  # FIXED: Was items_data["quantity"]
                price=product.price,
            )
            total_amount += order_item.price * order_item.quantity

        order.total_amount = total_amount
        order.save()
        return order
