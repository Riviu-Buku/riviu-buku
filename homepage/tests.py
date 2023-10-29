from django.test import TestCase
from django.urls import reverse
from homepage.models import Book

class HomePageTest(TestCase):
    def setUp(self):
        # Create some sample books
        Book.objects.create(
            title="Book 1",
            author="Author 1",
            description="Description for Book 1",
            rating=4.5,
            price=10.0,
            language="English",
            genres=["Genre 1", "Genre 2"],
            characters=["Character 1", "Character 2"],
            edition="First Edition",
            pages=300,
            publisher="Publisher 1",
            awards=["Award 1", "Award 2"],
            numRatings=100,
            numLikes=50,
            coverImg="http://example.com/cover1.jpg",
        )
        Book.objects.create(
            title="Book 2",
            author="Author 2",
            description="Description for Book 2",
            rating=4.0,
            price=12.0,
            language="Spanish",
            genres=["Genre 2", "Genre 3"],
            characters=["Character 2", "Character 3"],
            edition="Second Edition",
            pages=250,
            publisher="Publisher 2",
            awards=["Award 3", "Award 4"],
            numRatings=80,
            numLikes=40,
            coverImg="http://example.com/cover2.jpg",
        )

    def test_homepage_loads_correctly(self):
        response = self.client.get(reverse('homepage:show_homepage'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Selamat Datang di Riviu Buku!")

    def test_search_books_by_title(self): # When searching, the link is the same as the home page link
        response = self.client.get(reverse('homepage:show_homepage'))
        self.assertNotContains(response, "Book 1")
        self.assertNotContains(response, "Book 2")

        response = self.client.get(reverse('homepage:show_homepage') + '?title=Book 1')
        self.assertNotContains(response, "Book 1")
        self.assertNotContains(response, "Book 2")

    def test_search_books_by_author(self): # Can't search book by the author
        response = self.client.get(reverse('homepage:show_homepage'))
        self.assertNotContains(response, "Author 1")
        self.assertNotContains(response, "Author 2")

        response = self.client.get(reverse('homepage:show_homepage') + '?author=Author 1')
        self.assertNotContains(response, "Author 1")
        self.assertNotContains(response, "Author 2")

    def test_get_books_endpoint(self):
        response = self.client.get(reverse('homepage:get_books'))
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), 102) # 100 data from json and 2 were created in this file test

    def test_get_books_by_id_endpoint(self):
        book = Book.objects.get(title="Book 1")
        response = self.client.get(reverse('homepage:get_books_by_id', args=[book.pk]))
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data[0]['fields']['title'], "Book 1")
        self.assertNotContains(response, "Book 2")