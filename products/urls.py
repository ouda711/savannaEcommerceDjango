from django.urls import path
from products.views import ProductListView, ProductDetailsView

app_name = 'products'

urlpatterns = [
    path('products/', ProductListView.as_view(), name='product_list'),
    path('products/<slug:slug>', ProductDetailsView.as_view(), name='product_details'),
    path('products/by_id/<slug:pk>', ProductDetailsView.as_view(), name='product_details_by_id'),
]
