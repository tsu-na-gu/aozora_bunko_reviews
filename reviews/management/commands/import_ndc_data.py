import rdflib
from rdflib.namespace import RDFS, SKOS
from django.core.management.base import BaseCommand
from reviews.models import NDC_Classification
import pandas as pd


class Command(BaseCommand):
    help = 'Import NDC classifications from a TTL file'

    def handle(self, *args, **kwargs):
        # まずテーブルを空にする
        NDC_Classification.objects.all().delete()

        ttl_file = 'reviews/management/commands/ndc9.ttl'
        g = rdflib.Graph()

        # ファイルを読み込む（エンコーディングを指定）
        with open(ttl_file, 'r', encoding='utf-8') as f:
            g.parse(file=f, format='ttl')

        # データを抽出
        data = []
        label_dict = {}
        for s, p, o in g:
            if p == SKOS.notation:
                ndc_code = str(o)
                # NDCコードがちょうど3桁かチェック
                if len(ndc_code) == 3 and '.' not in ndc_code:
                    data.append((ndc_code, None))  # ラベルを一時的にNoneに設定
            elif p == RDFS.label:
                label = str(o).replace('--', '-').replace('.', '・').strip()
                label_dict[str(s)] = label

        # デバッグ: 抽出されたラベルの確認
        print("ラベルの辞書:")
        for key, value in label_dict.items():
            print(f"{key}: {value}")

        # データとラベルをマッピング
        for i in range(len(data)):
            ndc_code = data[i][0]
            for key, value in label_dict.items():
                if key.endswith(ndc_code):
                    # 500文字に収まるように処理
                    truncated_label = value[:500]
                    data[i] = (ndc_code, truncated_label)

        # データフレームに変換
        df = pd.DataFrame(data, columns=['NDCコード', 'ジャンル'])

        # 空のラベルを持つ行を表示
        nan_rows = df[df['ジャンル'].isna()]
        print("NaNを含む行:")
        print(nan_rows)

        # エラーが発生するジャンルの一覧を表示
        error_genres = df[df['ジャンル'].apply(lambda x: len(x) > 500)]
        print("500文字を超えるジャンル:")
        print(error_genres)

        # データの概要を表示
        print(df.info())

        # データの最初の数行を表示
        print(df.head())

        # 空のラベルを持つ行がないかチェック
        if nan_rows.empty:
            print("全てのラベルが正常に読み込まれました。")
        else:
            print("空のラベルを持つ行があります。")

        # データをデータベースに保存
        for index, row in df.iterrows():
            ndc_code = row['NDCコード']
            genre = row['ジャンル']
            if genre is not None:
                NDC_Classification.objects.get_or_create(ndc_code=ndc_code, defaults={'genre': genre})

        self.stdout.write(self.style.SUCCESS('Successfully imported NDC classifications'))