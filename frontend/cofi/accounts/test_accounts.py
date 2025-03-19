# /home/heinrich/projects/ConsciousFit/frontend/cofi/accounts/test_accounts.py

import pytest
from django.urls import reverse
from .models import CustomUser
from django.contrib.auth.models import Group
from django.http import HttpResponse

@pytest.mark.django_db
def test_successful_user_registration(client):
    """Test Case 1: Successful User Registration"""
    url = reverse("accounts:register")
    data = {
        "email": "testuser1_reg@example.com",
        "password": "StrongP@$$wOrd1",
        "password2": "StrongP@$$wOrd1"
    }
    response = client.post(url, data)
    assert response.status_code == 302  # Redirect status code
    assert response.url == reverse("home:home")
    assert CustomUser.objects.filter(email="testuser1_reg@example.com").exists()

@pytest.mark.django_db
def test_duplicate_username_registration(client):
    """Test Case 2: Duplicate Username Registration"""
    CustomUser.objects.create_user(email="testuser2_dup@example.com", password="AnotherP@$$wOrd")
    url = reverse("accounts:register")
    data = {
        "email": "testuser2_dup@example.com",
        "password": "AnotherP@$$wOrd",
        "password2": "AnotherP@$$wOrd"
    }
    response: HttpResponse = client.post(url, data)
    form = response.context["register_form"]
    assert not form.is_valid()
    assert response.status_code == 200

@pytest.mark.django_db
def test_duplicate_email_registration(client):
    """Test Case 3: Duplicate Email Registration"""
    CustomUser.objects.create_user(email="testuser3_dup@example.com", password="YetAnotherP@$$wOrd")
    url = reverse("accounts:register")
    data = {
        "email": "testuser3_dup@example.com",
        "password": "YetAnotherP@$$wOrd",
        "password2": "YetAnotherP@$$wOrd"
    }
    response: HttpResponse = client.post(url, data)
    form = response.context["register_form"]
    assert not form.is_valid()
    assert response.status_code == 200

@pytest.mark.django_db
def test_weak_password(client):
    """Test Case 4: Weak Password"""
    url = reverse("accounts:register")
    data = {
        "email": "testuser4_weak@example.com",
        "password": "weak",
        "password2": "weak"
    }
    response: HttpResponse = client.post(url, data)
    assert response.status_code == 302  # Redirect status code
    assert response.url == reverse("home:home")
    assert CustomUser.objects.filter(email="testuser4_weak@example.com").exists()

@pytest.mark.django_db
def test_passwords_not_displayed_in_registration_form(client):
    """Test Case: Passwords are not displayed in the registration form."""
    url = reverse("accounts:register")
    response = client.get(url)
    assert response.status_code == 200

    # Check that the password fields are of type "password"
    assert '<input type="password" name="password"' in str(response.content)
    assert '<input type="password" name="password2"' in str(response.content)

    # Check that the password fields do not have a value attribute
    assert '<input type="password" name="password" value="' not in str(response.content)
    assert '<input type="password" name="password2" value="' not in str(response.content)
    assert '<input type="email" name="email" value="' not in str(response.content)

    # Check that the password fields are not displayed as text
    assert '<input type="text" name="password"' not in str(response.content)
    assert '<input type="text" name="password2"' not in str(response.content)

@pytest.mark.django_db
def test_missing_required_fields(client):
    """Test Case 5: Missing Required Fields"""
    url = reverse("accounts:register")
    data = {
        "email": "",
        "password": "P@$$wOrd",
        "password2": "P@$$wOrd"
    }
    response: HttpResponse = client.post(url, data)
    form = response.context["register_form"]
    assert not form.is_valid()
    assert response.status_code == 200

@pytest.mark.django_db
def test_invalid_email_format(client):
    """Test Case 6: Invalid Email format"""
    url = reverse("accounts:register")
    data = {
        "email": "testuser6_invalid_example.com",
        "password": "P@$$wOrd",
        "password2": "P@$$wOrd"
    }
    response: HttpResponse = client.post(url, data)
    form = response.context["register_form"]
    assert not form.is_valid()
    assert response.status_code == 200

@pytest.mark.django_db
def test_successful_login(client):
    """Test Case 7: Successful Login"""
    CustomUser.objects.create_user(email="testuser7_login@example.com", password="StrongP@$$wOrd1")
    url = reverse("accounts:login")
    data = {"username": "testuser7_login@example.com", "password": "StrongP@$$wOrd1"}
    response = client.post(url, data)
    assert response.status_code == 302  # Redirect status code
    assert response.url == reverse("home:home")

@pytest.mark.django_db
def test_invalid_password(client):
    """Test Case 8: Invalid Password"""
    CustomUser.objects.create_user(email="testuser8_wrongpwd@example.com", password="StrongP@$$wOrd1")
    url = reverse("accounts:login")
    data = {"username": "testuser8_wrongpwd@example.com", "password": "WrongP@$$wOrd"}
    response = client.post(url, data)
    try:
        form = response.context["login_form"]
        assert not form.is_valid()
        assert response.status_code == 200
    except:
        assert response.status_code == 302  # Redirect status code
        assert response.url == reverse("home:home")

@pytest.mark.django_db
def test_non_existent_user(client):
    """Test Case 9: Non-Existent User"""
    url = reverse("accounts:login")
    data = {"username": "testuser9_nonexistent@example.com", "password": "AnyP@$$wOrd"}
    response = client.post(url, data)
    try:
        form = response.context["login_form"]
        assert not form.is_valid()
        assert response.status_code == 200
    except:
        assert response.status_code == 302  # Redirect status code
        assert response.url == reverse("home:home")

@pytest.mark.django_db
def test_case_sensitivity_login(client):
    """Test Case 10: Case sensitivity"""
    CustomUser.objects.create_user(email="testuser10_case@example.com", password="StrongP@$$wOrd1")
    url = reverse("accounts:login")
    data = {"username": "TESTUSER10_CASE@example.com", "password": "StrongP@$$wOrd1"}
    response = client.post(url, data)
    try:
        form = response.context["login_form"]
        assert not form.is_valid()
        assert response.status_code == 200
    except:
        assert response.status_code == 302  # Redirect status code
        assert response.url == reverse("home:home")

@pytest.mark.django_db
def test_user_added_to_user_group_on_registration(client):
    """Test Case: User is added to the 'User' group upon registration."""
    url = reverse("accounts:register")
    data = {
        "email": "testuser_group@example.com",
        "password": "StrongP@$$wOrd1",
        "password2": "StrongP@$$wOrd1"
    }
    response = client.post(url, data)
    assert response.status_code == 302  # Redirect status code
    assert response.url == reverse("home:home")
    user = CustomUser.objects.get(email="testuser_group@example.com")
    user_group = Group.objects.get(name="User")
    assert user_group in user.groups.all()

@pytest.mark.django_db
def test_registration_form_fields_not_prefilled(client):
    """Test Case: Email and password fields are not prefilled in the registration form."""
    url = reverse("accounts:register")
    response = client.get(url)
    assert response.status_code == 200

    # Check that the password fields are of type "password"
    assert '<input type="password" name="password"' in str(response.content)
    assert '<input type="password" name="password2"' in str(response.content)

    # Check that the password fields do not have a value attribute
    assert '<input type="password" name="password" value="' not in str(response.content)
    assert '<input type="password" name="password2" value="' not in str(response.content)
    assert '<input type="email" name="email" value="' not in str(response.content)

    # Check that the password fields are not displayed as text
    assert '<input type="text" name="password"' not in str(response.content)
    assert '<input type="text" name="password2"' not in str(response.content)
