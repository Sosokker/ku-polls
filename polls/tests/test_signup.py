from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class SignUpTestCase(TestCase):
    def test_signup_view(self):
        """Test Sign Up view Load correctly or not"""
        signup_url = reverse("polls:signup")
        response = self.client.get(signup_url)
        self.assertEqual(response.status_code, 200)

    def test_signup_success(self):
        """Test the signup System, is it work or not."""
        signup_url = reverse('polls:signup')
        data = {
            'username': 'testuser',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
        }
        response = self.client.post(signup_url, data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='testuser').exists())

    def test_signup_validation_error(self):
        """Test for data validation of Sign Up form"""
        signup_url = reverse('polls:signup')
        data = {
            'username': '',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
        }
        response = self.client.post(signup_url, data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username='').exists())

    def test_redirect_after_complete_signup(self):
        signup_url = reverse("polls:signup")
        data = {
            'username': 'tester_signup',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
        }
        response = self.client.post(signup_url, data)
        self.assertRedirects(response, reverse("polls:index"))