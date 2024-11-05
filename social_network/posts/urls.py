from django.urls import path
from rest_framework import routers
from .views import PostListCreateView, PostDetailUpdateDeleteView, CommentListCreateView, LikeCreateView, PostImageListCreateView

router = routers.DefaultRouter()

urlpatterns = [
    path('posts/', PostListCreateView.as_view(), name='post-list-create'),
    path('posts/<int:pk>/', PostDetailUpdateDeleteView.as_view(), name='post-detail-update-delete'),
    path('posts/<int:post_id>/comments/', CommentListCreateView.as_view(), name='comment-list-create'),
    path('posts/<int:post_id>/like/', LikeCreateView.as_view(), name='like-create'),
    path('posts/<int:post_id>/images/', PostImageListCreateView.as_view(), name='post-image-list-create'),
]