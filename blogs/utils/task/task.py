from celery import shared_task
from blogs.models import Blog

@shared_task(bind=True, name="process_blog_task")
def process_blog(self, blog_id):

    try:
        blog = Blog.objects.get(id=blog_id)
        if blog.is_published:
           raise ValueError(f"blog {blog.title} already published")
        
        print(f"🚀 Procesando blog {blog.id}: {blog.title}")
    except Blog.DoesNotExist:
        print(f"⚠️ Blog con id {blog_id} no existe.")