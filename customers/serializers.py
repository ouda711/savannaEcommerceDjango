from rest_framework import serializers
from customers.models import Customer
from users.models import AppUser
from users.serializers import UserUsernameAndIdSerializer
from addresses.serializers import AddressSerializer  # Assuming you have an Address serializer
from orders.serializers import OrderSerializer  # Assuming you have an Order serializer

class CustomerSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    address = AddressSerializer(many=True, read_only=True)  # Include the customer's addresses
    orders = serializers.SerializerMethodField()  # Include the customer's orders

    class Meta:
        model = Customer
        fields = ['id', 'first_name', 'last_name', 'email', 'phone', 'user']

    def get_user(self, customer):
        """
        Custom method to include user data if the `include_user` flag is passed in the context
        """
        if self.context.get('include_user', False):
            return UserUsernameAndIdSerializer(customer.user).data
        return None

    def get_orders(self, customer):
        """
        Custom method to include orders if the `include_orders` flag is passed in the context
        """
        if self.context.get('include_orders', False):
            orders = customer.orders.all()
            return OrderSerializer(orders, many=True).data
        return None

    def to_representation(self, instance):
        """
        Customizes the representation to remove empty fields if necessary
        """
        response = super(CustomerSerializer, self).to_representation(instance)

        # Remove 'orders' if it is None
        if response.get('orders') is None:
            response.pop('orders')

        # Remove 'address' if it is empty
        if not response.get('address'):
            response.pop('address')

        # Remove 'user' if it is None
        if response.get('user') is None:
            response.pop('user')

        return response

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = AppUser.objects.create_user(**user_data)

        # Then create the customer and associate the created user
        customer = Customer.objects.create(user=user, **validated_data)
        return customer
