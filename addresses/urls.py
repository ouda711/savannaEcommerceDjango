from django.urls import path
from addresses.views import AddressListView

app_name = 'addresses'

urlpatterns = [
    path('users/addresses/', AddressListView.as_view(), name='address_list'),
]
