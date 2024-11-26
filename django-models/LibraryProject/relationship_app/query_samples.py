import django
from django.conf import settings
from relationship_app.models import Author, Book, Library, Librarian

# Set up Django settings (for running queries outside of the server)
settings.configure(DEBUG=True, DATABASES={'default': {'ENGINE': 'django.db.backends.sqlite3', 'NAME': 'db.sqlite3'}})
django.setup()

# Query all books by a specific author
def books_by_author(author_name):
    author = Author.objects.get(name=author_name) 
    books = Book.objects.filter(author=author) # Can use this
    books = author.books.all() # and can use this also
    print(f'Books by {author_name}:')
    for book in books:
        print(book.title)

# List all books in a specific library
def books_in_library(library_name):
    library = Library.objects.get(name=library_name)
    books = library.books.all()
    print(f'Books in {library_name} Library:')
    for book in books:
        print(book.title)

# Retrieve the librarian for a specific library using OneToOneField
def librarian_for_library(library_name):
    library = Library.objects.get(name=library_name) # Can use this
    librarian = library.librarian # and can use this also
    librarian = Librarian.objects.get(library=library)
    print(f'Librarian for {library_name} Library: {librarian.name}')

# Example usage
books_by_author('J.K. Rowling')
books_in_library('Central Library')
librarian_for_library('Central Library')
