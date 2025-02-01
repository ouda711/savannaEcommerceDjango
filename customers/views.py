import environ
from pathlib import Path
from rest_framework import generics, status
from rest_framework.response import Response
from customers.models import Customer
from customers.serializers import CustomerSerializer
from savannaEcommerceDjango.settings import env
from shared.renderers import AppJsonRenderer
from shared.views import ResourceListView
from users.models import AppUser
from users.authentication import IsAdminOrOwnerOrReadOnly
from addresses.models import Address  # Assuming Address model is relevant to customers

class CustomerListView(ResourceListView, generics.CreateAPIView):
    BASE_DIR = Path(__file__).resolve().parent.parent
    env = environ.Env()
    environ.Env.read_env(BASE_DIR / ".env")

    serializer_class = CustomerSerializer

    def get_queryset(self):
        return Customer.objects.all()

    def get_serializer_context(self):
        serializer_context = super(CustomerListView, self).get_serializer_context()
        serializer_context['include_user'] = False  # Hide user details in list
        return serializer_context

    def get_renderers(self):
        return [AppJsonRenderer(resources_name='customers')]

    def create(self, request, *args, **kwargs):
        """
        Create a new customer instance by first creating a user with a default password.
        Then associate the user with the customer.
        """
        # Generate a random password or use a default one
        default_password = env('DEFAULT_PASSWORD')

        # Create the user first
        user_data = {
            'username': request.data.get('email'),  # You can use the email as the username
            'email': request.data.get('email'),
            'password': default_password,
        }

        # Create the user
        user = AppUser.objects.create_user(**user_data)

        # Now create the customer
        customer_data = request.data.copy()  # Copy request data to use for customer creation
        customer_data['user'] = user.id  # Associate the created user with the customer

        # Use the serializer to create the customer
        serializer = self.get_serializer(data=customer_data, context={'user': request.user})
        if serializer.is_valid():
            serializer.save()
            # Add any custom logic if needed, e.g., sending an email with the default password

            # Return success response with the customer data
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CustomerDetailsView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CustomerSerializer
    renderer_classes = (AppJsonRenderer,)
    permission_classes = [IsAdminOrOwnerOrReadOnly]

    def get_queryset(self):
        return Customer.objects.filter(pk=self.kwargs['pk'])

    def get_serializer_context(self):
        context = super(CustomerDetailsView, self).get_serializer_context()
        context['include_user'] = True  # Include user details in response
        return context

    def destroy(self, request, *args, **kwargs):
        response = super(CustomerDetailsView, self).destroy(request, args, kwargs)
        return Response({'full_messages': ['Customer removed successfully']}, status=status.HTTP_204_NO_CONTENT)
