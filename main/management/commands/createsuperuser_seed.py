import os

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


ADMIN_USERNAME = os.getenv('ADMIN_USERNAME')
ADMIN_EMAIL = os.getenv('ADMIN_EMAIL')
ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD')

class Command(BaseCommand):
    help = 'Create a superuser if not exists'

    def handle(self, *args, **kwargs):
        if not ADMIN_USERNAME or not ADMIN_EMAIL or not ADMIN_PASSWORD:
            return self.stdout.write(self.style.ERROR('Environment variables for admin not set'))

        if not User.objects.filter(username=ADMIN_USERNAME).exists():
            User.objects.create_superuser(username=ADMIN_USERNAME, email=ADMIN_EMAIL, password=ADMIN_PASSWORD)
            self.stdout.write(self.style.SUCCESS('Superuser created successfully'))
        else:
            self.stdout.write(self.style.WARNING('Superuser already exists'))
