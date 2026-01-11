from django.urls import path
from .views import BlogsView, BlogsByIdView, PublishBlogView


urlpatterns = [
    path('blogs', BlogsView.as_view(), name='blogs'),
    path('<int:blog_id>', BlogsByIdView.as_view(), name='blog'),
    path('publish/<int:blog_id>', PublishBlogView.as_view(), name='publish')
]