# management/commands/generate_wikipedia_links.py

from django.core.management.base import BaseCommand
from reviews.models import Author
import requests

class Command(BaseCommand):
    help = 'Generate Wikipedia links for authors and check their validity'

    def handle(self, *args, **kwargs):
        authors = Author.objects.all()
        for author in authors:
            full_name = author.full_name
            url = f"https://ja.wikipedia.org/wiki/{full_name}"

            try:
                response = requests.head(url, timeout=5)
                if response.status_code == 200:
                    author.wikipedia_link = url
                    author.save()
                    self.stdout.write(self.style.SUCCESS(f'Successfully set Wikipedia link for {full_name}'))
                else:
                    self.stdout.write(self.style.WARNING(f'No valid Wikipedia page found for {full_name}'))
            except requests.RequestException as e:
                self.stdout.write(self.style.ERROR(f'Error checking Wikipedia link for {full_name}: {e}'))

        self.stdout.write(self.style.SUCCESS('Wikipedia link generation completed successfully'))