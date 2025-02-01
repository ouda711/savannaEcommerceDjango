from django.urls import path
from categories.views import CategoryListCreateView

app_name = 'categories'

urlpatterns = [
    path('categories', CategoryListCreateView.as_view(), name='category_create_list'),
]