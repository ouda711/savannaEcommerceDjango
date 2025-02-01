from rest_framework import generics, status
from rest_framework.response import Response
from customers.models import Customer
from customers.serializers import CustomerSerializer
from shared.renderers import AppJsonRenderer
from shared.views import ResourceListView
from users.authentication import IsAdminOrOwnerOrReadOnly
from addresses.models import Address  # Assuming Address model is relevant to customers

class CustomerListView(ResourceListView, generics.CreateAPIView):
    serializer_class = CustomerSerializer

    def get_queryset(self):
        return Customer.objects.filter(user=self.request.user)

    def get_serializer_context(self):
        serializer_context = super(CustomerListView, self).get_serializer_context()
        serializer_context['include_user'] = False  # Hide user details in list
        return serializer_context

    def get_renderers(self):
        return [AppJsonRenderer(resources_name='customers')]

    def create(self, request, *args, **kwargs):
        # Creating a new customer and associating it with the authenticated user
        serializer_context = {
            'user': request.user,
            'request': request,
            'include_user': True  # Include user details when creating a customer
        }

        request_data = request.data
        request_data['user'] = request.user  # Associate the customer with the current user

        # You can add any other necessary validation here
        serializer = self.serializer_class(data=request_data, context=serializer_context)
        serializer.is_valid(raise_exception=True)
        customer = serializer.save()

        data = {'full_messages': ['Customer created successfully']}
        data.update(CustomerSerializer(customer, context=serializer_context).data)
        return Response(data, status=status.HTTP_201_CREATED)

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
