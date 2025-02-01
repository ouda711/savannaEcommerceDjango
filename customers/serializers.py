from rest_framework import serializers
from customers.models import Customer
from users.serializers import UserUsernameAndIdSerializer
from addresses.serializers import AddressSerializer  # Assuming you have an Address serializer
from orders.serializers import OrderSerializer  # Assuming you have an Order serializer

class CustomerSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    address = AddressSerializer(many=True, read_only=True)  # Include the customer's addresses
    orders = serializers.SerializerMethodField()  # Include the customer's orders

    class Meta:
        model = Customer
        fields = ['id', 'first_name', 'last_name', 'email', 'phone', 'created_at', 'updated_at', 'user', 'address', 'orders']

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
        """
        Custom create method to associate the customer with a user and set default fields
        """
        user = self.context['user']
        customer = Customer.objects.create(
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],
            phone=validated_data['phone'],
            user=user
        )
        return customer
