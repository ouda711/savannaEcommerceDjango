from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Customer

User = get_user_model()

class CustomerSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(write_only=True)
    last_name = serializers.CharField(write_only=True)
    email = serializers.EmailField(write_only=True)
    phone = serializers.CharField()
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Customer
        fields = ['id', 'first_name', 'last_name', 'email', 'phone', 'user']

    def create(self, validated_data):
        # Extract relevant fields for user creation
        first_name = validated_data.pop('first_name')
        last_name = validated_data.pop('last_name')
        email = validated_data.pop('email')

        # Create the user with a default password
        user = User.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            username=email,  # Use email as username
            email=email,
            password="Default@123"  # Default password
        )

        # Create the customer and associate it with the user
        customer = Customer.objects.create(user=user, **validated_data)
        return customer
