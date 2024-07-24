from django.core.management.base import BaseCommand
from reviews.models import NDC_Classification

class Command(BaseCommand):
    help = 'Check NDC Classification data'

    def handle(self, *args, **kwargs):
        ndc_data = NDC_Classification.objects.exclude(parent__isnull=True)

        if not ndc_data.exists():
            self.stdout.write(self.style.WARNING('No data found with parent code'))
        else:
            for ndc in ndc_data:
                self.stdout.write(f'NDC Code: {ndc.ndc_code}, Genre: {ndc.genre}, Parent: {ndc.parent.ndc_code if ndc.parent else "None"}')