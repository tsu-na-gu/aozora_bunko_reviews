import pandas as pd
from django.core.management.base import BaseCommand
from reviews.models import Work, FirstPublication  # モデルをインポート

def convert_nan_to_none(value):
    if pd.isna(value):
        return None
    return value

class Command(BaseCommand):
    help = 'Import first publication data from CSV'

    def handle(self, *args, **options):
        # CSVファイルのパスを指定
        csv_file_path = 'reviews/management/commands/list_person_all_extended_utf8.csv'

        # CSVデータを読み込み
        df = pd.read_csv(csv_file_path)

        # 副題の列にのみNaNをNoneに変換
        df['副題'] = df['副題'].apply(convert_nan_to_none)

        # データをインポート
        for index, row in df.iterrows():
            # テキストファイルURLとXHTML/HTMLファイルURLが両方ともない場合はスキップ
            if row['テキストファイルURL'] is None and row['XHTML/HTMLファイルURL'] is None:
                continue

            sub_title = row['副題']

            try:
                # 'title'と'sub_title'でWorkを検索
                work = Work.objects.get(title=row['作品名'], sub_title=sub_title)
                first_publication, created = FirstPublication.objects.get_or_create(
                    work=work,
                    defaults={'publication_info': row['初出']}
                )
                if not created:
                    first_publication.publication_info = row['初出']
                    first_publication.save()
                self.stdout.write(self.style.SUCCESS(f'Successfully imported publication info for work {work.id}'))
            except Work.DoesNotExist:
                self.stdout.write(self.style.WARNING(
                    f'Work with title "{row["作品名"]}" and sub_title "{sub_title}" does not exist. '
                    f'Author: "{row.get("著者", "不明")}", '
                    f'Text File URL: "{row["テキストファイルURL"]}", '
                    f'XHTML/HTML File URL: "{row["XHTML/HTMLファイルURL"]}"'
                ))