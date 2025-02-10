from rest_framework import generics
from rest_framework import status, views
from rest_framework.response import Response
from django.db.models import Avg


from categories.models import Category
from categories.serializers import CategoryIdAndNameSerializer
from products.models import Product
from shared.renderers import AppJsonRenderer
from users.authentication import IsAdminOrReadOnly


class CategoryListCreateView(generics.ListCreateAPIView):
    serializer_class = CategoryIdAndNameSerializer
    permission_classes = [IsAdminOrReadOnly, ]

    def get_queryset(self):
        return Category.objects.all()

    def list(self, request, *args, **kwargs):
        serializer_context = self.get_serializer_context()
        serializer_context['request'] = request
        serializer_context['include_urls'] = True
        page = self.paginate_queryset(self.get_queryset())
        serialized_data = self.serializer_class(page, many=True, context=serializer_context)
        return self.get_paginated_response(serialized_data.data)

    def get_serializer_context(self):
        serializer_context = super(CategoryListCreateView, self).get_serializer_context()
        serializer_context['include_urls'] = True
        serializer_context['request'] = self.request
        return serializer_context

    def get_renderer_context(self):
        renderer_context = super(CategoryListCreateView, self).get_renderer_context()
        renderer_context['paginator'] = self.paginator
        return renderer_context

    def get_renderers(self):
        return [AppJsonRenderer(resources_name='tags')]

    def perform_create(self, serializer):
        super(CategoryListCreateView, self).perform_create(serializer)
        data = {'success': True, 'full_messages': ['Tag created successfully']}
        serializer.data.update(data)


class CategoryAveragePriceView(views.APIView):
    def get(self, request, category_id):
        try:
            category = Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            return Response({"error": "Category not found"}, status=status.HTTP_404_NOT_FOUND)

        avg_price = Product.objects.filter(category=category).aggregate(Avg("price"))["price__avg"]

        return Response({"category": category.name, "average_price": avg_price or 0.0}, status=status.HTTP_200_OK)