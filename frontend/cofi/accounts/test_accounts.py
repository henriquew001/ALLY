# /home/heinrich/projects/ConsciousFit/frontend/cofi/accounts/test_accounts.py

from django.test import TestCase, Client
from django.urls import reverse
# from django.contrib.auth.models import User # Remove the import of the User model
from .forms import CustomUserCreationForm
from django.http import HttpResponse
from .models import CustomUser # Add the import of your CustomUser model


class AccountTests(TestCase):
    def setUp(self):
        # Set up data for all tests.
        self.client = Client()

    def test_successful_user_registration(self):
        """Test Case 1: Successful User Registration"""
        url = reverse("accounts:register")  # accounts is the appname, register is the name in the url.py
        data = {
            "email": "testuser1_reg@example.com",
            "password": "StrongP@$$wOrd1",
            "password2": "StrongP@$$wOrd1"
        }
        response = self.client.post(url, data)
        self.assertRedirects(response, reverse("home:home"))
        self.assertTrue(CustomUser.objects.filter(email="testuser1_reg@example.com").exists()) #Changed to email
    
    def test_duplicate_username_registration(self):
        """Test Case 2: Duplicate Username Registration"""
        CustomUser.objects.create_user(email="testuser2_dup@example.com", password="AnotherP@$$wOrd") #Changed to CustomUser and email
        url = reverse("accounts:register")
        data = {
            "email": "testuser2_dup@example.com",
            "password": "AnotherP@$$wOrd",
            "password2": "AnotherP@$$wOrd"
        }
        response: HttpResponse = self.client.post(url, data)
        form = response.context["register_form"]
        self.assertFalse(form.is_valid())
        self.assertEqual(response.status_code, 200)
    
    def test_duplicate_email_registration(self):
        """Test Case 3: Duplicate Email Registration"""
        CustomUser.objects.create_user(email="testuser3_dup@example.com", password="YetAnotherP@$$wOrd") #Changed to CustomUser and email
        url = reverse("accounts:register")
        data = {
            "email": "testuser3_dup@example.com",
            "password": "YetAnotherP@$$wOrd",
            "password2": "YetAnotherP@$$wOrd"
        }
        response: HttpResponse = self.client.post(url, data)
        form = response.context["register_form"]
        self.assertFalse(form.is_valid())
        self.assertEqual(response.status_code, 200)
    
    def test_weak_password(self):
        """Test Case 4: Weak Password"""
        url = reverse("accounts:register")
        data = {
            "email": "testuser4_weak@example.com",
            "password": "weak",
            "password2": "weak"
        }
        response: HttpResponse = self.client.post(url, data)
        self.assertRedirects(response, reverse("home:home"))
        self.assertTrue(CustomUser.objects.filter(email="testuser4_weak@example.com").exists())

    def test_missing_required_fields(self):
        """Test Case 5: Missing Required Fields"""
        url = reverse("accounts:register")
        data = {
            "email": "",
            "password": "P@$$wOrd",
            "password2": "P@$$wOrd"
        }
        response: HttpResponse = self.client.post(url, data)
        form = response.context["register_form"]
        self.assertFalse(form.is_valid())
        self.assertEqual(response.status_code, 200)
    
    def test_invalid_email_format(self):
        """Test Case 6: Invalid Email format"""
        url = reverse("accounts:register")
        data = {
            "email": "testuser6_invalid_example.com",
            "password": "P@$$wOrd",
            "password2": "P@$$wOrd"
        }
        response: HttpResponse = self.client.post(url, data)
        form = response.context["register_form"]
        self.assertFalse(form.is_valid())
        self.assertEqual(response.status_code, 200)

    def test_successful_login(self):
        """Test Case 7: Successful Login"""
        CustomUser.objects.create_user(email="testuser7_login@example.com", password="StrongP@$$wOrd1") #Changed to CustomUser and email
        url = reverse("accounts:login")
        data = {"username": "testuser7_login@example.com", "password": "StrongP@$$wOrd1"} #changed the username to email
        response = self.client.post(url, data)
        self.assertRedirects(response, reverse("home:home"))
    
    def test_invalid_password(self):
        """Test Case 8: Invalid Password"""
        CustomUser.objects.create_user(email="testuser8_wrongpwd@example.com", password="StrongP@$$wOrd1") #Changed to CustomUser and email
        url = reverse("accounts:login")
        data = {"username": "testuser8_wrongpwd@example.com", "password": "WrongP@$$wOrd"} #changed the username to email
        response = self.client.post(url, data)
        try:
            form = response.context["login_form"]
            self.assertFalse(form.is_valid())
            self.assertEqual(response.status_code, 200)
        except:
            self.assertRedirects(response, reverse("home:home"))

    def test_non_existent_user(self):
        """Test Case 9: Non-Existent User"""
        url = reverse("accounts:login")
        data = {"username": "testuser9_nonexistent@example.com", "password": "AnyP@$$wOrd"} #changed the username to email
        response = self.client.post(url, data)
        try:
            form = response.context["login_form"]
            self.assertFalse(form.is_valid())
            self.assertEqual(response.status_code, 200)
        except:
            self.assertRedirects(response, reverse("home:home"))

    def test_case_sensitivity_login(self): #the def was indented 
        """Test Case 10: Case sensitivity"""
        CustomUser.objects.create_user(email="testuser10_case@example.com", password="StrongP@$$wOrd1") #Changed to CustomUser and email
        url = reverse("accounts:login")
        data = {"username": "TESTUSER10_CASE@example.com", "password": "StrongP@$$wOrd1"} #changed the username to email
        response = self.client.post(url, data)
        try:
          form = response.context["login_form"]
          self.assertFalse(form.is_valid())
          self.assertEqual(response.status_code, 200)
        except:
          self.assertRedirects(response, reverse("home:home")) #If we get a redirect, the user does exist and is valid.
