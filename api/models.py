from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

# Model for Video
class Video(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField(blank=True, null=True)
    video_file = models.FileField(upload_to='videos/', null=True)  # Save in media/videos/
    duration = models.PositiveIntegerField()
    hashtags = models.CharField(max_length=255, blank=True, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='videos', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

# Custom User model
class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('creator', 'Creator'),
        ('consumer', 'Consumer'),
    ]
    
    role = models.CharField(max_length=8, choices=ROLE_CHOICES, default='consumer')
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    website_url = models.URLField(blank=True, null=True)
    followers_count = models.PositiveIntegerField(default=0)
    following_count = models.PositiveIntegerField(default=0)
    videos_count = models.PositiveIntegerField(default=0)

    last_login_time = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    groups = models.ManyToManyField('auth.Group', related_name='customuser_set', blank=True)
    user_permissions = models.ManyToManyField('auth.Permission', related_name='customuser_permissions_set', blank=True)

    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)

    def __str__(self):
        return self.username

    def increment_followers(self):
        self.followers_count += 1
        self.save()

    def increment_following(self):
        self.following_count += 1
        self.save()

    def increment_videos_count(self):
        self.videos_count += 1
        self.save()

    def decrement_videos_count(self):
        if self.videos_count > 0:
            self.videos_count -= 1
        self.save()

# Model for Rating (Now includes likes and dislikes)
class Rating(models.Model):
    LIKE_CHOICES = [
        ('like', 'Like'),
        ('dislike', 'Dislike'),
        ('neutral', 'Neutral')
    ]

    video = models.ForeignKey(Video, related_name='ratings', on_delete=models.CASCADE)
    user = models.ForeignKey('CustomUser', related_name='ratings', on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(1, '1 Star'), (2, '2 Stars'), (3, '3 Stars'), (4, '4 Stars'), (5, '5 Stars')], null=True, blank=True)
    reaction_type = models.CharField(max_length=10, choices=LIKE_CHOICES, default='neutral', null=True, blank=True)  # Like or Dislike
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.rating:
            return f"{self.user.username} rated {self.video.title} - {self.rating} stars"
        return f"{self.user.username} reacted to {self.video.title} with {self.reaction_type}"

# Model for Comment
class Comment(models.Model):
    video = models.ForeignKey(Video, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey('CustomUser', related_name='comments', on_delete=models.CASCADE)
    comment_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.video.title}"
