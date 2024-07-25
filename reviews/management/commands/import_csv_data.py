from django.core.management.base import BaseCommand
import pandas as pd
from reviews.models import Author, Work, FirstPublication, BaseTextInfo

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
        BaseTextInfo.objects.all().delete()

        df = pd.read_csv('reviews/management/commands/list_person_all_extended_utf8.csv')

        # NaNをNoneに変換
        df = df.applymap(lambda x: None if pd.isna(x) else x)

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
                author.full_name = f'{author.last_name}{author.first_name or ""}'
                author.full_name_reading = f'{author.last_name_reading}{author.first_name_reading or ""}'
                author.save()

            # 底本情報の設定
            base_text_info = None
            if row['底本名1']:
                base_text_info, _ = BaseTextInfo.objects.get_or_create(
                    base_text_name=row['底本名1'],
                    defaults={
                        'base_text_publisher': row['底本出版社名1'],
                        'base_text_publish_year': row['底本初版発行年1'],
                        'parent_text_name': row['底本の親本名1'],
                        'parent_text_publisher': row['底本の親本出版社名1'],
                        'parent_text_publish_year': row['底本の親本初版発行年1']
                    }
                )

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
                'html_file_url': row['XHTML/HTMLファイルURL'],
                'base_text_info': base_text_info  # 底本情報を関連付け
            }

            # 既存のWorkを取得または作成
            work, created = Work.objects.get_or_create(
                title=row['作品名'],
                sub_title=row['副題'],
                original_title=row['原題'],
                book_card_url=row['図書カードURL'],
                defaults=work_defaults
            )

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

            # FirstPublicationの登録
            if row['初出']:
                first_publication, created = FirstPublication.objects.get_or_create(
                    work=work,
                    defaults={
                        'publication_info': row['初出']
                    }
                )

        self.stdout.write(self.style.SUCCESS('Data import completed successfully.'))