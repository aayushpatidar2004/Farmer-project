import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = 'Create or promote a Render admin using temporary environment variables.'

    def handle(self, *args, **options):
        username = os.environ.get('RENDER_ADMIN_USERNAME', '').strip()
        email = os.environ.get('RENDER_ADMIN_EMAIL', '').strip()
        password = os.environ.get('RENDER_ADMIN_PASSWORD', '')

        if not username and not email and not password:
            self.stdout.write('Render admin bootstrap is not configured; skipping.')
            return
        if not username or not email or not password:
            raise CommandError(
                'Set RENDER_ADMIN_USERNAME, RENDER_ADMIN_EMAIL, and '
                'RENDER_ADMIN_PASSWORD together in the service environment.'
            )

        User = get_user_model()
        user, created = User.objects.get_or_create(
            username=username,
            defaults={'email': email},
        )

        # Set the bootstrap password only when creating/promoting the account.
        # Removing the environment variables after deployment keeps it from
        # being reset on future service restarts.
        if created or not user.is_superuser:
            user.set_password(password)
        user.email = email
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save()

        self.stdout.write(self.style.SUCCESS(f'Render admin is ready: {username}'))
