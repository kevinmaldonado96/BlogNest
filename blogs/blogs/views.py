from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status, serializers
from django.db.models import F, Window, Prefetch
from django.db.models.functions import RowNumber
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema, inline_serializer, OpenApiResponse, OpenApiParameter
from drf_spectacular.types import OpenApiTypes
from .serializers import BlogSerializer
from .models import Blog
from comments.models import Comment
from utils.task import task
from utils.paginators.paginator import StandardResultsPagination

class BlogsView(APIView):

    permission_classes = [IsAuthenticated]
    serializer_class = BlogSerializer
    pagination_class = StandardResultsPagination

    def transform_form_to_json_data(self, image_file, title, content):
        return {
            'image': image_file,
            'title': title,
            'content': content
        }
        

    @extend_schema(
        summary="Create blog",
        request={
            "multipart/form-data": inline_serializer(
            name="CreateBlog",
            fields={
                "title": serializers.CharField(),
                "content": serializers.CharField(),
                "image": serializers.ImageField(help_text="Upload an image", required=False)
            }
        )},
        responses={
            201: OpenApiResponse(
                response=BlogSerializer,
                description="Blog created succesfully"),
            400: OpenApiResponse(
                description="Bad request")           
        }
    )
    def post(self, request):  
        
        image_file = request.FILES.get('image')
        
        title = request.POST.get('title')
        content =  request.POST.get('content')  
        
        data = self.transform_form_to_json_data(image_file, title, content)
                
        serializer = self.serializer_class(data = data)
        if serializer.is_valid():
            serializer.save(user_author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @extend_schema(
        summary="Get blogs",
        responses={
            200: BlogSerializer(many=True),
            500: OpenApiResponse(
                description="Internal server error") 
        }
    )
    def get(self, request):

        try:
            paginator = self.pagination_class()
            serializer = self.serializer_class()
            
            comments_qs  = Comment.objects.annotate(
                rn=Window(
                    expression=RowNumber(),
                    partition_by=[F('blog_id')],
                    order_by=F('created_at').desc()
                )
            ).filter(rn__lte=2)
            
            print(comments_qs)
            
            prefetch = Prefetch('comments', queryset=comments_qs, to_attr='_prefetched_comments')
            print(prefetch)
            
            blogs_qs = Blog.objects.filter(authors=request.user).prefetch_related(prefetch)
            paginated_blogs = paginator.paginate_queryset(blogs_qs, request)      
                        
            serializer  = BlogSerializer(paginated_blogs, many=True)
                        
            return paginator.get_paginated_response(serializer.data) 
        except Exception as ex:
            return Response(
                {"error": "error trying to obtain blogs list"},
                status = status.HTTP_500_INTERNAL_SERVER_ERROR)

class BlogsByIdView(APIView):        
    @extend_schema(
        summary="Update blog",
        responses={
            200: BlogSerializer,
            404: OpenApiResponse(
                description="Not found"
                ),
            400: OpenApiResponse(
                description="Bad request"
                ),
            500: OpenApiResponse(
                description="Internal server error"
                ),
        }
    )
    def put(self, request, blog_id):
        try:
            image_file = request.FILES.get('image')     
            title = request.POST.get('title')
            content =  request.POST.get('content')    
            
            data = self.transform_form_to_json_data(image_file, title, content)
            
            blog_to_update = Blog.objects.filter(authors = request.user, id = blog_id).first()
            
            if not blog_to_update:
                return Response(
                    {"error": f"blog with id {blog_id} does not exist or it does not belong to the user {request.user}"},
                    status = status.HTTP_404_NOT_FOUND)
            
            blog_serializer = self.serializer_class(blog_to_update, data = data)
            if blog_serializer.is_valid():
                blog_serializer.save()
                return Response(blog_serializer.data, status=status.HTTP_200_OK)
            else:         
                print(blog_serializer.errors)
                   
                return Response(
                    {"error": "error with blog's new parameters"},
                    status = status.HTTP_400_BAD_REQUEST)
        except Exception as ex:
            print('ex'+ex)
            
            return Response(
                {"error": f"error trying to update block {blog_id}"},
                status = status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @extend_schema(
        summary="Get blog by id",
        parameters=[
            OpenApiParameter(
                name="blog_id",
                type=OpenApiTypes.INT,
                location=OpenApiParameter.PATH,
                description="Primary key of the blog"
            )
        ],
        responses={200: BlogSerializer}
    )
    def get(self, request, blog_id):        
        try:
            
            blog = Blog.objects.filter(authors = request.user, id = blog_id).first()
            if blog:
                blog_serializer = self.serializer_class(blog)
                return Response(blog_serializer.data, status=status.HTTP_200_OK)                
            else:
                return Response(
                    {"error": f"blog with id {blog_id} does not exist or it does not belong to the user {request.user}"},
                    status = status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            
            print(ex)
            return Response(
                    {"error": f"error trying to update block {blog_id}"},
                    status = status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @extend_schema(
        summary="Delete blog by id",
        parameters=[
            OpenApiParameter(
                name="blog_id",
                type=OpenApiTypes.INT,
                location=OpenApiParameter.PATH,
                description="Primary key of the blog"
            )
        ],
        responses={200: OpenApiResponse(
                description="blog succesfully delete"
                ),
                500: inline_serializer(
                    name='error trying to delete block',
                    fields={
                        "error": serializers.CharField()
                    }
            )}
    )       
    def delete(self, request, blog_id):        
        try:
            blog = get_object_or_404(Blog, id=blog_id, authors=request.user)
            blog.delete()
            return Response(f"blog succesfully delete", status=status.HTTP_204_NO_CONTENT)                
        except Exception as ex:
            print(ex)
            return Response(
                    {"error": f"error trying to delete block {blog_id}"},
                    status = status.HTTP_500_INTERNAL_SERVER_ERROR)
    
class PublishBlogView(APIView):
        
        def get(self, request, blog_id):
            try:
                task.process_blog.delay(blog_id)
                return Response(f"blog succesfully published", status=status.HTTP_204_NO_CONTENT)                

            except ValueError as vaerr:
                return Response(
                    {"error": f"error trying to publish block {blog_id} {str(vaerr)}"},
                    status = status.HTTP_400_BAD_REQUEST)
            except Exception as ex:
                print(ex)
                return Response(
                    {"error": f"error trying to publish block {blog_id} {str(ex)}"},
                    status = status.HTTP_500_INTERNAL_SERVER_ERROR)