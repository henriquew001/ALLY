from django.contrib import admin
from django.urls import include, path
from django.conf.urls.i18n import i18n_patterns

urlpatterns = [
    path('admin/', admin.site.urls),
]

urlpatterns += i18n_patterns(
    path('', include('home.urls')),
    path('accounts/', include('authentication.urls')),
    path('accounts/', include('django.contrib.auth.urls')), # Add this line
    path('quiz/', include('focoquiz.urls')),
    path('about/', include('about.urls')),
)
