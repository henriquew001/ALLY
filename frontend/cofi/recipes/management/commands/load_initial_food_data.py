from django.core.management.base import BaseCommand, CommandError
from recipes.models import Ingredient
import json

class Command(BaseCommand):
    help = 'Loads initial food data from a JSON file'

    def add_arguments(self, parser):
        parser.add_argument('json_file', type=str, help='Path to the JSON file')

    def handle(self, *args, **options):
        json_file = options['json_file']
        try:
            with open(json_file, 'r') as file:
                data = json.load(file)

            for item in data:
                #  Extract data and create Ingredient instances
                name = item.get('product_name')  # Adjust based on your JSON
                #  ... other fields ...

                if name:
                    ingredient, created = Ingredient.objects.get_or_create(
                        name=name,
                        #  ... other fields ...
                    )
                    if created:
                        self.stdout.write(self.style.SUCCESS(f'Created ingredient: {name}'))
                    else:
                        self.stdout.write(self.style.SUCCESS(f'Ingredient already exists: {name}'))

            self.stdout.write(self.style.SUCCESS('Initial data load completed'))

        except FileNotFoundError:
            raise CommandError("JSON file not found.")
        except Exception as e:
            raise CommandError(f"An error occurred: {e}")
