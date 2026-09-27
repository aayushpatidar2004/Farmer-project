from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    help = 'Create an admin user with the Admin role and Django admin access.'

    def add_arguments(self, parser):
        parser.add_argument('username', type=str)
        parser.add_argument('email', type=str)
        parser.add_argument('password', type=str)

    def handle(self, *args, **options):
        User = get_user_model()
        username = options['username']
        email = options['email']
        password = options['password']

        if User.objects.filter(username=username).exists():
            self.stdout.write(self.style.ERROR(f'User with username "{username}" already exists.'))
            return

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name='Admin',
            last_name='User',
            is_staff=True,
            is_superuser=True,
        )

        profile = user.farmer_profile
        profile.role = 'admin'
        profile.save()

        self.stdout.write(
            self.style.SUCCESS(
                f'Admin user created successfully: {user.username} ({user.email})'
            )
        )
