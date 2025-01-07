from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse , path , include
from api.models import Book , Author

# Create your tests here.

# This Python class contains test cases for creating, retrieving, updating, and deleting books using
# Django REST framework API testing.
class BookAPITestCase(APITestCase):
    urlpatterns = [
        path('api/', include('api.urls')),
        ]
    def setUp(self):
        self.author = Author.objects.create(name='Test Author')
        self.client = APIClient()
        self.client.login(username='testuser', password='testpassword')
        self.book_data = {
            'title': 'Test Book',
            'author': 'Test Author',
            'publication_year': 2021
        }
        self.create_url = reverse('CreateView')
        self.detail_url = reverse('book_detail', args=[1])
        self.update_url = reverse('update', args=[1])
        self.delete_url = reverse('delete', args=[1])

    def test_create_book(self):
        data = {'title': 'New Book', 'author': 'New Author', 'publication_year': 2022}
        response = self.client.post(self.book_list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], data['title'])

        
    def test_get_books(self):
        response = self.client.get(self.detail_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # Verify two books are returned

        
    def test_update_book(self):
        update_url = reverse('update', args=[self.book_data.id])
        data = {'title': 'Updated Book'}
        response = self.client.patch(update_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], data['title'])
        
    def test_delete_book(self):
        delete_url = reverse('book-detail', args=[self.book1.id])
        response = self.client.delete(delete_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 1)  # Verify only one book remains
        
    def test_filter_books_by_author(self):
        response = self.client.get(self.book_list_url, {'author': 'Author One'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['author'], 'Author One')
        
    def test_search_books_by_title(self):
        response = self.client.get(self.book_list_url, {'title': 'Book One'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Book One')

    def test_order_books_by_publication_year(self):
        response = self.client.get(self.book_list_url, {'ordering': 'publication_year'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['title'], 'Book One')  # Oldest book first


        
    def test_unauthenticated_access(self):
        self.client.logout()
        response = self.client.get(self.book_list_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)  # Or 401 based on your setup



