from celery import Celery
import os
from db import connect_to_db
from models import Blog

app = Celery('worker', broker=os.getenv('CELERY_BROKER_URL'))

session_local = connect_to_db()

@app.task(name="process_blog_task")
def process_data(blog_id):
    
    print(f"📦 Procesando datos: {blog_id}")
    blog = session_local.query(Blog).filter(Blog.id == blog_id).first()
    
    if blog:
        blog.is_published = True
        session_local.commit()
        print(f"✅ Blog con ID {blog.id} actualizado correctamente.")
    else:
        print("⚠️ Blog no encontrado.")
