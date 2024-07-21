import pandas as pd
import django
import os
from datetime import datetime

from django.core.management import BaseCommand

from reviews.models import Author


class Command(BaseCommand):
    help = 'Import authors from CSV file'

    def handle(self, *args, **options):
        df = pd.read_csv('reviews/management/commands/list_person_all_extended_utf8.csv')
        df2 = df[['人物ID', '姓', '名', '姓読み', '名読み', '姓読みソート用', '名読みソート用', '生年月日', '没年月日']]
        df2_unique = df2.drop_duplicates()

        def parse_date(date_str):
            try:
                return datetime.strptime(date_str, '%Y-%m-%d').date() if pd.notnull(date_str) else None
            except ValueError:
                return None

        # データのインポート
        for index, row in df2_unique.iterrows():
            birth_date = parse_date(row['生年月日'])
            death_date = parse_date(row['没年月日'])

            author, created = Author.objects.get_or_create(
                person_id=row['人物ID'],
                defaults={
                    'last_name':row['姓'],
                    'first_name':row['名'],
                    'last_name_reading':row['姓読み'],
                    'first_name_reading':row['名読み'],
                    'last_name_sorting':row['姓読みソート用'],
                    'first_name_sorting':row['名読みソート用'],
                    'birth_date':birth_date,
                    'death_date':death_date,
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"新しい作家が作成されました: {author}"))
            else:
                self.stdout.write(self.style.SUCCESS(f"既存の作家が取得されました: {author}"))
