from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from .models import Book
from .serializers import BookSerializer

class BookAPITests(APITestCase):

    def setUp(self):
        """
        إعداد بيانات الاختبار.
        """
        self.book1 = Book.objects.create(title="Book One", author="Author One", publication_year=2020)
        self.book2 = Book.objects.create(title="Book Two", author="Author Two", publication_year=2021)

        self.book_list_url = reverse('book-list')  # URL الرئيسي للأدوات
        self.book_detail_url = lambda pk: reverse('book-detail', args=[pk])  # URL للتفاصيل باستخدام الـ id

    def test_get_books_list(self):
        """
        اختبار عرض قائمة الكتب.
        """
        response = self.client.get(self.book_list_url)
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_create_book(self):
        """
        اختبار إضافة كتاب جديد.
        """
        data = {
            "title": "New Book",
            "author": "New Author",
            "publication_year": 2022
        }
        response = self.client.post(self.book_list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 3)  # تأكد من أن الكتاب تم إضافته

    def test_update_book(self):
        """
        اختبار تعديل كتاب.
        """
        data = {
            "title": "Updated Book",
            "author": "Updated Author",
            "publication_year": 2023
        }
        response = self.client.put(self.book_detail_url(self.book1.id), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, "Updated Book")

    def test_delete_book(self):
        """
        اختبار حذف كتاب.
        """
        response = self.client.delete(self.book_detail_url(self.book1.id))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 1)  # تأكد من أن الكتاب تم حذفه

    def test_filter_books(self):
        """
        اختبار الفلترة.
        """
        response = self.client.get(self.book_list_url, {"author": "Author One"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['author'], "Author One")

    def test_search_books(self):
        """
        اختبار البحث.
        """
        response = self.client.get(self.book_list_url, {"search": "Book One"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], "Book One")

    def test_order_books(self):
        """
        اختبار الترتيب.
        """
        response = self.client.get(self.book_list_url, {"ordering": "publication_year"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['publication_year'], 2020)  # تأكد أن الكتاب الأول هو الأقدم

