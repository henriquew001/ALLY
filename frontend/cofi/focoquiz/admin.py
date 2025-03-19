# Inside your_app/admin.py (e.g., focoquiz/admin.py)

from django.contrib import admin
from .models import Question, Choice  # Import your models
from django.db import connection
from django.http import HttpResponse  # Import HttpResponse


class ChoiceInline(admin.TabularInline):  # Or StackedInline, if that's what you're using
    model = Choice
    extra = 3

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline]
    list_display = ['text']  # Example; adjust as needed

    def add_view(self, request, form_url="", extra_context=None):
        # *** TEMPORARY DEBUGGING CODE - START ***
        from django.conf import settings
        import json

        # Print the ENTIRE DATABASES setting
        print("-" * 20)
        print("DEBUG: settings.DATABASES:")
        print(json.dumps(settings.DATABASES, indent=2))  # Pretty-print
        print("-" * 20)


        # Check the connection settings directly
        with connection.cursor() as cursor:
            cursor.execute("SHOW VARIABLES LIKE 'character_set_%'")
            print("-" * 20)
            print("DEBUG: character_set variables:")
            for row in cursor.fetchall():
                print(row)
            print("-" * 20)

            cursor.execute("SHOW VARIABLES LIKE 'collation_%'")
            print("-" * 20)
            print("DEBUG: collation variables:")
            for row in cursor.fetchall():
                print(row)
            print("-" * 20)


        # *** TEMPORARY DEBUGGING CODE - END ***

        return super().add_view(request, form_url, extra_context)