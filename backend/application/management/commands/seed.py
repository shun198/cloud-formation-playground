from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Seeds the database with initial data"

    def handle(self, *args, **options):
        print("add data")
