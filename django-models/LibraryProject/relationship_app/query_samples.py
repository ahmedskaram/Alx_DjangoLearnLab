from relationship_app.models import Author, Book, Library, Librarian

author = Author.objects.get(name='J.K. Rowling')
books = author.books.all()
for book in books:
    print(book.title)

library = Library.objects.get(name='Central Library')
books = library.books.all()
for book in books:
    print(book.title)

library = Library.objects.get(name='Central Library')
librarian = library.librarian
print(librarian.name)
