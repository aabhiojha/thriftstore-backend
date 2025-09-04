from django.urls import path
from . import views

urlpatterns = [
    path("category/create/", views.CategoryCreateAPIView.as_view(), name="category_create"),
    path("category/list/", views.CategoryListAPIView.as_view(), name="category_list"),
    path("product/create/", views.ProductCreateAPIView.as_view(), name="product_create"),
    path("product/list/", views.ProductListAPIView.as_view(), name="product_list"),
    path("product/retrieve/<int:pk>/", views.ProductRetrieveAPIView.as_view(), name="product_retrieve"),
    path("product/update/<int:pk>/", views.ProductUpdateAPIView.as_view(), name="product_update"),
    path("product/delete/<int:pk>/", views.ProductDeleteAPIView.as_view(), name="product_delete"),
]
