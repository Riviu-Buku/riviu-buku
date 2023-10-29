from django.http import HttpRequest
from django.test import RequestFactory, TestCase
from django.core import serializers
from django.urls import reverse
from homepage.models import Book
from homepage.views import add_book_ajax, get_books, get_books_by_id, show_homepage

class HomePageTest(TestCase):
    def test_valid_request_with_books(self):
        response = self.client.get(reverse('homepage:get_books'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')
        self.assertGreater(len(response.content), 0)

    def test_returns_json_response_with_matching_book_id(self):
        book = Book.objects.first()
        response = self.client.get(reverse('homepage:get_books_by_id', args=[book.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')
        self.assertJSONEqual(response.content, serializers.serialize("json", [book]))

    def test_add_book_valid_title_author(self):
        data = {'title': 'Book Title', 'author': 'Author Name'}
        response = self.client.post(reverse('homepage:add_book_ajax'), data)
        self.assertEqual(response.status_code, 201)