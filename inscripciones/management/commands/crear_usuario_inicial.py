from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'Crea el superusuario inicial si no existe'

    def handle(self, *args, **options):
        username = 'Ariel'
        password = 'Ariel37787045'

        if User.objects.filter(username=username).exists():
            self.stdout.write(self.style.WARNING(f'El usuario "{username}" ya existe.'))
        else:
            User.objects.create_superuser(
                username=username,
                password=password,
                email='ariel@hut.org',
            )
            self.stdout.write(self.style.SUCCESS(f'✅ Superusuario "{username}" creado correctamente.'))
