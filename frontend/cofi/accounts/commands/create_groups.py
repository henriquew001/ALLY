# frontend/cofi/accounts/commands/create_groups.py

from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

class Command(BaseCommand):
    help = 'Creates the default groups and permissions'

    def handle(self, *args, **options):
        # Create groups
        admin_group, created = Group.objects.get_or_create(name='Administrator')
        content_editor_group, created = Group.objects.get_or_create(name='Content Editor')
        user_group, created = Group.objects.get_or_create(name='User')
        guest_group, created = Group.objects.get_or_create(name='Guest')

        # Assign all permissions to the Administrator group
        all_permissions = Permission.objects.all()
        admin_group.permissions.set(all_permissions)
        self.stdout.write(self.style.SUCCESS('Successfully added all permissions to the Administrator group.'))

        # Content Editor Permissions for CMS
        content_editor_permissions = []
        cms_models = ['recipe', 'lesson', 'additionalmaterial', 'package']  # Add your CMS models here

        for model_name in cms_models:
            try:
                content_type = ContentType.objects.get(app_label='cms', model=model_name) # Assuming your CMS models are in the 'cms' app
                add_perm = Permission.objects.get(codename=f'add_{model_name}', content_type=content_type)
                change_perm = Permission.objects.get(codename=f'change_{model_name}', content_type=content_type)
                delete_perm = Permission.objects.get(codename=f'delete_{model_name}', content_type=content_type)
                view_perm = Permission.objects.get(codename=f'view_{model_name}', content_type=content_type)

                content_editor_permissions.extend([add_perm, change_perm, delete_perm, view_perm])
                self.stdout.write(self.style.SUCCESS(f'Successfully added Content Editor permissions for {model_name}.'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error adding Content Editor permissions for {model_name}. Ensure your models are correct! Details: {e}'))

        content_editor_group.permissions.set(content_editor_permissions)
        self.stdout.write(self.style.SUCCESS('Successfully added Content Editor permissions for CMS.'))

        # Guest Permissions (View only for examples)
        guest_view_permissions = []
        guest_view_models = ['recipe', 'lesson', 'additionalmaterial', 'package'] # You can specify which models guests can view
        for model_name in guest_view_models:
            try:
                content_type = ContentType.objects.get(app_label='cms', model=model_name)
                view_perm = Permission.objects.get(codename=f'view_{model_name}', content_type=content_type)
                guest_view_permissions.append(view_perm)
                self.stdout.write(self.style.SUCCESS(f'Successfully added Guest view permission for {model_name}.'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error adding Guest view permission for {model_name}. Ensure your models are correct! Details: {e}'))
        guest_group.permissions.set(guest_view_permissions)
        self.stdout.write(self.style.SUCCESS('Successfully added Guest permissions.'))

        self.stdout.write(self.style.SUCCESS('Successfully created or updated groups and permissions.'))
