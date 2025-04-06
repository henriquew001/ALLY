# products/urls.py

from django.urls import path
from . import views  # Importiert Views aus der gleichen App

app_name = 'products'  # Definiert den Namespace für diese App

urlpatterns = [
    # URL für die Produktliste (z.B. /products/)
    path('', views.product_list, name='list'),

    # URL für die Detailansicht eines einzelnen Produkts (z.B. /products/detail/123/)
    # <int:pk> erwartet eine Ganzzahl (Integer) als Primärschlüssel (pk) des Produkts
    path('detail/<int:pk>/', views.product_detail, name='detail'),

    # --- Fügen Sie hier weitere URL-Muster für Ihre Produkte hinzu ---
    # Beispiel: URL für Bundles (falls benötigt)
    # path('bundle/<int:pk>/', views.recipe_bundle_detail, name='bundle_detail'),

]
