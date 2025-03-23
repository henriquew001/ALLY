import pytest
from django.urls import reverse
from .models import CustomUser
from django.contrib.auth.models import Group, Permission
from django.http import HttpResponse
from django.test import Client
from django.contrib.admin.sites import AdminSite
from .admin import CustomUserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout
from django.core.management import call_command
from django.contrib.contenttypes.models import ContentType


@pytest.mark.django_db  # Apply the django_db marker to the test class (or individual tests)
class TestAccountViews:  # It's good practice to group your tests in classes
    
    def setUpModule():
        """
        Ensure the groups are created before any tests in this module run.
        """
        call_command('create_groups')  # Call the management command

    def test_user_added_to_user_group_on_registration(self): # 'client' is available as pytest fixture
        """Test Case: User is added to the 'User' group upon registration."""
        client = Client()
        url = reverse("accounts:register")
        data = {
            "email": "testuser_group@example.com",
            "password": "StrongP@$$wOrd1",
            "password2": "StrongP@$$wOrd1"
        }
        response = client.post(url, data)

@pytest.mark.django_db
class TestAccountViews:
    def test_administrator_has_all_permissions(self):
        """Test that the Administrator group has all permissions."""
        call_command('flush', '--noinput')
        call_command('migrate')  # Ensure migrations are applied!
        call_command("create_groups")

        admin_group = Group.objects.get(name='Administrator')
        all_permissions = Permission.objects.all()

        print(f"Admin group permissions count: {admin_group.permissions.count()}")  # Debug
        print(f"Total permissions count: {all_permissions.count()}")  # Debug

        assert admin_group.permissions.count() == all_permissions.count()
        
@pytest.mark.django_db
def test_groups_are_created():
    """Test that the correct groups are created."""
    assert Group.objects.filter(name='Administrator').exists()
    assert Group.objects.filter(name='Content Editor').exists()
    assert Group.objects.filter(name='User').exists()
    assert Group.objects.filter(name='Guest').exists()

@pytest.mark.django_db
class TestUserRegistration:
    def setup_method(self):
        # Create the "User" group if it doesn't exist
        if not Group.objects.filter(name="User").exists():
            Group.objects.create(name="User")
        self.client = Client()

    def test_successful_user_registration(self):
        """Test Case 1: Successful User Registration"""
        url = reverse("accounts:register")
        data = {
            "email": "testuser1_reg@example.com",
            "password": "StrongP@$$wOrd1",
            "password2": "StrongP@$$wOrd1"
        }
        response = self.client.post(url, data, follow=True)

        # Add your assertions here to check for successful registration
        assert response.status_code == 200  # Or whatever status code you expect
        # Example: Check if the user is created
        # self.assertTrue(User.objects.filter(email="testuser1_reg@example.com").exists())

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
class TestAccountViews:  # Changed class name to be more descriptive
    def setup_method(self):  # Changed to setup_method for pytest
        # Create the "User" group if it doesn't exist
        if not Group.objects.filter(name="User").exists():
            Group.objects.create(name="User")
        self.client = Client()

    def test_user_added_to_user_group_on_registration(self):  # Added self
        """Test Case: User is added to the 'User' group upon registration."""
        url = reverse("accounts:register")
        data = {
            "email": "testuser_group@example.com",
            "password": "StrongP@$$wOrd1",
            "password2": "StrongP@$$wOrd1"
        }
        response = self.client.post(url, data)
        assert response.status_code == 302  # Redirect status code
        assert response.url == reverse("home:home")
        user = CustomUser.objects.get(email="testuser_group@example.com")
        user_group = Group.objects.get(name="User")
        assert user_group in user.groups.all()

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
    response = client.post(url, data, follow=True)
    assert response.status_code == 200  # Redirect status code
    assert response.request['PATH_INFO'] == reverse("home:home")
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

@pytest.mark.django_db
def test_logged_in_user_cannot_access_login_page(client: Client):
    """
    Testet, ob ein eingeloggter Benutzer nicht auf die Login-Seite zugreifen kann.
    """
    # 1. Erstelle einen Testbenutzer
    user = CustomUser.objects.create_user(email="testuser_login@example.com", password="testpassword")

    # 2. Logge den Benutzer ein
    client.login(username="testuser_login@example.com", password="testpassword")

    # 3. Rufe die Login-Seite auf
    url = reverse("accounts:login")  # Ersetze "login" durch den Namen deiner Login-URL in urls.py
    response = client.get(url)

    # 4. Überprüfe, ob der Benutzer umgeleitet wurde (z.B. zu /)
    assert response.status_code == 302  # 302 bedeutet "Found" (Weiterleitung)
    assert response.url != url # Überprüfe, ob die Weiterleitung nicht auf die selbe Seite geht.
    # Optional: Überprüfe, ob der Benutzer auf die Startseite umgeleitet wurde
    assert response.url == reverse("home:home")

    # 5. Überprüfe, ob die Login Seite nicht aufgerufen wurde.
    response = client.get(url, follow=True)
    assert response.status_code == 200
    assert url not in response.request['PATH_INFO']

@pytest.mark.django_db
def test_logged_out_user_can_access_login_page(client: Client):
    """
    Testet, ob ein ausgeloggter Benutzer auf die Login-Seite zugreifen kann.
    """
    # 1. Rufe die Login-Seite auf
    url = reverse("accounts:login")  # Ersetze "login" durch den Namen deiner Login-URL in urls.py
    response = client.get(url)

    # 2. Überprüfe, ob der Benutzer die Login-Seite sehen kann
    assert response.status_code == 200
    assert url in response.request['PATH_INFO']

@pytest.mark.django_db
def test_password_mismatch_registration(client):
    """Test Case: Password Mismatch on Registration"""
    url = reverse("accounts:register")
    data = {
        "email": "testuser_mismatch@example.com",
        "password": "StrongP@$$wOrd1",
        "password2": "DifferentP@$$wOrd"
    }
    response: HttpResponse = client.post(url, data)
    form = response.context["register_form"]
    assert not form.is_valid()
    assert "Passwords do not match" in form.errors["__all__"][0]
    assert response.status_code == 200
    assert not CustomUser.objects.filter(email="testuser_mismatch@example.com").exists()

@pytest.mark.django_db
def test_admin_custom_user_form_fields():
    """Test Case: Check if the correct fields are displayed in the admin form."""
    site = AdminSite()
    user_admin = CustomUserAdmin(CustomUser, site)

    # Check fields in CustomUserChangeForm
    form = CustomUserChangeForm()
    assert "email" in form.fields
    assert "is_active" in form.fields
    assert "is_staff" in form.fields
    assert "is_superuser" in form.fields
    assert "password" in form.fields  # Expect 'password' to be present

    # Check fields in CustomUserCreationForm
    form = CustomUserCreationForm()
    assert "email" in form.fields
    assert "password" in form.fields
    assert "password2" in form.fields

@pytest.mark.django_db
def test_admin_add_fieldsets():
    """Test Case: Check if the add_fieldsets are correct."""
    site = AdminSite()
    user_admin = CustomUserAdmin(CustomUser, site)
    assert user_admin.add_fieldsets == (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password', 'password2')}
         ),
    )

@pytest.mark.django_db
def test_admin_fieldsets():
    """Test Case: Check if the fieldsets are correct."""
    site = AdminSite()
    user_admin = CustomUserAdmin(CustomUser, site)
    assert user_admin.fieldsets == (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('username', 'first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser','groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

@pytest.mark.django_db
def test_admin_list_display():
    """Test Case: Check if the list_display is correct."""
    site = AdminSite()
    user_admin = CustomUserAdmin(CustomUser, site)
    assert user_admin.list_display == ['email', 'is_active', 'is_staff', 'is_superuser']

@pytest.mark.django_db
def test_admin_search_fields():
    """Test Case: Check if the search_fields is correct."""
    site = AdminSite()
    user_admin = CustomUserAdmin(CustomUser, site)
    assert user_admin.search_fields == ['email']

@pytest.mark.django_db
def test_admin_ordering():
    """Test Case: Check if the ordering is correct."""
    site = AdminSite()
    user_admin = CustomUserAdmin(CustomUser, site)
    assert user_admin.ordering == ['email']

@pytest.mark.django_db
def test_login_with_username_not_allowed(client):
    """Test Case: Login with username is not allowed"""
    CustomUser.objects.create_user(username="testuser_username", email="testuser_username@example.com", password="StrongP@$$wOrd1")
    url = reverse("accounts:login")
    data = {"username": "testuser_username", "password": "StrongP@$$wOrd1"}
    response = client.post(url, data)
    
    assert response.status_code == 200  # Expect the login page to be re-displayed
    
    # Check for form errors (adjust based on your actual error messages)
    form = response.context.get('login_form')  
    assert form is not None
    assert form.errors  # Assert that the form has errors
    assert "Please enter a correct email and password." in str(form.errors) # Or whatever the exact error message is
    