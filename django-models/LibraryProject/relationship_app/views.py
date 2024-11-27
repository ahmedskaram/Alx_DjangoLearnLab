# Function-based view to list all books in a specific library.
from django.shortcuts import render
from .models import Book

def list_books(request):
    books = Book.objects.all() # This can be used
    books = Book.objects.select_related('author').all()  # This too
    return render(request, 'relationship_app/list_books.html', {'books': books})

# -----------------------------------------------------------------------------------------

#Class-based view to detail view in a specific library.
from django.views.generic.detail import DetailView
from .models import Library

class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'

# -----------------------------------------------------------------------------------------
# In this task we will not use these views (login, logout) because they are built-in.
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

# -------------------------------------------------------------------------------------------

from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_tes

def is_admin(user):
    return user.userprofile.role == 'Admin'

@user_passes_test(is_admin)
def admin_view(request):
    # This view is only accessible to users with the 'Admin' role
    return render(request, 'relationship_app/admin_view.html')  # You can customize the template as needed

def is_librarian(user):
    return user.userprofile.role == 'Librarian'

@user_passes_test(is_librarian)
def librarian_view(request):
    # This view is only accessible to users with the 'Librarian' role
    return render(request, 'relationship_app/librarian_view.html') 

def is_member(user):
    return user.userprofile.role == 'Member'

@user_passes_test(is_member)
def member_view(request):
    # This view is only accessible to users with the 'Member' role
    return render(request, 'relationship_app/member_view.html')

