# /home/heinrich/projects/ConsciousFit/frontend/cofi/accounts/tests.py

from django.test import TestCase, Client
from django.urls import reverse
from .forms import CustomUserCreationForm
from django.http import HttpResponse
from .models import CustomUser # Add the import of your CustomUser model
from django.db.models import Q

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
        self.assertTrue(CustomUser.objects.filter(username="testuser1_reg@example.com").exists()) #Changed to CustomUser
    
    def test_duplicate_email_registration(self):
        """Test Case 2: Duplicate Email Registration"""
        CustomUser.objects.create_user(username="testuser2_dup@example.com", email="testuser2_dup@example.com", password="AnotherP@$$wOrd") #Changed to CustomUser
        url = reverse("accounts:register")
        data = {
            "email": "TESTUSER2_DUP@example.com", #changed testusername
            "password": "AnotherP@$$wOrd",
            "password2": "AnotherP@$$wOrd"
        }
        response: HttpResponse = self.client.post(url, data)
        form = response.context["register_form"]
        self.assertFalse(form.is_valid())
        self.assertEqual(response.status_code, 200)
        #check if it still exists
        self.assertTrue(CustomUser.objects.filter(username="testuser2_dup@example.com").exists())
    
    def test_duplicate_email_registration_2(self):
        """Test Case 3: Duplicate Email Registration"""
        CustomUser.objects.create_user(username="testuser3_dup@example.com", email="testuser3_dup@example.com", password="YetAnotherP@$$wOrd") #Changed to CustomUser
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
        form = response.context["register_form"]
        self.assertFalse(form.is_valid())
        self.assertEqual(response.status_code, 200)

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
        CustomUser.objects.create_user(username="testuser7_login@example.com", email="testuser7_login@example.com", password="StrongP@$$wOrd1") #Changed to CustomUser
        url = reverse("accounts:login")
        data = {"username": "testuser7_login@example.com", "password": "StrongP@$$wOrd1"}
        response = self.client.post(url, data)
        self.assertRedirects(response, reverse("home:home"))
    
    def test_invalid_password(self):
        """Test Case 8: Invalid Password"""
        CustomUser.objects.create_user(username="testuser8_wrongpwd@example.com", email="testuser8_wrongpwd@example.com", password="StrongP@$$wOrd1") #Changed to CustomUser
        url = reverse("accounts:login")
        data = {"username": "testuser8_wrongpwd@example.com", "password": "WrongP@$$wOrd"}
        response = self.client.post(url, data)
        form = response.context["login_form"]
        self.assertFalse(form.is_valid())
        self.assertEqual(response.status_code, 200)

    def test_non_existent_user(self):
        """Test Case 9: Non-Existent User"""
        url = reverse("accounts:login")
        data = {"username": "testuser9_nonexistent@example.com", "password": "AnyP@$$wOrd"}
        response = self.client.post(url, data)
        form = response.context["login_form"]
        self.assertFalse(form.is_valid())
        self.assertEqual(response.status_code, 200)

    def test_case_sensitivity_login(self):
        """Test Case 10: Case sensitivity"""
        CustomUser.objects.create_user(username="testuser10_case@example.com", email="testuser10_case@example.com", password="StrongP@$$wOrd1") #Changed to CustomUser
        url = reverse("accounts:login")
        data = {"username": "TESTUSER10_CASE@EXAMPLE.COM", "password": "StrongP@$$wOrd1"}
        response = self.client.post(url, data)
        self.assertRedirects(response, reverse("home:home")) #Changed to assertRedirects
