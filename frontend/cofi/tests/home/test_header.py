# /home/heinrich/projects/ConsciousFit/frontend/cofi/home/tests/test_header.py
from django.test import TestCase
from django.urls import reverse
from django.conf import settings
import os

class HeaderTest(TestCase):
    def test_logo_exists_and_has_correct_path(self):
        """Testet, ob das Logo vorhanden ist und den korrekten Pfad hat."""
        response = self.client.get('/en/')  # Korrigierter Namespace

        self.assertEqual(response.status_code, 200)

        logo_path = os.path.join(settings.STATIC_URL, 'img', 'cofi_logo_89x110.png')

        # Überprüft, ob das Logo im HTML vorhanden ist und den korrekten Pfad hat
        self.assertContains(response, f'<img src="{logo_path}" alt="Cofi Logo" class="logo">')

    def test_navigation_links_exist(self):
        """Testet, ob die Navigationslinks vorhanden sind."""
        response = self.client.get('/en/')  # Korrigierter Namespace

        self.assertEqual(response.status_code, 200)

        # Überprüft, ob die Navigationslinks vorhanden sind
        self.assertContains(response, '<a href="#">Home</a>')
        self.assertContains(response, '<a href="#">About</a>')
        self.assertContains(response, '<a href="#">Services</a>')
        self.assertContains(response, '<a href="#">Contact</a>')
    
    def test_brand_text_exists(self):
        """Testet, ob der Brand Text vorhanden ist."""
        response = self.client.get('/en/')  # Korrigierter Namespace
        self.assertEqual(response.status_code, 200)

        # Überprüft, ob die Text vorhanden ist
        self.assertContains(response, '<span class="consciencia">Consciencia</span>')
        self.assertContains(response, '<span class="fitness">Fitness</span>')

    def test_header_layout(self):
      """Testet, ob das Layout im Header korrekt ist."""
      response = self.client.get('/en/') # Korrigierter Namespace

      self.assertEqual(response.status_code, 200)

      # Überprüft, ob die Navigation unter dem Logo angezeigt wird
      self.assertContains(response, '<header>')
      self.assertContains(response, '<div class="logo-container">')
      self.assertContains(response, '<nav>')
