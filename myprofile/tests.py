from django.test import TestCase
from django.urls import reverse
from myprofile.models import ProfileUser
from django.contrib.auth.models import User

class ProfileUserModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )

    def test_profile_user_creation(self):
        profile = ProfileUser.objects.create(
            user=self.user,
            name='Test Name',
            avatar='test_avatar.png',
            email='test@example.com',
            handphone='1234567890',
            bio='Test bio',
            address='Test address'
        )
        self.assertEqual(profile.user, self.user)
        self.assertEqual(profile.name, 'Test Name')
        self.assertEqual(profile.avatar, 'test_avatar.png')
        self.assertEqual(profile.email, 'test@example.com')
        self.assertEqual(profile.handphone, '1234567890')
        self.assertEqual(profile.bio, 'Test bio')
        self.assertEqual(profile.address, 'Test address')

class MyProfileURLsTestCase(TestCase):
    def test_show_profile_url(self):
        response = self.client.get(reverse('myprofile:show_profile'))
        self.assertEqual(response.status_code, 200)

    def test_complete_profile_url(self):
        response = self.client.get(reverse('myprofile:complete_profile'))
        self.assertEqual(response.status_code, 302)

    def test_update_profile_url(self):
        response = self.client.get(reverse('myprofile:update_profile'))
        self.assertEqual(response.status_code, 302)

    def test_toggle_unlike_book_url(self):
        book_id = 1
        response = self.client.get(reverse('myprofile:toggle_unlike_book', args=[book_id]))
        self.assertEqual(response.status_code, 302)