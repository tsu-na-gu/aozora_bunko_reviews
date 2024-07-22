from django.test import TestCase
from django.core.management import call_command
from reviews.models import Work, Author
class DataImportTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # フィクスチャをロード
        call_command('loaddata', 'reviews/fixtures/new_fixture.json')

    def test_author_data_import(self):
        # データベースに指定の人物IDが存在することを確認します
        person_id = 1562  # テストする人物IDを指定
        author = Author.objects.get(person_id=person_id)
        self.assertIsNotNone(author)

        # 著者の各フィールドが正確にインポートされていることを確認します
        self.assertEqual(author.last_name, '吉川')
        self.assertEqual(author.first_name, '英治')
        self.assertEqual(author.last_name_reading, 'よしかわ')
        self.assertEqual(author.first_name_reading, 'えいじ')
        self.assertEqual(author.last_name_sorting, 'よしかわ')
        self.assertEqual(author.first_name_sorting, 'えいし')

    def test_work_data_import(self):
        # データベースに指定の作品名が存在することを確認します
        title = '新書太閤記'  # テストする作品名を指定
        sub_title = '07 第七分冊'  # テストする副題を指定
        work = Work.objects.get(title=title, sub_title=sub_title)
        self.assertIsNotNone(work)

        # 作品の各フィールドが正確にインポートされていることを確認します
        self.assertEqual(work.sub_title, '07 第七分冊')
        self.assertEqual(work.title_reading, 'しんしょたいこうき')
        self.assertEqual(work.title_sorting, 'しんしよたいこうき')
        self.assertEqual(work.sub_title_reading, '07 だいななぶんさつ')
        self.assertEqual(work.original_title, None)
        self.assertEqual(work.classification_number, 'NDC 913')
        self.assertEqual(work.character_usage, '新字新仮名')
        self.assertEqual(work.copyright_flag, False)  # 著作権フラグが「なし」の場合
        self.assertEqual(work.release_date.strftime('%Y-%m-%d'), '2016-01-03')
        self.assertEqual(work.last_updated.strftime('%Y-%m-%d'), '2016-01-03')
        self.assertEqual(work.book_card_url, 'https://www.aozora.gr.jp/cards/001562/card56758.html')
        self.assertEqual(work.text_file_url, 'https://www.aozora.gr.jp/cards/001562/files/56758_ruby_57843.zip')
        self.assertEqual(work.html_file_url, 'https://www.aozora.gr.jp/cards/001562/files/56758_57892.html')

        # ForeignKeyのリレーションシップが正しいことを確認します
        self.assertEqual(work.author.person_id, 1562)
        self.assertEqual(work.author.last_name, '吉川')
        self.assertEqual(work.author.first_name, '英治')

    def test_work_data_import2(self):
        work = Work.objects.get(title='老年と人生', sub_title=None)
        self.assertEqual(work.title, '老年と人生')
        self.assertEqual(work.sub_title, None)
        self.assertEqual(work.title_reading, 'ろうねんとじんせい')
        self.assertEqual(work.title_sorting, 'ろうねんとしんせい')
        self.assertEqual(work.original_title, None)
        self.assertEqual(work.classification_number, 'NDC 914')
        self.assertEqual(work.character_usage, '新字新仮名')
        self.assertFalse(work.copyright_flag)
        self.assertEqual(work.release_date.strftime('%Y-%m-%d'), '2001-10-11')
        self.assertEqual(work.last_updated.strftime('%Y-%m-%d'), '2016-01-17')
        self.assertEqual(work.author.last_name, '萩原')
        self.assertEqual(work.author.first_name, '朔太郎')


    def test_author_data_import2(self):
        author = Author.objects.get(person_id=67)
        self.assertEqual(author.last_name, '萩原')
        self.assertEqual(author.first_name, '朔太郎')
        self.assertEqual(author.last_name_reading, 'はぎわら')
        self.assertEqual(author.first_name_reading, 'さくたろう')
        self.assertEqual(author.last_name_sorting, 'はきわら')
        self.assertEqual(author.first_name_sorting, 'さくたろう')
        self.assertEqual(author.birth_date.strftime('%Y-%m-%d'), '1886-11-01')
        self.assertEqual(author.death_date.strftime('%Y-%m-%d'), '1942-05-11')

