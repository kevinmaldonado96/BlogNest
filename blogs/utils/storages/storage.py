from django.core.files.storage import FileSystemStorage

class LocalMediaStorage(FileSystemStorage):
    location = 'blog_images'
    base_url = '/blog_images/'