from django.urls import path
from . import views

urlpatterns = [
    path('', views.home , name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/', views.profile, name='profile'),
]

##########################################################################################

from django.urls import path
from .views import (
    PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView
)

urlpatterns = [
    path('', PostListView.as_view(), name='post-list'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
]

##########################################################################################

from django.urls import path
from .views import CommentCreateView, CommentUpdateView, CommentDeleteView, CommentListView

urlpatterns = [
    path('post/<int:pk>/comments/new/', views.CommentCreateView.as_view() , name='create_comment'),
    path('comment/<int:pk>/update/', CommentUpdateView.as_view(), name='update-comment'),
    path('comment/<int:pk>/delete/', CommentDeleteView.as_view(), name='delete-comment'),
    path('post/<int:post_id>/comments/', CommentListView.as_view(), name='post-detail'),
]

##########################################################################################

from django.urls import path
from .views import search_posts, PostByTagListView

urlpatterns = [
    path('search/', search_posts, name='search-posts'),
    path('tags/<slug:tag_slug>/',views.PostByTagListView.as_view(),name='tags'),
]

