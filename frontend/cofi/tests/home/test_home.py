import os
from pathlib import Path
from django.test import TestCase, Client

class HomeViewTest(TestCase):
    """
    Tests the home view.
    """
    def test_home_view_status_code(self):
        """
        Test if home view returns 200 status code.
        """
        client = Client()
        response = client.get('/en/', HTTP_ACCEPT_LANGUAGE='en')  # Set the language in get
        self.assertEqual(response.status_code, 200)

    def test_home_view_has_content(self):
        """
        Test if home view returns a html file with specific content.
        """
        BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
        template_path = os.path.join(BASE_DIR, "frontend", "cofi", "home", "templates", "home", "home.html")
        client = Client()
        response = client.get('/en/', HTTP_ACCEPT_LANGUAGE='en') # Set the language in get
        self.assertContains(response, "Welcome to the Homepage!")

    def test_home_view_has_content_german(self):
        """
        Test if home view returns a html file with specific content in german.
        """
        BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
        template_path = os.path.join(BASE_DIR, "frontend", "cofi", "home", "templates", "home", "home.html")
        client = Client()
        response = client.get('/de/', HTTP_ACCEPT_LANGUAGE='de') # Set the language in get
        self.assertContains(response, "Willkommen auf der Startseite!")
