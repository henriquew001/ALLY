# frontend/django_test/home/test_views.py
from django.test import TestCase, Client
from django.urls import reverse
from django.utils.translation import override, activate
from django.contrib.auth.models import User
from django.conf import settings


class HomeViewTest(TestCase):
    def setUp(self):
        """Setup method to initialize the client and home URL."""
        self.client = Client()
        self.home_url = reverse('home')
        # Set the default language to English before each test
        override(settings.LANGUAGE_CODE)

    def tearDown(self):
        """Resets the language after each test."""
        activate(settings.LANGUAGE_CODE)

    def test_home_view_status_code(self):
        """Test if the home view returns a 200 OK status code."""
        response = self.client.get(self.home_url)
        self.assertEqual(response.status_code, 200)

    def test_home_view_template_used(self):
        """Test if the correct template is used."""
        response = self.client.get(self.home_url)
        self.assertTemplateUsed(response, 'home.html')
        self.assertTemplateUsed(response, 'base.html')

    def test_home_view_content_unauthenticated(self):
        """Test content for unauthenticated users."""
        with override('en'):  # Set English as default for this test
            #Get the Home URL in English
            home_url_en = reverse('home_lang', kwargs={'lang': 'en'})
            response = self.client.get(home_url_en)
            self.assertContains(response, "Welcome to Consciencia Fitness!")
            self.assertContains(response, "You are not logged in.")
            self.assertContains(response, 'href="/accounts/login/"')
            self.assertContains(response, 'href="/accounts/register/"')
            self.assertNotContains(response, 'href="/accounts/logout/"')
            self.assertContains(response, '<a href="/accounts/login/">Login</a>')
            self.assertContains(response, '<a href="/accounts/register/">Register</a>')
            self.assertContains(response, "<title>Home</title>")

        with override('de'):
            #Get the Home URL in German
            home_url_de = reverse('home_lang', kwargs={'lang': 'de'})
            response = self.client.get(home_url_de)
            self.assertContains(response, "Willkommen bei Consciencia Fitness!")
            self.assertContains(response, "Sie sind nicht angemeldet.") #Corrected Text!
            self.assertContains(response, '<a href="/accounts/login/">Anmeldung</a>') #Corrected Text!
            self.assertContains(response, '<a href="/accounts/register/">Registrieren</a>')
            self.assertContains(response, "<title>Startseite</title>")

    def test_home_view_content_authenticated(self):
        """Test content for authenticated users."""
        user = self.create_and_login_user()
        with override('en'):
            #Get the Home URL in English
            home_url_en = reverse('home_lang', kwargs={'lang': 'en'})
            response = self.client.get(home_url_en)
            self.assertContains(response, "Welcome to Consciencia Fitness!")
            self.assertContains(response, f"Hello {user.username}!")
            self.assertContains(response, 'href="/accounts/logout/"')
            self.assertNotContains(response, 'href="/accounts/login/"')
            self.assertNotContains(response, 'href="/accounts/register/"')
            self.assertContains(response, '<a href="/accounts/logout/">Logout</a>')
            self.assertContains(response, "<title>Home</title>")

        with override('de'):
            #Get the Home URL in German
            home_url_de = reverse('home_lang', kwargs={'lang': 'de'})
            response = self.client.get(home_url_de)
            self.assertContains(response, "Willkommen bei Consciencia Fitness!")
            self.assertContains(response, f"Hallo {user.username}!")
            self.assertContains(response, '<a href="/accounts/logout/">Abmelden</a>')
            self.assertNotContains(response, 'href="/accounts/login/"')
            self.assertNotContains(response, 'href="/accounts/register/"')
            self.assertContains(response, "<title>Startseite</title>")

    def test_template_extends_base(self):
        """Test if home.html extends base.html."""
        response = self.client.get(self.home_url)
        self.assertTemplateUsed(response, 'base.html')

    def test_messages_include(self):
        """Test if home.html includes messages.html."""
        response = self.client.get(self.home_url)
        self.assertTemplateUsed(response, "messages.html")

    def test_home_view_browser_language(self):
        """Test if the browser's preferred language is detected correctly."""

        # Test with German browser preference
        response = self.client.get(self.home_url, HTTP_ACCEPT_LANGUAGE='de')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<html lang="de">')
        self.assertContains(response, "<title>Startseite</title>")

        # Test with Portuguese (Brazil) browser preference
        response = self.client.get(self.home_url, HTTP_ACCEPT_LANGUAGE='pt-br')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<html lang="pt-br">')
        self.assertContains(response, "<title>Início</title>")

        # Test with English browser preference
        response = self.client.get(self.home_url, HTTP_ACCEPT_LANGUAGE='en-US,en;q=0.9')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<html lang="en">')
        self.assertContains(response, "<title>Home</title>")

        # Test with a language not supported, should fallback to default
        response = self.client.get(self.home_url, HTTP_ACCEPT_LANGUAGE='es')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<html lang="en">')
        self.assertContains(response, "<title>Home</title>")

    def create_and_login_user(self):
        """Helper function to create and log in a user."""
        user = User.objects.create_user(
            username='testuser',
            password='ValidPassword123!',
            email='test@example.com'
        )
        self.client.login(username='testuser', password='ValidPassword123!')
        return user
