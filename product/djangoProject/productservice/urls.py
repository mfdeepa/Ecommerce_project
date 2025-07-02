from django.urls import path

from productservice.admin import ProductAdmin, CategoryAdmin
from productservice.views.category_views import CategoryRetrieveUpdateDestroyAPIView
from productservice.views.fakeStoreCategoryView import FakeStoreCategoryListCreateAPIView, \
    FakeStoreCategoryRetrieveAPIView
from productservice.views.fakeStoreProductViews import FakeStoreProductRetrieveUpdateDestroyAPIView
from productservice.views.productView import ProductRetrieveUpdateDestroyAPIView, ProductViewSet

urlpatterns = [
    path("pro_admin/", ProductViewSet.as_view({'get': 'list', 'post': 'create'}), name="ProductAdmin"),
    path("cat/", CategoryAdmin),

    path("fStore/products/", FakeStoreProductRetrieveUpdateDestroyAPIView.as_view(), name="fStore-products"),
    path("fStore/products/<int:product_id>/", FakeStoreProductRetrieveUpdateDestroyAPIView.as_view(), name="fStore-productservice-detail"),

    path("fStore/category/", FakeStoreCategoryListCreateAPIView.as_view(), name="fakeStore-categories"),
    path("fStore/category/<str:name>", FakeStoreCategoryRetrieveAPIView.as_view(), name="fakeStoreIn-category"),


    path("products/", ProductRetrieveUpdateDestroyAPIView.as_view(), name="products"),
    path("products/<int:pk>", ProductRetrieveUpdateDestroyAPIView.as_view(), name="products_details"),
    path("category/", CategoryRetrieveUpdateDestroyAPIView.as_view(), name="categories"),
    path("category/<int:pk>", CategoryRetrieveUpdateDestroyAPIView.as_view(), name="category-detail"),
]
