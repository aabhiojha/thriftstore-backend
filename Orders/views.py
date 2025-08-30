from rest_framework.response import Response
from rest_framework.views import APIView

from Orders.models import Order, OrderItems
from Orders.serializers import OrderCreateSerializer, OrderSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework import status

from Product.models import Product


class OrderListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        orders = Order.objects.filter(buyer=request.user).order_by("-created_at")
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """It'll create a new order"""
        serializer = OrderCreateSerializer(data=request.data)
        if serializer.is_valid():
            items_data = request.data.get("items", [])
            for item in items_data:
                product = get_object_or_404(Product, id=item["product_id"])
                if not product.is_available:
                    return Response(
                        {"error": f"Product {product.name} is not available"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                if product.seller == request.user:
                    return Response(
                        {"error": "You cannot buy your own product"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )

            order = serializer.save(buyer=request.user)

            response_serializer = OrderSerializer(order)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
