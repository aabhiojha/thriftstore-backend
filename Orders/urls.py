from django.urls import path

from Orders.views import OrderListCreateAPIView

urlpatterns = [
    path("orders/", OrderListCreateAPIView.as_view(), name="order-list-create"),
]
