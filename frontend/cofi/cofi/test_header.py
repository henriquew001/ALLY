from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils.translation import gettext as _
from django.utils import translation
from django.utils.translation import get_language


class HeaderTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_navigation_links_exist(self):
        """Testet, ob die Navigationslinks vorhanden sind."""
        with translation.override('en'):
            response = self.client.get(reverse('home:home'))

            self.assertEqual(response.status_code, 200)

            # Überprüft, ob die Navigationslinks vorhanden sind
            self.assertContains(response, f'<a href="{reverse("home:home")}" class="menu__item">Home</a>')
            self.assertContains(response, f'<a href="{reverse("focoquiz:quiz")}" class="menu__item">Quiz</a>')
            self.assertContains(response, f'<a href="{reverse("about:about")}" class="menu__item">About</a>')
            self.assertContains(response, '<a href="#" class="menu__item">Shop</a>')
            self.assertContains(response, '<a href="#" class="menu__item">Contact</a>')

    def test_login_link_exists_when_not_logged_in(self):
        """Testet, ob der Login-Link angezeigt wird, wenn der Benutzer nicht angemeldet ist."""
        with translation.override('en'):
            response = self.client.get(reverse('home:home'))
            self.assertEqual(response.status_code, 200)
            login_url = reverse("authentication:login")
            self.assertContains(response, f'<a href="{login_url}" class="login-icon-link">')
            self.assertContains(response, '<i class="fas fa-user login-icon"></i>')

    def test_logout_link_exists_when_logged_in(self):
        """Testet, ob der Logout-Link angezeigt wird, wenn der Benutzer angemeldet ist."""
        with translation.override('en'):
            self.client.login(username='testuser', password='testpassword')
            response = self.client.get(reverse('home:home'))
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, f'<form method="post" action="{reverse("authentication:logout")}">')
            self.assertContains(response, '<button type="submit" class="logout-link">Logout</button>')
            self.client.logout()

    def test_navigation_links_are_working(self):
        """Testet, ob die Navigationslinks funktionieren."""
        with translation.override('en'):
            response = self.client.get(reverse('home:home'))
            self.assertEqual(response.status_code, 200)

            response = self.client.get(reverse('focoquiz:quiz'))
            self.assertEqual(response.status_code, 200)

            response = self.client.get(reverse('about:about'))
            self.assertEqual(response.status_code, 200)

    def test_language_switcher_exists(self):
        """Testet, ob der Language Switcher vorhanden ist."""
        with translation.override('en'):
            response = self.client.get(reverse('home:home'))
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, '<div class="active-language-display">')
            self.assertContains(response, '<div class="language-picker">')
            self.assertContains(response, '<a href="/en/" class="language-link active" hreflang="en">')
            self.assertContains(response, '<a href="/de/" class="language-link " hreflang="de">')
            self.assertContains(response, '<a href="/pt-br/" class="language-link " hreflang="pt-br">')
