from django.core.management.base import BaseCommand
import pandas as pd
from reviews.models import Author, Work, FirstPublication

def convert_nan_to_none(value):
    if pd.isna(value):
        return None
    return value

class Command(BaseCommand):
    help = 'Imports works from a CSV file'

    def handle(self, *args, **kwargs):
        # データベースのクリア
        FirstPublication.objects.all().delete()
        Work.objects.all().delete()
        Author.objects.all().delete()

        df = pd.read_csv('reviews/management/commands/list_person_all_extended_utf8.csv')

        # NaNをNoneに変換
        df = df.apply(lambda x: x.map(convert_nan_to_none) if x.dtype == "O" else x)

        for index, row in df.iterrows():
            if not row['テキストファイルURL'] and not row['XHTML/HTMLファイルURL']:
                continue  # テキストファイルURLとXHTML/HTMLファイルURLが両方ともない場合はスキップ

            # Authorのデフォルト値を設定
            author = None
            if row['姓'] and row['人物ID']:
                author, created = Author.objects.get_or_create(
                    person_id=row['人物ID'],
                    defaults={
                        'last_name': row['姓'],
                        'first_name': row['名'],
                        'last_name_reading': row['姓読み'],
                        'first_name_reading': row['名読み'],
                        'last_name_sorting': row['姓読みソート用'],
                        'first_name_sorting': row['名読みソート用'],
                    }
                )

                # 必要に応じてfull_nameとfull_name_readingを更新
                author.full_name = f'{author.last_name}{author.first_name or ""}'
                author.full_name_reading = f'{author.last_name_reading}{author.first_name_reading or ""}'
                author.save()

            # Workオブジェクトのデフォルト値
            work_defaults = {
                'title_reading': row['作品名読み'],
                'title_sorting': row['ソート用読み'],
                'sub_title_reading': row['副題読み'],
                'original_title': row['原題'],
                'classification_number': row['分類番号'],
                'character_usage': row['文字遣い種別'],
                'copyright_flag': row['作品著作権フラグ'] == 'あり',
                'release_date': row['公開日'],
                'last_updated': row['最終更新日'],
                'book_card_url': row['図書カードURL'],
                'text_file_url': row['テキストファイルURL'],
                'html_file_url': row['XHTML/HTMLファイルURL']
            }

            work, created = Work.objects.get_or_create(
                title=row['作品名'],
                sub_title=row['副題'],
                defaults=work_defaults
            )

            # 既存のWorkを更新する場合
            if not created:
                for key, value in work_defaults.items():
                    setattr(work, key, value)

            # 役割フラグに基づいてリレーションシップを設定
            if row['役割フラグ'] == '著者' and author:
                work.authors.add(author)
            elif row['役割フラグ'] == '翻訳者' and author:
                work.translator = author
            elif row['役割フラグ'] == '編集' and author:
                work.editor = author
            elif author:
                work.other_role = author

            work.save()

            self.stdout.write(self.style.SUCCESS(f'Successfully imported work {work.id}'))

        self.stdout.write(self.style.SUCCESS('Data import completed successfully.'))