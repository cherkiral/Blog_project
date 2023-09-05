from django.contrib import admin
from django.urls import path
from blog.views import (home,
                        about,
                        PostListView,
                        PostDetailView,
                        PostCreateView,
                        PostUpdateView,
                        PostDeleteView,
                        CommentCreateView,
                        CommentUpdateView,
                        CommentDetailView,
                        CommentDeleteView
)

urlpatterns = [
    # path('', home, name='blog_home'),
    path('', PostListView.as_view(), name='blog_home'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post_update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),
    path('post/create/', PostCreateView.as_view(), name='post_create'),
    path('post/<int:pk>/comments/create/', CommentCreateView.as_view(), name='comment_create'),
    path('comments/<pk>/', CommentDetailView.as_view(), name='comment_detail'),
    path('comments/<pk>/update/', CommentUpdateView.as_view(), name='comment_update'),
    path('comments/<pk>/delete/', CommentDeleteView.as_view(), name='comment_delete'),

    path('about/', about, name='blog_about'),
]