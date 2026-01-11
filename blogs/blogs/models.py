from django.db import models

from django.db import models
from users.models import User
from django.utils.text import slugify
from utils.storages.storage import LocalMediaStorage


class Blog(models.Model):
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=220, unique=True, blank=True) 
    image = models.ImageField(storage=LocalMediaStorage(), blank=True, null=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)  
    updated_at = models.DateTimeField(auto_now=True)  
    is_published = models.BooleanField(default=False)

    authors = models.ManyToManyField(User, related_name="blogs")

    class Meta:
        ordering = ['-created_at'] 

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
            self.is_published = False  
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
