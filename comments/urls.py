from django.urls import path
from comments.views import CommentListView, CommentDetailsView

app_name = 'comments'

urlpatterns = [
    path('products/<slug:slug>/comments', CommentListView.as_view(), name='comment_list'),
    path('comments/<slug:pk>', CommentDetailsView.as_view(), name='comment_details_short'),
    path('products/<slug:slug>/comments/<slug:pk>', CommentDetailsView.as_view(), name='comment_details'),
]