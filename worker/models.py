from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Blog(Base):
    __tablename__ = "blogs_blog"

    id = Column(Integer, primary_key=True, autoincrement=True)
    
    title = Column(String(200), unique=True, nullable=False)
    slug = Column(String(220), unique=True)
    image = Column(String, nullable=True)  # Guardamos la ruta o URL de la imagen
    content = Column(Text, nullable=False)

    created_at = Column(DateTime, server_default=func.now())      # auto_now_add=True
    updated_at = Column(DateTime, onupdate=func.now(), server_default=func.now())  # auto_now=True

    is_published = Column(Boolean, default=False, nullable=False)

    def __repr__(self):
        return f"<Blog id={self.id} title={self.title}>"