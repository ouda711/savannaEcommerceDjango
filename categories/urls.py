from django.urls import path
from categories.views import CategoryListCreateView, CategoryAveragePriceView

app_name = 'categories'

urlpatterns = [
    path('categories', CategoryListCreateView.as_view(), name='category_create_list'),
    path("categories/<int:category_id>/average-price/", CategoryAveragePriceView.as_view(), name="category-average-price"),
]