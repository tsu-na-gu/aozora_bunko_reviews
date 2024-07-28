from django import forms

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