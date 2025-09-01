from django.urls import path
from . import views

urlpatterns = [
    # path("product/", views.ProductListCreateAPIView.as_view()),
    path("/product/list", views.ProductListAPIView.as_view()),
    path("/product/create", views.ProductCreateAPIView.as_view()),
    path("/product/retrieve/<int:pk>", views.ProductRetrieveAPIView.as_view()),
    path("/product/update/<int:pk>", views.ProductUpdateAPIView.as_view()),
    path("/product/delete/<int:pk>", views.ProductDeleteAPIView.as_view()),
    path("/category", views.CategoryListAPIView.as_view()),
]
