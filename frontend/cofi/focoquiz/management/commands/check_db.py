from django.core.management.base import BaseCommand, CommandError
from django.db import connection
from django.conf import settings
import json
import os
import pprint  # Import pprint

class Command(BaseCommand):
    help = 'Checks the database connection and settings.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Checking database connection...'))

        # 1. Print DJANGO_SETTINGS_MODULE
        self.stdout.write(f"\nDEBUG: DJANGO_SETTINGS_MODULE = {os.environ.get('DJANGO_SETTINGS_MODULE')}")

        # 2. Print settings.DATABASES (pretty-printed with json)
        self.stdout.write("\nDEBUG: settings.DATABASES:")
        self.stdout.write(json.dumps(settings.DATABASES, indent=2))

        # 3. Print the ENTIRE settings object (using pprint)
        self.stdout.write("\nDEBUG: Entire settings object:")
        pprint.pprint(settings.__dict__)


        # 4. Check connection and variables
        try:
            with connection.cursor() as cursor:
                cursor.execute("SHOW VARIABLES LIKE 'character_set_%'")
                self.stdout.write("\nDEBUG: character_set variables:")
                for row in cursor.fetchall():
                    self.stdout.write(str(row))

                cursor.execute("SHOW VARIABLES LIKE 'collation_%'")
                self.stdout.write("\nDEBUG: collation variables:")
                for row in cursor.fetchall():
                    self.stdout.write(str(row))

                # 5. Test INSERT (with emoji)
                try:
                     # Check if any questions exist
                    cursor.execute("SELECT COUNT(*) FROM `focoquiz_question`")
                    question_count = cursor.fetchone()[0]

                    if question_count == 0:
                        self.stdout.write(self.style.WARNING("WARNING: No questions exist in the `focoquiz_question` table.  The INSERT test will likely fail."))
                        # You could choose to skip the INSERT here, or still try it
                        self.stdout.write(self.style.WARNING("Adding a default question for testing..."))
                        cursor.execute("INSERT INTO `focoquiz_question` (`text`) VALUES ('Test Question?');")

                    cursor.execute("INSERT INTO `focoquiz_choice` (`question_id`, `text`, `choice_number`) VALUES (LAST_INSERT_ID(), 'Emoji Test 🥗🍫🍕🎉📱', 1);")
                    self.stdout.write("\nDEBUG: INSERT successful (inside Django shell)")
                    cursor.execute("SELECT * from focoquiz_choice;")
                    self.stdout.write("DEBUG: SELECT results:")
                    for row in cursor.fetchall():
                        self.stdout.write(str(row))

                except Exception as e:
                    self.stdout.write(self.style.ERROR("\nDEBUG: INSERT FAILED (inside Django shell)"))
                    self.stdout.write(self.style.ERROR(f"ERROR: {e}"))

        except Exception as e:
            raise CommandError(f'Database connection failed: {e}')

        self.stdout.write(self.style.SUCCESS('\nDatabase check complete.'))
