from django.urls import path
from orders.views import OrderListView, OrderDetailsView

app_name = 'orders'

urlpatterns = [
    path('orders', OrderListView.as_view(), name='order_list'),
    path('orders/<slug:pk>', OrderDetailsView.as_view(), name='order_details'),
]