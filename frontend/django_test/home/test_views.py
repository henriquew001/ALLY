# /home/heinrich/projects/ConsciousFit/frontend/django/test/home/test_views.py

from django.test import TestCase, Client
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from django.template.loader import render_to_string

class HomeViewTest(TestCase):
    def setUp(self):
        # Create a client to make requests
        self.client = Client()

    def test_home_view_status_code(self):
        # Check if the home view returns a 200 OK status code
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_home_view_template_used(self):
        # Check if the correct template is used
        response = self.client.get(reverse('home'))
        self.assertTemplateUsed(response, 'home.html')

    def test_home_view_content_unauthenticated(self):
        # Check content for unauthenticated users
        response = self.client.get(reverse('home'))
        self.assertContains(response, _("Welcome to Consciencia Fitness!"))
        self.assertContains(response, _("You are not logged in."))
        self.assertContains(response, reverse("accounts:login"))
        self.assertContains(response, reverse("accounts:register"))
        #make sure that there is no logout-link
        self.assertNotContains(response, reverse("accounts:logout"))
        # Check that the login and register links are in the template
        rendered_template = render_to_string('home.html', {'user': response.wsgi_request.user})
        self.assertIn(reverse('accounts:login'), rendered_template)
        self.assertIn(reverse('accounts:register'), rendered_template)

    def test_home_view_content_authenticated(self):
        # Create and log in a user
        user = self.create_and_login_user()
        # Check content for authenticated users
        response = self.client.get(reverse('home'))
        self.assertContains(response, _("Welcome to Consciencia Fitness!"))
        self.assertContains(response, _("You are logged in as"))
        self.assertContains(response, user.username)
        self.assertContains(response, reverse("accounts:logout"))
        # make sure that there is no login- and register-link
        self.assertNotContains(response, reverse("accounts:login"))
        self.assertNotContains(response, reverse("accounts:register"))
        # Check that the logout link is in the template
        rendered_template = render_to_string('home.html', {'user': user})
        self.assertIn(reverse('accounts:logout'), rendered_template)

    def create_and_login_user(self):
        #helper-function to create and log in a user
        user = User.objects.create_user(username='testuser', password='ValidPassword123!', email='test@example.com')
        self.client.login(username='testuser', password='ValidPassword123!')
        return user

    def test_template_extends_base(self):
        response = self.client.get(reverse('home'))
        self.assertTemplateUsed(response, 'base.html')
    
    def test_template_block_title(self):
        response = self.client.get(reverse('home'))
        self.assertContains(response, "<title>Home</title>")

    def test_messages_include(self):
        response = self.client.get(reverse('home'))
        self.assertTemplateUsed(response, "messages.html")
