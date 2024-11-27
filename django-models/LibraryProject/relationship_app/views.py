from django.shortcuts import render
from .models import Book

def list_books(request):
    books = Book.objects.all() # This can be used
    books = Book.objects.select_related('author').all()  # This too
    return render(request, 'relationship_app/list_books.html', {'books': books})

# -----------------------------------------------------------------------------------------

from django.views.generic.detail import DetailView
from .models import Library

class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'

# -----------------------------------------------------------------------------------------

from django.contrib.auth.views import LoginView

class UserLoginView(LoginView):
    template_name = 'relationship_app/login.html'

# -----------------------------------------------------------------------------------------

from django.contrib.auth.views import LogoutView

class UserLogoutView(LogoutView):
    template_name = 'relationship_app/logout.html'

# -----------------------------------------------------------------------------------------
# This can be used
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'relationship_app/register.html', {'form': form})

# This too
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView

class Register(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'relationship_app/register.html'


