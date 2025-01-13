from django.urls import path
from .views import (
    user_login,
    VideoUploadView,
    VideoListView,
    VideoDetailView,
    like_dislike_video,
    CommentCreateView,
    register,      
    login_page,     
    home,
    play_video,
    upload_video,
    user_logout,
    register_view,
    user_login,

)
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Logout
    path('logout/', user_logout, name='logout'),

    # User registration (API)
    path('register/', register_view, name='user-register'),

    path('login/', login_page, name='login-page'),  # Renders login.html
    path('login/api/', user_login, name='user-login'),  # Handles API login

    # Video upload (API)
    path('upload_video/', upload_video, name='upload_video'),
    # path('/upload-video/', upload_video, name='upload_video'),
 
    # List all videos (API)
    path('api/videos/', VideoListView.as_view(), name='video-list'),

    # play video 
    path('play_video/<int:video_id>/', play_video, name='play_video'),


    # Video details (API - single video)
    path('api/videos/<int:id>/', VideoDetailView.as_view(), name='video-detail'),

    # Like/Dislike Video (API)
    path('api/videos/<int:video_id>/reaction/', like_dislike_video, name='like-dislike-video'),

    # Add comment to video (API)
    path('api/videos/<int:video_id>/comment/', CommentCreateView.as_view(), name='add-comment'),

    # Serve HTML pages
    path('register/', register, name='register'),  # Serve register page
    path('login/', login_page, name='login'),      # Serve login page
    path('', home, name='home'),
    path('home/', home, name='home'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
