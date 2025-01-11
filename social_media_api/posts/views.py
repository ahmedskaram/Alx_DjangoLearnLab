from rest_framework import viewsets, permissions
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from django_filters.rest_framework import DjangoFilterBackend


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.filter(author__in=following_users).order_by
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['title', 'content']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

##########################################################################################

from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import Post
from .serializers import PostSerializer

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_feed(request):
    followed_users = request.user.following.all()
    posts = Post.objects.filter(author__in=followed_users).order_by('-created_at')
    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data)

##########################################################################################

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Post, Like
from notifications.models import Notification
from django.contrib.auth import get_user_model

User = get_user_model()

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def like_post(request, post_id):
    try:
        post = Post.objects.get(id=post_id)
        # Check if the post is already liked
        if Like.objects.get_or_create(user=request.user, post=post).exists():
            return Response({'message': 'You have already liked this post.'}, status=400)
        
        # Add the like
        like = Like.objects.create(user=request.user, post=post)

        # Create a notification
        notification = Notification.objects.create(
            recipient=post.author,
            actor=request.user,
            verb='liked',
            target=post
        )

        return Response({'message': f'You liked {post.title}'}, status=200)

    except Post.DoesNotExist:
        return Response({'error': 'Post not found'}, status=404)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def unlike_post(request, post_id):
    try:
        post = Post.objects.get(id=post_id)
        like = Like.objects.filter(user=request.user, post=post).first()
        
        if not like:
            return Response({'message': 'You haven\'t liked this post yet.'}, status=400)
        
        like.delete()  # Remove the like

        return Response({'message': f'You unliked {post.title}'}, status=200)

    except Post.DoesNotExist:
        return Response({'error': 'Post not found'}, status=404)


##########################################################################################
