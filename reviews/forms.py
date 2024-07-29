from django import forms

from reviews.models import Review


class DetailSearchForm(forms.Form):
    title = forms.CharField(required=False, label='書籍名')
    title_reading = forms.CharField(required=False, label='書籍名（読み）')
    author_last_name = forms.CharField(required=False, label='著者の姓')
    author_first_name = forms.CharField(required=False, label='著者の名')
    author_last_name_reading = forms.CharField(required=False, label='著者の姓（読み）')
    author_first_name_reading = forms.CharField(required=False, label='著者の名（読み）')
    translator_last_name = forms.CharField(required=False, label='翻訳者の姓')
    translator_first_name = forms.CharField(required=False, label='翻訳者の名')
    translator_last_name_reading = forms.CharField(required=False, label='翻訳者の姓（読み）')
    translator_first_name_reading = forms.CharField(required=False, label='翻訳者の名（読み）')
    character_usage = forms.ChoiceField(required=False, choices=[
        ('新字旧仮名', '新字旧仮名'),
        ('旧字旧仮名', '旧字旧仮名'),
        ('新字新仮名', '新字新仮名'),
    ], label='仮名遣い')
    is_children_book = forms.BooleanField(required=False, label='児童書')



class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['title', 'rating', 'content', 'is_spoiler']
        labels = {
            'title': 'タイトル',
            'rating': '1〜５で評価',
            'content': 'レビュー内容',
            'is_spoiler': 'ネタバレを含む'
        }
        widgets = {
            'rating': forms.Select(choices=[(i, i) for i in range(1, 6)]),
        }