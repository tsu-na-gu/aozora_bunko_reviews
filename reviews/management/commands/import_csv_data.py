from django.core.management.base import BaseCommand
import pandas as pd
from reviews.models import Author, Work, WorkEditInfo
import logging

class Command(BaseCommand):
    help = 'Imports works from a CSV file'

    def handle(self, *args, **kwargs):
        df = pd.read_csv('reviews/management/commands/list_person_all_extended_utf8.csv')

        # 全ての文字列列の前後および中間の空白を削除
        def remove_spaces(date_str):
            if pd.isna(date_str):
                return date_str
            return date_str.replace(' ', '')

        df = df.apply(lambda col: col.map(lambda x: remove_spaces(x) if isinstance(x, str) else x))

        # '作品著作権フラグ' 列の 'なし' と 'あり' を True と False に変換
        df['作品著作権フラグ'] = df['作品著作権フラグ'].map({'あり': True, 'なし': False})

        # 'テキストファイルURL' と 'XHTML/HTMLファイルURL' が存在する行のみをフィルタリング
        df = df.dropna(subset=['テキストファイルURL', 'XHTML/HTMLファイルURL'])

        # 生年月日と没年月日列を削除
        df = df.drop(columns=['生年月日', '没年月日'])

        # ロギングの設定
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

        for index, row in df.iterrows():
            try:
                # 著者の作成または取得
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

                # 翻訳者の作成または取得
                translator = None
                if '翻訳者ID' in row and pd.notna(row['翻訳者ID']):
                    translator, created = Author.objects.get_or_create(
                        person_id=row['翻訳者ID'],
                        defaults={
                            'last_name': row['翻訳者姓'],
                            'first_name': row['翻訳者名'],
                            'last_name_reading': row['翻訳者姓読み'],
                            'first_name_reading': row['翻訳者名読み'],
                            'last_name_sorting': row['翻訳者姓読みソート用'],
                            'first_name_sorting': row['翻訳者名読みソート用'],
                        }
                    )

                # 作品の作成または取得
                work, created = Work.objects.get_or_create(
                    title=row['作品名'],
                    sub_title=row['副題'],
                    defaults={
                        'title_reading': row['作品名読み'],
                        'title_sorting': row['ソート用読み'],
                        'sub_title_reading': row['副題読み'],
                        'original_title': row['原題'],
                        'classification_number': row['分類番号'],
                        'character_usage': row['文字遣い種別'],
                        'copyright_flag': row['作品著作権フラグ'],
                        'release_date': row['公開日'],
                        'last_updated': row['最終更新日'],
                        'book_card_url': row['図書カードURL'],
                        'author': author,
                        'translator': translator,
                        'text_file_url': row['テキストファイルURL'],
                        'html_file_url': row['XHTML/HTMLファイルURL'],
                    }
                )

                # 作品編集情報の作成または取得
                WorkEditInfo.objects.get_or_create(
                    work=work,
                    defaults={
                        'inputter': row.get('入力者名'),
                        'proofer': row.get('校正者名'),
                        'base_text_name1': row['底本名1'],
                        'base_text_publisher1': row['底本出版社名1'],
                        'base_text_first_published_year1': row['底本初版発行年1'],
                        'base_text_name2': row['底本名2'],
                        'base_text_publisher2': row['底本出版社名2'],
                        'base_text_first_published_year2': row['底本初版発行年2'],
                        'original_base_text_name1': row.get('底本の親本名1'),
                        'original_base_text_publisher1': row['底本の親本出版社名1'],
                        'original_base_text_first_published_year1': row.get('底本の親本初版発行年1'),
                        'original_base_text_name2': row['底本の親本名2'],
                        'original_base_text_publisher2': row['底本の親本出版社名2'],
                        'original_base_text_first_published_year2': row['底本の親本初版発行年2'],
                        'creation_date': row.get('ファイル作成日'),
                        'modified_date': row.get('ファイル修正日'),
                        'notes': row.get('由来に関する注'),
                    }
                )
            except Exception as e:
                logging.error(f"Error processing row {index}: {e}")
                logging.error(f"Row data: {row.to_dict()}")