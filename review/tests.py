from django.test import TestCase
from homepage.models import Book
from .views import *
from django.test import TestCase, Client
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseNotFound, JsonResponse, Http404, HttpRequest
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User  # You might need to adjust this import

class mainTest(TestCase):
    def setUp(self):
        # Create a test user for authentication
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.user.save()
        # Create a test book
        self.book = Book.objects.create(title='Test Book', author='test', description='test', rating=1, price=1, language="eng", genres="['test']"
, characters="['test']", pages=374, publisher="test", edition="test", awards="['test']",numRatings=0,coverImg="test")
        self.book.save()
        self.review = Review.objects.create(description='Test Review', user=self.user, stars=0, name="test", reply=0,upvote=0,downvote=0)
        self.review.save()
        self.book.review.add(self.review)
        self.book.liked_by_users.add(self.user)
        self.book.save()

    def test_show_review_view(self):
        # URL for the show_review view with the book's ID
        url = reverse('review:show_review', args=[self.book.id])

        # Ensure the view returns a 200 status code for an existing book
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        # Ensure the view returns a 404 status code for a non-existing book
        url_non_existing = reverse('review:show_review', args=[999])  # Assuming 999 doesn't exist
        response_non_existing = self.client.get(url_non_existing)
        self.assertEqual(response_non_existing.status_code, 404)

    def test_get_review_json_view(self):
        # URL for the get_review_json view with the book's ID
        url = reverse('review:get_review_json', args=[self.book.id])

        # Ensure the view returns a 200 status code for an existing book
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        # Ensure the view returns a 404 status code for a non-existing book
        url_non_existing = reverse('review:get_review_json', args=[999])  # Assuming 999 doesn't exist
        response_non_existing = self.client.get(url_non_existing)
        self.assertEqual(response_non_existing.status_code, 404)


    def test_show_review_view(self):
        url = reverse('review:show_review', args=[self.book.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_show_review_view_with_non_existing_book(self):
        url = reverse('review:show_review', args=[999])  # Assuming 999 doesn't exist
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_add_review_ajax_view(self):
        self.client.force_login(self.user)
        url = reverse('review:add_review_ajax', args=[self.book.id])
        response = self.client.post(url, {'description': 'New Review', 'stars': 4})
        self.assertEqual(response.status_code, 201)

    def test_add_book_like_view(self):
        self.client.force_login(self.user)
        url = reverse('review:add_book_like', args=[self.book.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 201)

    def test_add_book_unlike_view(self):
        self.client.force_login(self.user)
        url = reverse('review:add_book_unlike', args=[self.book.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 201)

    def test_get_review_json_view(self):
        url = reverse('review:get_review_json', args=[self.book.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_get_review_json_view_with_non_existing_book(self):
        url = reverse('review:get_review_json', args=[999])  # Assuming 999 doesn't exist
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_get_review_by_user_json_view(self):
        self.client.force_login(self.user)
        url = reverse('review:get_review_by_user_json', args=[self.book.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_get_liked_by_user_view(self):
        self.client.force_login(self.user)
        url = reverse('review:get_liked_by_user', args=[self.book.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_increase_upvote_ajax_view(self):
        self.client.force_login(self.user)
        url = reverse('review:increase_upvote_ajax', args=[self.review.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 201)

    def test_decrease_upvote_ajax_view(self):
        self.client.force_login(self.user)
        url = reverse('review:decrease_upvote_ajax', args=[self.review.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 201)

    def test_increase_downvote_ajax_view(self):
        self.client.force_login(self.user)
        url = reverse('review:increase_downvote_ajax', args=[self.review.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 201)

    def test_decrease_downvote_ajax_view(self):
        self.client.force_login(self.user)
        url = reverse('review:decrease_downvote_ajax', args=[self.review.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 201)

    def test_delete_review_view(self):
        self.client.force_login(self.user)
        url = reverse('review:delete_review', args=[self.review.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 201)
