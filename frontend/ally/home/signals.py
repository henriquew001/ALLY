# /home/heinrich/projects/ConsciousFit/frontend/ally/home/signals.py

from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.contrib.auth.models import Group
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

@receiver(post_migrate)
def create_default_groups(sender, **kwargs):
    """
    Creates the default groups (Administrator, Content Editor, User, Guest)
    if they don't exist. Logs the creation of each group.
    """
    if sender.name == 'home':  # Check if the signal is sent by the home app # oder core
        groups = ['Administrator', 'Content Editor', 'User', 'Guest']
        for group_name in groups:
            group, created = Group.objects.get_or_create(name=group_name)
            if created:
                logger.info(f"Created group: {group_name}")
                print(f"Created group: {group_name}") # for console output
            else:
                logger.debug(f"Group {group_name} already exists.")
