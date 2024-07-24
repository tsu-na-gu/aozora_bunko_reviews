from django.core.management.base import BaseCommand
from reviews.models import NDC_Classification

class Command(BaseCommand):
    help = 'Check and create the children literature genre in NDC_Classification'

    def handle(self, *args, **kwargs):
        # 児童文学がNDC分類にあるか確認し、なければ作成
        children_literature, created = NDC_Classification.objects.get_or_create(
            genre='児童文学',
            defaults={'ndc_code': 'K'}
        )
        if created:
            self.stdout.write(self.style.SUCCESS('児童文学のジャンルを作成しました。'))
        else:
            self.stdout.write(self.style.SUCCESS('児童文学のジャンルは既に存在します。'))