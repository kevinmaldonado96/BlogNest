from django.contrib import admin
from django.urls import path, include
from .views import CommentsView, BlogCommentsListView


urlpatterns = [
    path('comments', CommentsView.as_view(), name='comments'),
    path('<int:comment_id>', CommentsView.as_view(), name='comments'),
    path('<int:blog_id>/comments', BlogCommentsListView.as_view(), name='comments'),
 ]