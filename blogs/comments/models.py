from django.db import models
from blogs.models import Blog
from users.models import User


class Comment(models.Model):
    blog = models.ForeignKey(
        Blog, 
        related_name="comments",  
        on_delete=models.CASCADE  
    )
    author = models.ForeignKey(
        User,
        related_name="comments", 
        on_delete=models.CASCADE  
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']