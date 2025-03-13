# frontend/django_tests/test_forms.py
from django.test import TestCase
from django.contrib.auth.models import User
from accounts.forms import UserRegisterForm


class UserRegisterFormTest(TestCase):
    def test_user_registration_with_existing_username(self):
        User.objects.create_user(
            username="existinguser", email="existing@example.com", password="testpassword"
        )
        data = {
            "username": "existinguser",
            "email": "new@example.com",
            "password": "testpassword",
            "password_confirm": "testpassword",
        }
        form = UserRegisterForm(data)
        self.assertFalse(form.is_valid())
        self.assertTrue("username" in form.errors)

    def test_user_registration_with_existing_email(self):
        User.objects.create_user(
            username="existinguser", email="existing@example.com", password="testpassword"
        )
        data = {
            "username": "newuser",
            "email": "existing@example.com",
            "password": "testpassword",
            "password_confirm": "testpassword",
        }
        form = UserRegisterForm(data)
        self.assertFalse(form.is_valid())
        self.assertTrue("email" in form.errors)

    def test_clean_passwords_match(self):
        form = UserRegisterForm(
            data={
                "username": "testuser",
                "email": "test@example.com",
                "password": "testpassword",
                "password_confirm": "testpassword",
            }
        )
        form.is_valid()
        self.assertEqual(len(form.errors), 0)

    def test_clean_passwords_mismatch(self):
        form = UserRegisterForm(
            data={
                "username": "testuser",
                "email": "test@example.com",
                "password": "testpassword",
                "password_confirm": "wrongpassword",
            }
        )
        form.is_valid()
        self.assertNotEqual(len(form.errors), 0)
        self.assertTrue("password" in form.errors)
