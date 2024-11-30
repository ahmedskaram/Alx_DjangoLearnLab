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
from django.contrib.auth.decorators import user_passes_test

def is_admin(user):
    return user.userprofile.role == 'Admin'

def is_librarian(user):
    return user.userprofile.role == 'Librarian'

def is_member(user):
    return user.userprofile.role == 'Member'

@user_passes_test(is_admin)
def admin_view(request):
    return render(request, 'relationship_app/admin_view.html')

@user_passes_test(is_librarian)
def librarian_view(request):
    return render(request, 'relationship_app/librarian_view.html')

@user_passes_test(is_member)
def member_view(request):
    return render(request, 'relationship_app/member_view.html')

# -------------------------------------------------------------------------------------------

# Custom Permissions
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import permission_required
from .models import Book
from .models import Author

# Add book View
@permission_required('relationship_app.can_add_book', raise_exception=True)
def add_book(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        author_id = request.POST.get('author_id')
        author = Author.objects.get(id=author_id)
        new_book = Book.objects.create(title=title, author=author)
        return redirect('list_books')
    return render(request, 'relationship_app/add_book.html')

# Change book View
@permission_required('relationship_app.can_change_book', raise_exception=True)
def edit_book(request, book_id):
    book = Book.objects.get(id=book_id)
    if request.method == 'POST':
        book.title = request.POST.get('title')
        book.author = Author.objects.get(id=request.POST.get('author_id'))
        book.save()
        return redirect('list_books')
    return render(request, 'relationship_app/edit_book.html', {'book': book})

# Delete book View
@permission_required('relationship_app.can_delete_book', raise_exception=True)
def delete_book(request, book_id):
    book = Book.objects.get(id=book_id)
    book.delete()
    return redirect('list_books')

# -------------------------------------------------------------------------------------------


