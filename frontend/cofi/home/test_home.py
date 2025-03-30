import os
from pathlib import Path
from django.test import Client, TestCase
from django.urls import reverse
import pytest
from django.conf import settings
from django.utils.translation import activate, gettext as _

# Assuming your test file is in tests/home/test_home.py
# and your home app is in frontend/cofi/home

@pytest.mark.django_db
class TestHomeView(TestCase):  # Inherit from TestCase
    def test_home_view_has_content(self):
        """
        Test if home view returns a html file with specific content.
        """
        client = Client()
        response = client.get(reverse('home:home'), HTTP_ACCEPT_LANGUAGE='en')  # Set the language in get
        response_content = response.content.decode('utf-8')
        assert response.status_code == 200
        assert "Welcome to the Conscious Fitness!" in response_content

    def test_home_view_status_code(self):
        """
        Test if home view returns a 200 status code.
        """
        client = Client()
        response = client.get(reverse('home:home'), HTTP_ACCEPT_LANGUAGE='en')
        assert response.status_code == 200

    def test_home_view_language_en(self):
        """
        Test if home view returns a html file with specific content for english.
        """
        client = Client()
        response = client.get(reverse('home:home'), HTTP_ACCEPT_LANGUAGE='en')
        response_content = response.content.decode('utf-8')
        assert response.status_code == 200
        assert '<html lang="en">' in response_content
        assert "Home" in response_content
        assert "Quiz" in response_content
        assert "About" in response_content
        assert '<i class="fas fa-user login-icon"></i>' in response_content
        assert "You don't need more willpower, you need direction!" in response_content
        assert "Are you interested in such a result?" in response_content
        assert "I want to take advantage of this opportunity" in response_content
        assert "Spots are limited." in response_content
        assert "Consciência Fitness" in response_content

    def test_home_view_language_de(self):
        """
        Test if home view returns a html file with specific content for german.
        """
        client = Client()
        
        # Set the language in the settings for the test
        with self.settings(LANGUAGE_CODE='de'):
            activate('de')
            response = client.get(reverse('home:home'), HTTP_ACCEPT_LANGUAGE='de')
            response_content = response.content.decode('utf-8')
            assert response.status_code == 200
            assert '<html lang="de">' in response_content
            assert "Startseite" in response_content # Changed to Startseite
            assert "Quiz" in response_content
            assert "Über uns" in response_content
            assert '<i class="fas fa-user login-icon"></i>' in response_content # Removed the extra slash
            # Use _() to get the translated string
            assert _("You don't need more willpower, you need direction!") in response_content
            assert _("Are you interested in such a result?") in response_content
            assert _("I want to take advantage of this opportunity") in response_content
            assert _("Spots are limited.") in response_content
            assert "Consciência Fitness" in response_content

    def test_home_view_language_pt_br(self):
        """
        Test if home view returns a html file with specific content for portuguese.
        """
        client = Client()
        with self.settings(LANGUAGE_CODE='pt-br'):
            activate('pt-br')
            response = client.get(reverse('home:home'), HTTP_ACCEPT_LANGUAGE='pt-br')
            response_content = response.content.decode('utf-8')
            assert response.status_code == 200
            assert '<html lang="pt-br">' in response_content
            assert "Início" in response_content
            assert "Quiz" in response_content
            assert "Sobre" in response_content
            assert '<i class="fas fa-user login-icon"></i>' in response_content
            assert _("You don't need more willpower, you need direction!") in response_content
            assert _("Are you interested in such a result?") in response_content
            assert _("I want to take advantage of this opportunity") in response_content
            assert _("Spots are limited.") in response_content
            assert "Consciência Fitness" in response_content
