# /home/heinrich/projects/ConsciousFit/frontend/cofi/conftest.py
import pytest
from django.conf import settings
import os
import django

@pytest.fixture(scope="session", autouse=True)
def set_django_env():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cofi.settings")
    django.setup()
