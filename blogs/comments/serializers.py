from rest_framework import serializers
from .models import Comment, Blog

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'blog', 'content']
        
    def validate_content(self, value):
       if len(value) > 100:
           raise serializers.ValidationError("Comment must be less than 100 characters long")
       return value
   
    def validate_blog(self, value):
        if not value.is_published:
           raise serializers.ValidationError("The blog has not yet been published.")
        return value
   
    def create(self, validated_data):
        
        comment = Comment.objects.create(**validated_data)
        return comment