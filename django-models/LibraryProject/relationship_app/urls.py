from django.urls import path
from .views import list_books, LibraryDetailView

urlpatterns = [
    path('books/', list_books, name='list_books'),
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),

]

# -----------------------------------------------------------------------------------------

from django.urls import path
from .views import UserLoginView, UserLogoutView, register

urlpatterns = [
    path('login/', UserLoginView.as_v_view(template_name='relationship_app/login.html'), name='login'),
    path('logout/', UserLogoutView.as_view(template_name='relationship_app/logout.html'), name='logout'),
    path('register/', register, name='register'),
]

# -----------------------------------------------------------------------------------------


