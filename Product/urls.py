from django.urls import path
from . import views

urlpatterns = [
    path("product/", views.ProductListCreateAPIView.as_view()),
    path("product/<int:pk>/", views.ProductRetriveUpdateDestroyAPIView.as_view()),
    path("category/", views.CategoryListAPIView.as_view()),
]
