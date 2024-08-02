# management/commands/set_default_book_for_reviewhistory.py
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from user_account.models import ReviewHistory
from reviews.models import Review

class Command(BaseCommand):
    help = 'Set default book for existing review history records'

    def handle(self, *args, **kwargs):
        default_review = Review.objects.first()  # 適切なデフォルトの本を選択
        ReviewHistory.objects.filter(review__isnull=True).update(review=default_review)
        self.stdout.write(self.style.SUCCESS('Successfully set default book for existing review histories'))