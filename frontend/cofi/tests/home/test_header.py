from django.test import TestCase, Client
from django.urls import reverse
from django.utils.translation import gettext as _


class HeaderTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_navigation_links_exist(self):
        """Testet, ob die Navigationslinks vorhanden sind."""
        response = self.client.get(reverse('home:home'))

        self.assertEqual(response.status_code, 200)

        # Überprüft, ob die Navigationslinks vorhanden sind
        self.assertContains(response, f'<a href="{reverse("home:home")}">Home</a>')
        self.assertContains(response, f'<a href="{reverse("focoquiz:quiz")}">Quiz</a>') #Anpassung!
        self.assertContains(response, f'<a href="{reverse("about")}">About</a>') # Anpassung
        self.assertContains(response, '<a href="#">Services</a>')
        self.assertContains(response, '<a href="#">Contact</a>')
    
    def test_login_link_exists_when_not_logged_in(self):
        """Testet, ob der Login-Link angezeigt wird, wenn der Benutzer nicht angemeldet ist."""
        response = self.client.get(reverse('home:home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, f'<a href="{reverse("accounts:login")}">Login</a>')
