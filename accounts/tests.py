from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse

class AuthSystemTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.login_url = reverse('accounts:login')
        self.signup_url = reverse('accounts:signup')
        self.test_user = User.objects.create_user(username='testuser', password='testpassword123')

    def test_signup_visibility(self):
        # Validates routing and form loads without server crash
        response = self.client.get(self.signup_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Register")

    def test_login_flow(self):
        # Actively test standard login redirection flow
        response = self.client.post(self.login_url, {
            'username': 'testuser',
            'password': 'testpassword123'
        })
        # Should redirect to home/dashboard
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/')

    def test_logout_flow(self):
        self.client.login(username='testuser', password='testpassword123')
        response = self.client.post(reverse('accounts:logout'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/')
