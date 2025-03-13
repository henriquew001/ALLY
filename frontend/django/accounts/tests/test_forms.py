from django.test import TestCase
from accounts.forms import UserRegisterForm
from django.contrib.auth.models import User

class UserRegisterFormTest(TestCase):
    def test_valid_form(self):
        data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "testpassword",
            "password_confirm": "testpassword",
        }
        form = UserRegisterForm(data)
        self.assertTrue(form.is_valid())
        user = form.save()
        self.assertEqual(user.username, "testuser")
        self.assertEqual(user.email, "test@example.com")
        self.assertTrue(user.check_password("testpassword"))

    def test_invalid_form_password_mismatch(self):
        data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "testpassword",
            "password_confirm": "wrongpassword",
        }
        form = UserRegisterForm(data)
        self.assertFalse(form.is_valid())
        self.assertIn("password", form.errors)

    def test_invalid_form_existing_username(self):
        User.objects.create_user(username="existinguser", email="existing@example.com", password="testpassword")
        data = {
            "username": "existinguser",
            "email": "new@example.com",
            "password": "testpassword",
            "password_confirm": "testpassword",
        }
        form = UserRegisterForm(data)
        self.assertFalse(form.is_valid())
        self.assertTrue("username" in form.errors)
    
    def test_invalid_form_existing_email(self):
        User.objects.create_user(username="existinguser", email="existing@example.com", password="testpassword")
        data = {
            "username": "newuser",
            "email": "existing@example.com",
            "password": "testpassword",
            "password_confirm": "testpassword",
        }
        form = UserRegisterForm(data)
        self.assertFalse(form.is_valid())
        self.assertTrue("email" in form.errors)
