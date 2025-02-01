from django.urls import path

from customers.views import CustomerListView, CustomerDetailsView

app_name = 'customers'

urlpatterns = [
    # Endpoint to list all customers and create a new customer
    path('customers', CustomerListView.as_view(), name='customer_list'),

    # Endpoint to retrieve, update, or delete a specific customer by ID
    path('customers/<int:pk>', CustomerDetailsView.as_view(), name='customer_details'),
]
