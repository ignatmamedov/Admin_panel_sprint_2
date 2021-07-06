from django.core.management.base import BaseCommand
from movies.factories import generate_content


class Command(BaseCommand):
    def handle(self, *args, **options):
        generate_content()
