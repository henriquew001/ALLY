import os
from pathlib import Path
from django.test import Client
from django.urls import reverse
import pytest

# Assuming your test file is in tests/home/test_home.py
# and your home app is in frontend/cofi/home

@pytest.mark.django_db
class HomeViewTest:
    def test_home_view_has_content(self):
        """
        Test if home view returns a html file with specific content.
        """
        client = Client()
        response = client.get('/en/', HTTP_ACCEPT_LANGUAGE='en')  # Set the language in get
        response_content = response.content.decode('utf-8')
        assert response.status_code == 200
        assert "Welcome to the Conscious Fitness!" in response_content

    def test_home_view_status_code(self):
        """
        Test if home view returns a 200 status code.
        """
        client = Client()
        response = client.get('/en/', HTTP_ACCEPT_LANGUAGE='en')
        assert response.status_code == 200

    def test_home_view_language_en(self):
        """
        Test if home view returns a html file with specific content for english.
        """
        client = Client()
        response = client.get('/en/', HTTP_ACCEPT_LANGUAGE='en')
        response_content = response.content.decode('utf-8')
        assert response.status_code == 200
        assert '<html lang="en">' in response_content
        assert "Home" in response_content
        assert "Quiz" in response_content
        assert "About" in response_content
        assert "Login" in response_content
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
        response = client.get('/de/', HTTP_ACCEPT_LANGUAGE='de')
        response_content = response.content.decode('utf-8')
        assert response.status_code == 200
        assert '<html lang="de">' in response_content
        assert "Home" in response_content
        assert "Quiz" in response_content
        assert "Über uns" in response_content
        assert "Anmelden" in response_content
        assert "Du brauchst nicht mehr Willenskraft, du brauchst Richtung!" in response_content
        assert "Interessierst du dich für ein solches Ergebnis?" in response_content
        assert "Ich möchte diese Gelegenheit nutzen" in response_content
        assert "Die Plätze sind begrenzt." in response_content
        assert "Consciência Fitness" in response_content

    def test_home_view_language_pt_br(self):
        """
        Test if home view returns a html file with specific content for portuguese.
        """
        client = Client()
        response = client.get('/pt-br/', HTTP_ACCEPT_LANGUAGE='pt-br')
        response_content = response.content.decode('utf-8')
        assert response.status_code == 200
        assert '<html lang="pt-br">' in response_content
        assert "Início" in response_content
        assert "Quiz" in response_content
        assert "Sobre" in response_content
        assert "Entrar" in response_content
        assert "Você não precisa de mais força de vontade, você precisa de direção!" in response_content
        assert "Você está interessado em um resultado como esse?" in response_content
        assert "Quero aproveitar esta oportunidade" in response_content
        assert "As vagas são limitadas." in response_content
        assert "Consciência Fitness" in response_content
