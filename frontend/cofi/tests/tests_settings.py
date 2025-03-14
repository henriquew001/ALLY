# cofi/tests_settings.py

from .settings import *  # Import all existing settings

# =============================================================================
#                                 Database
# =============================================================================
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",  # In-memory database for testing
    }
}

# =============================================================================
#                                  Security
# =============================================================================
DEBUG = False
SECRET_KEY = "test_secret_key"  # Replace with a long, random string for testing

# =============================================================================
#                                  Caching
# =============================================================================

# Disable caching during testing
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.dummy.DummyCache",
    }
}

# =============================================================================
#                                  Logging
# =============================================================================

# Reduce logging verbosity
LOGGING = {
    "version": 1,
    "disable_existing_loggers": True,
    "handlers": {"console": {"class": "logging.StreamHandler"}},
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": "ERROR",  # Set to ERROR or CRITICAL for less output
        },
    },
}

# =============================================================================
#                            Static and Media Files
# =============================================================================
STATIC_ROOT = None
MEDIA_ROOT = None

# =============================================================================
#                                   Other
# =============================================================================

# Prevent from send emails
EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"

# Add any other test-specific settings below...
