# frontend/django_tests/test_views.py
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib import messages
from django.utils.translation import gettext_lazy as _


class AccountsViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.register_url = reverse("accounts:register")
        self.login_url = reverse("accounts:login")
        self.logout_url = reverse("accounts:logout")
        self.home_url = reverse("home")

    def test_user_registration_success(self):
        data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "testpassword",
            "password_confirm": "testpassword",
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, 302)  # Redirect
        self.assertTrue(User.objects.filter(username="testuser").exists())
        self.assertRedirects(response, self.home_url)
        messages_list = list(messages.get_messages(response.wsgi_request))
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(
            str(messages_list[0]),
            _("Account created for testuser! You are now logged in."),
        )

    def test_user_registration_invalid_data(self):
        data = {
            "username": "testuser2",
            "email": "test2@example.com",
            "password": "testpassword",
            "password_confirm": "wrongpassword",
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username="testuser2").exists())
        messages_list = list(messages.get_messages(response.wsgi_request))
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(
            str(messages_list[0]), _("Please correct the errors below.")
        )

    def test_user_login_success(self):
        user = User.objects.create_user(username="testuser", password="testpassword")
        data = {"username": "testuser", "password": "testpassword"}
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.wsgi_request.user.is_authenticated)
        self.assertRedirects(response, self.home_url)
        messages_list = list(messages.get_messages(response.wsgi_request))
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(
            str(messages_list[0]), _(f"You are now logged in as testuser.")
        )

    def test_user_login_invalid_credentials(self):
        data = {"username": "wronguser", "password": "wrongpassword"}
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.wsgi_request.user.is_authenticated)
        messages_list = list(messages.get_messages(response.wsgi_request))
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(
            str(messages_list[0]), _("Invalid username or password.")
        )

    def test_user_logout_success(self):
        user = User.objects.create_user(username="testuser", password="testpassword")
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(self.logout_url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(response.wsgi_request.user.is_authenticated)
        self.assertRedirects(response, self.home_url)
        messages_list = list(messages.get_messages(response.wsgi_request))
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(
            str(messages_list[0]), _("You have successfully logged out.")
        )

    def test_user_logout_without_login(self):
        response = self.client.get(self.logout_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.home_url)
