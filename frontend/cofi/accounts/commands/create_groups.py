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

        # Check if the database is empty (newly initialized)
        if Permission.objects.count() == 0:
            # Assign all permissions to the Administrator group
            all_permissions = Permission.objects.all()
            admin_group.permissions.set(all_permissions)
            self.stdout.write(self.style.SUCCESS('Successfully added all permissions to the Administrator group (new database).'))
        else:
            self.stdout.write(self.style.SUCCESS('Database is not empty. Administrator permissions not modified.'))

        # Content Editor Permissions (Beispiel: Blog)
        # Hier musst du ggf. deine Models einfügen!
        # Das Beispiel ist angenommener weise blog.models.Post
        try:
            content_type_blog = ContentType.objects.get(app_label='blog', model='post')
            add_post = Permission.objects.get(codename='add_post', content_type=content_type_blog)
            change_post = Permission.objects.get(codename='change_post', content_type=content_type_blog)
            delete_post = Permission.objects.get(codename='delete_post', content_type=content_type_blog)
            view_post = Permission.objects.get(codename='view_post', content_type=content_type_blog)

            content_editor_group.permissions.add(add_post, change_post, delete_post, view_post)
            self.stdout.write(self.style.SUCCESS('Successfully added Content Editor permissions for Blog.'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error adding Blog permissions. Ensure your models are correct! Details: {e}'))
        self.stdout.write(self.style.SUCCESS('Successfully created or updated groups and permissions.'))
