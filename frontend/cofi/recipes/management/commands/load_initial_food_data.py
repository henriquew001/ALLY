from django.core.management.base import BaseCommand, CommandError
    from recipes.models import Ingredient
    import json

    class Command(BaseCommand):
        help = 'Loads initial food data from a JSON file'

        def handle(self, *args, **options):
            try:
                with open('path/to/your/initial_food_data.json', 'r') as file:
                    data = json.load(file)

                for item in data:
                    #  Extract data and create Ingredient instances
                    name = item.get('product_name')  # Adjust based on your JSON
                    #  ... other fields ...

                    ingredient = Ingredient.objects.create(
                        name=name,
                        #  ... other fields ...
                    )
                    self.stdout.write(self.style.SUCCESS(f'Created ingredient: {name}'))

                self.stdout.write(self.style.SUCCESS('Initial data load completed'))

            except FileNotFoundError:
                raise CommandError("JSON file not found.")
            except Exception as e:
                raise CommandError(f"An error occurred: {e}")
