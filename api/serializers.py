from rest_framework import serializers
from .models import Video, CustomUser, Rating, Comment

# Serializer for CustomUser model
class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'role', 'profile_picture', 'bio', 'website_url']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)  # Use create_user for hashed password
        return user



# Serializer for Video model
class VideoSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer(read_only=True)  # Nested user information
    class Meta:
        model = Video
        fields = ['id', 'title', 'content', 'video_url', 'thumbnail_url', 'duration', 'hashtags', 
                  'views', 'likes', 'comments_count', 'user', 'created_at', 'updated_at']

# Serializer for Rating model
class RatingSerializer(serializers.ModelSerializer):
    video = VideoSerializer(read_only=True)  # Nested video information
    user = CustomUserSerializer(read_only=True)  # Nested user information
    
    class Meta:
        model = Rating
        fields = ['id', 'video', 'user', 'rating', 'reaction_type', 'created_at']

# Serializer for Comment model
class CommentSerializer(serializers.ModelSerializer):
    video = VideoSerializer(read_only=True)  # Nested video information
    user = CustomUserSerializer(read_only=True)  # Nested user information
    
    class Meta:
        model = Comment
        fields = ['id', 'video', 'user', 'comment_text', 'created_at']
