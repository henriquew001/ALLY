from django.test import TestCase, Client
from django.urls import reverse
import os
from pathlib import Path

class HomeViewTest(TestCase):
    def setUp(self):
        pass

    def test_home_url_resolves(self):
        """
        Test if the home URL resolves to the correct view.
        """
        url = reverse('home:home')
        self.assertEqual(url, '/')  # Changed expected URL to '/'

    def test_home_view_status_code(self):
        """
        Test if the home view returns a 200 OK status code.
        """
        client = Client()
        response = client.get('/')  # Changed URL to '/'
        self.assertEqual(response.status_code, 200)

    def test_home_view_uses_correct_template(self):
        """
        Test if the home view uses the correct template (home/home.html).
        """
        client = Client()
        response = client.get('/')  # Changed URL to '/'
        self.assertTemplateUsed(response, 'home/home.html')

    def test_home_view_has_content(self):
        """
        Test if home view returns a html file with specific content.
        """
        BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
        template_path = os.path.join(BASE_DIR, "frontend", "cofi", "home", "templates", "home", "home.html")
        client = Client()
        response = client.get('/')  # Changed URL to '/'
        self.assertContains(response, "Willkommen auf der Startseite!")