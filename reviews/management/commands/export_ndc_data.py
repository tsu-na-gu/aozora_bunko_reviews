from django.core.management.base import BaseCommand
from reviews.models import NDC_Classification
import pandas as pd


class Command(BaseCommand):
    help = 'Export NDC classifications to a CSV file'

    def handle(self, *args, **kwargs):
        # データベースからデータを取得
        ndc_data = NDC_Classification.objects.all().values('ndc_code', 'genre')

        # データをDataFrameに変換
        df = pd.DataFrame(list(ndc_data))

        # CSVファイルにエクスポート
        csv_file = 'reviews/management/commands/ndc_classifications.csv'
        df.to_csv(csv_file, index=False, encoding='utf-8')

        self.stdout.write(self.style.SUCCESS(f'Successfully exported NDC classifications to {csv_file}'))