```python
#home/test_views.py
from django.test import TestCase, Client
from django.urls import reverse
from django.utils.translation import gettext_lazy as _, override, activate, get_language
from django.contrib.auth.models import User
from django.conf import settings


class HomeViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.home_url = reverse('home')
        # Set the default language to English BEFORE any tests run. CRUCIAL!
        override(settings.LANGUAGE_CODE)

    def tearDown(self):
        # Reset the language to the default AFTER EACH TEST. Also crucial.
        activate(settings.LANGUAGE_CODE)

    def test_template_block_title(self):
        with override('en'):  # Activate the English locale
            response = self.client.get(self.home_url)
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, "<title>Home</title>")

        with override('pt-br'):  # Activate the Portuguese (Brazil) locale
            response = self.client.get(self.home_url)
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, "<title>Início</title>")

        with override('de'):  # Activate the German locale
            response = self.client.get(self.home_url)
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, "<title>Startseite</title>")

    def test_home_view_status_code(self):
        # Check if the home view returns a 200 OK status code
        response = self.client.get(self.home_url)
        self.assertEqual(response.status_code, 200)

    def test_home_view_template_used(self):
        # Check if the correct template is used
        response = self.client.get(self.home_url)
        self.assertTemplateUsed(response, 'home.html')
        self.assertTemplateUsed(response, 'base.html')

    def test_home_view_content_unauthenticated(self):
        # Check content for unauthenticated users
        with override('en'):  # Set English as default for this test
            response = self.client.get(self.home_url)
            self.assertContains(response, "Welcome to Consciencia Fitness!")
            self.assertContains(response, "You are not logged in.")
            self.assertContains(response, "href=\"/accounts/login/\"")  # Use the href attribute
            self.assertContains(response, "href=\"/accounts/register/\"")  # Use the href attribute
            self.assertNotContains(response, "href=\"/accounts/logout/\"")
            #Check that the content within the <a>-tag is correct:
            self.assertContains(response, '<a href="/accounts/login/">Login</a>')
            self.assertContains(response, '<a href="/accounts/register/">Register</a>')

    def test_home_view_content_authenticated(self):
        # Create and log in a user
        user = self.create_and_login_user()
        # Check content for authenticated users
        with override('en'):
            response = self.client.get(self.home_url)
            self.assertContains(response, "Welcome to Consciencia Fitness!")
            self.assertContains(response, f"Hello {user.username}!")  # Removed the <p> tag, because it is not in the string
            self.assertContains(response, "href=\"/accounts/logout/\"")
            self.assertNotContains(response, "href=\"/accounts/login/\"")
            self.assertNotContains(response, "href=\"/accounts/register/\"")
            self.assertContains(response, '<a href="/accounts/logout/">Logout</a>')

    def create_and_login_user(self):
        # helper-function to create and log in a user
        user = User.objects.create_user(username='testuser', password='ValidPassword123!', email='test@example.com')
        self.client.login(username='testuser', password='ValidPassword123!')
        return user

    def test_template_extends_base(self):
        response = self.client.get(self.home_url)
        self.assertTemplateUsed(response, 'base.html')

    def test_messages_include(self):
        response = self.client.get(self.home_url)
        self.assertTemplateUsed(response, "messages.html")

    def test_home_view_browser_language(self):
        # Test with German browser preference
        response = self.client.get(self.home_url, HTTP_ACCEPT_LANGUAGE='de')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(get_language(), 'de')  # Check that German is activated
        self.assertContains(response, "<title>Startseite</title>")

        # Test with Portuguese (Brazil) browser preference
        response = self.client.get(self.home_url, HTTP_ACCEPT_LANGUAGE='pt-br')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(get_language(), 'pt-br')  # Check that Portuguese is activated
        self.assertContains(response, "<title>Início</title>")

        # Test with English browser preference
        response = self.client.get(self.home_url, HTTP_ACCEPT_LANGUAGE='en-US,en;q=0.9')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(get_language(), 'en')  # Check that English is activated
        self.assertContains(response, "<title>Home</title>")

        # Test with a language not supported, should fallback to default
        response = self.client.get(self.home_url, HTTP_ACCEPT_LANGUAGE='es')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(get_language(), 'en')  # Should fallback to default
        self.assertContains(response, "<title>Home</title>")
```
