from django.urls import path
from tags.views import TagCreateListView

app_name = 'tags'

urlpatterns = [
    path('tags', TagCreateListView.as_view(), name='tag_create_list'),
]
