from rest_framework import serializers
from .models import Blog
from comments.serializers import CommentSerializer

class BlogSerializer(serializers.ModelSerializer):
    comments = serializers.SerializerMethodField()
    
    class Meta:
        model = Blog
        fields = ['id', 'title','image','content','comments']
        
    def validate_title(self, value):
        if len(value) > 100:
            raise serializers.ValidationError("Title must be less than 100 characters long")
        return value
    
    def validate_content(self, value):
        if len(value) > 350:
            raise serializers.ValidationError("Content must be less than 350 characters long")
        return value
    
    def create(self, validated_data):
               
        user_author = validated_data.pop('user_author')        
        blog = Blog.objects.create(**validated_data)
        blog.authors.add(user_author)
        return blog
    
    def get_comments(self, obj):
        comments = getattr(obj, '_prefetched_comments', None)
        if comments is None:
            comments = obj.comments.all().order_by('-created_at')[:2]
        return CommentSerializer(comments, many=True).data