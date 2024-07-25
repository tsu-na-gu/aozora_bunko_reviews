from django.core.management.base import BaseCommand
from reviews.models import Work, NDC_Classification


class Command(BaseCommand):
    help = 'Update genre_info1 and genre_info2 fields in Work model based on NDC classification number'

    def handle(self, *args, **kwargs):
        # 児童文学がNDC分類にあるか確認
        try:
            children_literature = NDC_Classification.objects.get(genre='児童書')
        except NDC_Classification.DoesNotExist:
            self.stdout.write(self.style.ERROR(
                '児童書のジャンルが見つかりません。まず create_children_literature コマンドを実行してください。'))
            return

        # すべてのWorkオブジェクトのgenre_info1とgenre_info2を空にする
        works = Work.objects.all()
        for work in works:
            work.genre_info1 = None
            work.genre_info2 = None
            work.save()

        # 処理の開始
        for work in works:
            classification_numbers = work.classification_number.split() if work.classification_number else []
            genre_info1 = None
            genre_info2 = None

            for i, number in enumerate(classification_numbers):
                if i == 0:  # 最初のNDC文字列はスキップ
                    continue
                if number.startswith('K'):
                    genre_info1 = children_literature
                    ndc_code = number[1:4]  # Kの後の3桁を取得
                else:
                    ndc_code = number[:3]  # 最初の3桁を取得

                try:
                    genre_info = NDC_Classification.objects.get(ndc_code=ndc_code)
                    if genre_info1 is None:
                        genre_info1 = genre_info
                    else:
                        genre_info2 = genre_info
                except NDC_Classification.DoesNotExist:
                    self.stdout.write(self.style.WARNING(f'No NDC_Classification found for code {ndc_code}'))

            work.genre_info1 = genre_info1
            work.genre_info2 = genre_info2
            work.save()

            self.stdout.write(self.style.SUCCESS(f'Successfully updated {work.title} with genres'))

        self.stdout.write(self.style.SUCCESS('Successfully updated genre_info1 and genre_info2 for all works'))