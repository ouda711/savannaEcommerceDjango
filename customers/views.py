import environ
from pathlib import Path
from django.db import transaction
from rest_framework import generics, status
from rest_framework.response import Response
from customers.models import Customer
from customers.serializers import CustomerSerializer
from savannaEcommerceDjango.settings import env
from shared.renderers import AppJsonRenderer
from shared.views import ResourceListView
from users.models import AppUser
from users.authentication import IsAdminOrOwnerOrReadOnly

class CustomerListView(ResourceListView, generics.CreateAPIView):
    BASE_DIR = Path(__file__).resolve().parent.parent
    env = environ.Env()
    environ.Env.read_env(BASE_DIR / ".env")

    serializer_class = CustomerSerializer

    def get_queryset(self):
        return Customer.objects.all()

    def get_serializer_context(self):
        serializer_context = super().get_serializer_context()
        serializer_context['include_user'] = False  # Hide user details in list
        return serializer_context

    def get_renderers(self):
        return [AppJsonRenderer(resources_name='customers')]

    def create(self, request, *args, **kwargs):
        """
        Create a new customer instance by first creating a user with a default password.
        Then associate the user with the customer.
        """
        default_password = env('DEFAULT_PASSWORD', default='Default@123')

        # Prepare user data
        user_data = {
            'email': request.data.get('email'),
            'first_name': request.data.get('first_name'),
            'last_name': request.data.get('last_name'),
            'username': request.data.get('email'),
            'password': default_password,
        }

        # Ensure required fields are present
        if not user_data['email']:
            return Response({'email': 'This field is required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            with transaction.atomic():  # Ensures rollback on failure
                # Check if user already exists
                if AppUser.objects.filter(username=user_data['username']).exists():
                    return Response({'error': 'User with this email already exists.'}, status=status.HTTP_400_BAD_REQUEST)

                # Create user
                user = AppUser.objects.create_user(**user_data)

                # Prepare customer data
                customer_data = request.data.copy()
                customer_data['user'] = user  # Pass the created user

                # Pass the context (including the user) to the serializer
                serializer = self.get_serializer(data=customer_data, context={'user': request.user})
                serializer.is_valid(raise_exception=True)
                serializer.save()

                return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)



class CustomerDetailsView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CustomerSerializer
    renderer_classes = (AppJsonRenderer,)
    permission_classes = [IsAdminOrOwnerOrReadOnly]

    def get_queryset(self):
        return Customer.objects.filter(pk=self.kwargs['pk'])

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['include_user'] = True  # Include user details in response
        return context

    def destroy(self, request, *args, **kwargs):
        response = super().destroy(request, *args, **kwargs)
        return Response({'full_messages': ['Customer removed successfully']}, status=status.HTTP_204_NO_CONTENT)
