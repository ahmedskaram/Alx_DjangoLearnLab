from rest_framework import routers
from .views import BookListView, DetailView, CreateView, UpdateView, DeleteView , AuthorView
from django.urls import path ,include

router = routers.DefaultRouter()
router.register(r'books', BookListView, basename='books')
router.register(r'books/<int:pk>', DetailView, basename='books_detail')
router.register(r'books/create', CreateView, basename='create')
router.register(r'books/update/<int:pk>', UpdateView, basename='update')
router.register(r'books/delete/<int:pk>', DeleteView, basename='delete')
router.register(r'users', AuthorView, basename='users')

urlpatterns =[
    path('', include(router.urls))
]
