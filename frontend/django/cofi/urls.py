# cofi/urls.py
from django.contrib import admin
from django.urls import include, path
from django.conf.urls.i18n import i18n_patterns
from django.views.generic import RedirectView  # Import RedirectView
from django.conf import settings

urlpatterns = [
    path('i18n/', include(('django.conf.urls.i18n', 'django.contrib.auth'), namespace='i18n')),
    path('accounts/', include('accounts.urls')),
    path('admin/', admin.site.urls),
    path('', include('home.urls')),
]

urlpatterns += i18n_patterns(
    path('', include('home.urls')),
    # prefix_default_language=False
)
path("", include("home.urls")),  # the home view without prefix

if settings.DEBUG:
    urlpatterns += [
        path('<str:lang_code>/', RedirectView.as_view(pattern_name='home'), name='redirect-to-home-with-prefix'),
    ]
