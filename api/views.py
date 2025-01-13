from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from .models import Video, Rating, Comment, CustomUser
from .serializers import VideoSerializer
from rest_framework.generics import  ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import redirect
from django.contrib.auth import logout
from django.urls import reverse
from rest_framework.permissions import AllowAny
from django.contrib.auth.decorators import login_required

from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Video
from django.core.files.storage import default_storage
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from .models import CustomUser

def user_logout(request):
    # Perform any custom actions before logging out (optional)
    logout(request)  # Log out the user
    return redirect(reverse('login')) 


# User Registration View (API)
def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Simple validation
        if not username or not email or not password:
            messages.error(request, 'All fields are required.')
            return render(request, 'register.html')

        # Create the user
        try:
            user = CustomUser.objects.create_user(
                username=username,
                email=email,
                password=password
            )
            login(request, user)  # Automatically log the user in
            messages.success(request, 'User created successfully!')
            return redirect('home')  # Redirect to home or other page after registration
        except Exception as e:
            messages.error(request, f"Error creating user: {e}")
            return render(request, 'register.html')

    return render(request, 'register.html')


# View to render login.html
def login_page(request):
    return render(request, 'login.html')

# User Login View (JWT Token generation) (API)
@api_view(['POST'])
@permission_classes([AllowAny])
def user_login(request):
    username = request.data.get('username')  # Adjusted to match frontend field
    password = request.data.get('password')
    print("username:",username)
    print("password:",password)
    if not username or not password:
        return Response({'detail': 'Username and password are required'}, status=status.HTTP_400_BAD_REQUEST)

    # Authenticate the user
    user = authenticate(username=username, password=password)
    if user is None:
        return Response({'detail': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

    # Generate JWT token for the authenticated user
    refresh = RefreshToken.for_user(user)
    access_token = str(refresh.access_token)

    # Optionally, store the token in the session
    request.session['access_token'] = access_token

    # Return success response
    return Response({
        'detail': 'Login successful',
        'access_token': access_token,
        'refresh_token': str(refresh),
    }, status=status.HTTP_200_OK)

# Video Upload View (API)
class VideoUploadView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data
        data['user'] = request.user.id  # associate uploaded video with logged-in user
        serializer = VideoSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            user = request.user
            user.increment_videos_count()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Fetch All Videos (Homepage Videos)
class VideoListView(ListAPIView):
    queryset = Video.objects.all().order_by('-created_at')  # Fetch videos ordered by most recent
    serializer_class = VideoSerializer
    permission_classes = [permissions.AllowAny]

# Fetch Single Video (Play Video Page)
class VideoDetailView(RetrieveAPIView):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
    lookup_field = 'id'
    permission_classes = [permissions.AllowAny]

# Like or Dislike Video View (with Rating)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def like_dislike_video(request, video_id):
    video = Video.objects.get(id=video_id)
    reaction_type = request.data.get('reaction_type')  # 'like' or 'dislike'

    if reaction_type not in ['like', 'dislike']:
        return Response({'detail': 'Invalid reaction type'}, status=status.HTTP_400_BAD_REQUEST)

    existing_reaction = Rating.objects.filter(video=video, user=request.user, reaction_type=reaction_type).first()

    if existing_reaction:
        return Response({'detail': f'You already {reaction_type}d this video'}, status=status.HTTP_400_BAD_REQUEST)

    Rating.objects.create(video=video, user=request.user, reaction_type=reaction_type)

    if reaction_type == 'like':
        video.increment_likes()
    elif reaction_type == 'dislike':
        video.increment_likes()  # Optional: Handle dislikes differently if needed

    return Response({'detail': f'Video {reaction_type}d successfully'}, status=status.HTTP_200_OK)

# Add a Rating (1 to 5 stars) on a Video
class RatingCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, video_id):
        video = Video.objects.get(id=video_id)
        rating = request.data.get('rating')

        existing_rating = Rating.objects.filter(video=video, user=request.user).first()

        if existing_rating:
            return Response({'detail': 'You have already rated this video'}, status=status.HTTP_400_BAD_REQUEST)

        Rating.objects.create(video=video, user=request.user, rating=rating)

        return Response({'detail': 'Rating added successfully'}, status=status.HTTP_201_CREATED)

# Add a Comment on a Video
class CommentCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, video_id):
        video = Video.objects.get(id=video_id)
        comment_text = request.data.get('comment_text')

        comment = Comment.objects.create(video=video, user=request.user, comment_text=comment_text)
        video.increment_comments()

        return Response({'detail': 'Comment added successfully'}, status=status.HTTP_201_CREATED)

# Render Homepage with List of Videos
@login_required
def home(request):
    videos = Video.objects.all().order_by('-created_at')  # Latest videos first
    return render(request, 'home.html', {'videos': videos})


# Render Video Play Page
def play_video(request, video_id):
    video = Video.objects.get(id=video_id)
    ratings = Rating.objects.filter(video=video)
    comments = Comment.objects.filter(video=video)
    return render(request, 'play_video.html', {'video': video, 'ratings': ratings, 'comments': comments})



# Render Register Page
def register(request):
    return render(request, 'register.html')

# Render Login Page
def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Authenticate the user
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # Log the user in and redirect to homepage
            login(request, user)
            return redirect('home')  # Replace 'home' with the name of your homepage URL pattern
        else:
            # Add error message to the context
            messages.error(request, 'Invalid username or password')
            return render(request, 'login.html')

    # Render the login page for GET requests
    return render(request, 'login.html')


# Video upload handling view
def upload_video(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content', '')
        duration = request.POST.get('duration')
        hashtags = request.POST.get('hashtags', '')
        video_file = request.FILES.get('video-file')

        if not video_file:
            return JsonResponse({'success': False, 'error': 'No video file uploaded'})

        # Save the video to the model
        try:
            video = Video.objects.create(
                title=title,
                content=content,
                video_file=video_file,
                duration=duration,
                hashtags=hashtags,
                user=request.user
            )
            video.save()
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

    # Render the upload video page for GET requests
    return render(request, 'upload_video.html')
