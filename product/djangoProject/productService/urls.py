from django.urls import path

from productService.admin import ProductAdmin, CategoryAdmin
from productService.views.category_views import CategoryRetrieveUpdateDestroyAPIView
from productService.views.fakeStoreCategoryView import FakeStoreCategoryListCreateAPIView, \
    FakeStoreCategoryRetrieveAPIView
from productService.views.fakeStoreProductViews import FakeStoreProductRetrieveUpdateDestroyAPIView
from productService.views.productView import ProductRetrieveUpdateDestroyAPIView

urlpatterns = [
    path("", ProductAdmin),
    path("cat/", CategoryAdmin),

    path("fStore/products/", FakeStoreProductRetrieveUpdateDestroyAPIView.as_view(), name="fStore-products"),
    path("fStore/products/<int:product_id>/", FakeStoreProductRetrieveUpdateDestroyAPIView.as_view(), name="fStore-product-detail"),

    path("fStore/category/", FakeStoreCategoryListCreateAPIView.as_view(), name="fakeStore-categories"),
    path("fStore/category/<str:name>", FakeStoreCategoryRetrieveAPIView.as_view(), name="fakeStoreIn-category"),


    path("products/", ProductRetrieveUpdateDestroyAPIView.as_view(), name="products"),
    path("products/<int:pk>", ProductRetrieveUpdateDestroyAPIView.as_view(), name="products"),
    path("category/", CategoryRetrieveUpdateDestroyAPIView.as_view(), name="categories"),
    path("category/<int:pk>", CategoryRetrieveUpdateDestroyAPIView.as_view(), name="category-detail"),
]
