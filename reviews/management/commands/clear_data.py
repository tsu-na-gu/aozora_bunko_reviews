from django.core.management.base import BaseCommand
from reviews.models import Work, Author, FirstPublication

class Command(BaseCommand):
    help = 'Clears all data from the Work, Author, and FirstPublication tables'

    def handle(self, *args, **kwargs):
        FirstPublication.objects.all().delete()
        Work.objects.all().delete()
        Author.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('Successfully cleared the data from Work, Author, and FirstPublication tables.'))