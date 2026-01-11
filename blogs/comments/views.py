from django.shortcuts import render
from .serializers import CommentSerializer
from utils.paginators.paginator import CommentPagination
from .models import Comment
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status, serializers
from drf_spectacular.utils import extend_schema, OpenApiResponse, inline_serializer, OpenApiParameter
from drf_spectacular.types import OpenApiTypes

class CommentsView(APIView):
    
    permission_classes = [IsAuthenticated]
    serializer_class = CommentSerializer
    
    @extend_schema(
        summary="Create comment",
        request={
            "application/json": inline_serializer(
            name="CreateComment",
            fields={
                "blog": serializers.IntegerField(),
                "content": serializers.CharField()
            }
        )},
        responses={
            201: OpenApiResponse(
                response=CommentSerializer,
                description="comment created succesfully"),
            400: OpenApiResponse(
                description="Bad request")           
        }
    )
    def post(self, request):
        try:        
            comment_serializer = self.serializer_class(data = request.data)
            if comment_serializer.is_valid():
               comment_serializer.save(author=request.user)
               return Response(comment_serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(comment_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as ex:            
            return Response(
                {"error": f"error trying to save comment {str(ex)}"},
                status = status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @extend_schema(
        summary="Update comment",
        responses={
            201: CommentSerializer,
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
    def put(self, request, comment_id):
        
        try:                        
            comment_update = Comment.objects.filter(id = comment_id, author = request.user).first()
            
            if not comment_update:
               return Response(
                    {"error": f"comment with id {comment_id} does not exist or it does not belong to the user {request.user}"},
                    status = status.HTTP_404_NOT_FOUND)
                                   
            comment_serializer = self.serializer_class(comment_update, data = request.data)
            if comment_serializer.is_valid():
               comment_serializer.save()
               return Response(comment_serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(comment_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as ex:            
            return Response(
                {"error": "error trying to save comment"},
                status = status.HTTP_500_INTERNAL_SERVER_ERROR)
            
    @extend_schema(
        summary="Delete comment by id",
        parameters=[
            OpenApiParameter(
                name="comment_id",
                type=OpenApiTypes.INT,
                location=OpenApiParameter.PATH,
                description="Primary key of the comment"
            )
        ],
        responses={200: OpenApiResponse(
                description="comment succesfully delete"
                ),
                500: inline_serializer(
                    name='error trying to delete comment',
                    fields={
                        "error": serializers.CharField()
                    }
            )}
    )  
    def delete(self, request, comment_id):        
        try:
            comment_to_delete = get_object_or_404(Comment, id=comment_id, author=request.user)
            comment_to_delete.delete()
            return Response(f"blog succesfully delete", status=status.HTTP_204_NO_CONTENT)                
        except Exception as ex:
            print(ex)
            
            return Response(
                    {"error": f"error trying to delete comment {comment_id}"},
                    status = status.HTTP_500_INTERNAL_SERVER_ERROR)
        


class BlogCommentsListView(ListAPIView):

    permission_classes = [IsAuthenticated]
    serializer_class = CommentSerializer
    pagination_class = CommentPagination
    
    
    @extend_schema(
        summary="List comments of a blog",
        description="Returns a paginated list of comments for the given blog ID.",
        parameters=[
            OpenApiParameter(
                name="blog_id",
                type=OpenApiTypes.INT,
                location=OpenApiParameter.PATH,
                required=True,
                description="ID of the blog whose comments you want to fetch"
            ),
        ],
        responses=CommentSerializer(many=True),  
    )
    def get_queryset(self):
        blog_id = self.kwargs.get('blog_id')
        return Comment.objects.filter(blog_id = blog_id).all()
    