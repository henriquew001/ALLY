from django.test import TestCase
from django.contrib.auth.models import User
from accounts.forms import UserRegisterForm
from django.utils.translation import gettext_lazy as _
from django.db.utils import IntegrityError

class UserRegisterFormTest(TestCase):
    def test_user_registration_with_valid_data(self):
        data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'password123',
            'password_confirm': 'password123',
        }
        form = UserRegisterForm(data)
        self.assertTrue(form.is_valid())
        user = form.save()
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.email, 'test@example.com')
        self.assertNotEqual(user.password, 'password123')

    def test_user_registration_with_existing_email(self):
        # Create a user with an email, so that the email exists.
        user = User.objects.create_user(username='existinguser', password='password123', email='existing@example.com')
        
        data = {
            'username': 'newuser',
            'email': 'existing@example.com',
            'password': 'password123',
            'password_confirm': 'password123',
        }
        form = UserRegisterForm(data)
        self.assertFalse(form.is_valid())
        self.assertTrue("email" in form.errors)

    def test_clean_passwords_mismatch(self):
        data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'password123',
            'password_confirm': 'differentpassword',
        }
        form = UserRegisterForm(data)
        self.assertFalse(form.is_valid())
        self.assertTrue("password" in form.errors)

    def test_user_registration_with_invalid_email(self):
        data = {
            'username': 'testuser',
            'email': 'invalid-email',
            'password': 'password123',
            'password_confirm': 'password123',
        }
        form = UserRegisterForm(data)
        self.assertFalse(form.is_valid())
        self.assertTrue("email" in form.errors)

    def test_user_registration_with_empty_username(self):
        data = {
            'username': '',
            'email': 'test@example.com',
            'password': 'password123',
            'password_confirm': 'password123',
        }
        form = UserRegisterForm(data)
        self.assertFalse(form.is_valid())
        self.assertTrue("username" in form.errors)

    def test_user_registration_with_empty_email(self):
        data = {
            'username': 'testuser',
            'email': '',
            'password': 'password123',
            'password_confirm': 'password123',
        }
        form = UserRegisterForm(data)
        self.assertFalse(form.is_valid())
        self.assertTrue("email" in form.errors)

    def test_user_registration_with_short_password(self):
        data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'short',
            'password_confirm': 'short',
        }
        form = UserRegisterForm(data)
        self.assertFalse(form.is_valid())
        self.assertTrue("password" in form.errors)

    def test_user_registration_with_duplicate_username(self):
        # Create a user with a username so that the username exists.
        user = User.objects.create_user(username='existinguser', password='password123', email='existing123@example.com')

        data = {
            'username': 'existinguser',
            'email': 'test@example.com',
            'password': 'password123',
            'password_confirm': 'password123',
        }
        form = UserRegisterForm(data)
        self.assertFalse(form.is_valid())
        self.assertTrue("username" in form.errors)
    
    def test_clean_email_empty(self):
        data = {
            'username': 'testuser',
            'email': '',
            'password': 'password123',
            'password_confirm': 'password123',
        }
        form = UserRegisterForm(data)
        self.assertFalse(form.is_valid())
        self.assertTrue("email" in form.errors)
    
    def test_clean_username_empty(self):
        data = {
            'username': '',
            'email': 'test@example.com',
            'password': 'password123',
            'password_confirm': 'password123',
        }
        form = UserRegisterForm(data)
        self.assertFalse(form.is_valid())
        self.assertTrue("username" in form.errors)
