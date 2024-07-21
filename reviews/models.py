from django.db import models


class Author(models.Model):
    person_id = models.IntegerField(primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    first_name_reading = models.CharField(max_length=100)
    last_name_reading = models.CharField(max_length=100)
    first_name_sorting = models.CharField(max_length=100)
    last_name_sorting = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Work(models.Model):
    title = models.CharField(max_length=256)
    title_reading = models.CharField(max_length=256)
    title_sorting = models.CharField(max_length=256)
    sub_title = models.CharField(max_length=256, null=True, blank=True)
    sub_title_reading = models.CharField(max_length=256, null=True, blank=True)
    original_title = models.CharField(max_length=256, null=True, blank=True)
    classification_number = models.CharField(max_length=50, null=True, blank=True)
    character_usage = models.CharField(max_length=50)
    copyright_flag = models.BooleanField(default=False)
    release_date = models.DateField(null=True, blank=True)
    last_updated = models.DateField(null=True, blank=True)
    book_card_url = models.URLField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='works')
    translator = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True, blank=True, related_name='translated_works')
    text_file_url = models.URLField(max_length=200, null=True, blank=True)
    html_file_url = models.URLField(max_length=200, null=True, blank=True)

    class Meta:
        unique_together = (('title', 'sub_title'),)

    def __str__(self):
        return self.title


class WorkEditInfo(models.Model):
    work = models.OneToOneField(Work, on_delete=models.CASCADE)
    inputter = models.CharField(max_length=255, null=True, blank=True)  # 入力者名
    proofer = models.CharField(max_length=255, null=True, blank=True)  # 校正者名
    base_text_name1 = models.CharField(max_length=255, null=True, blank=True)  # 底本名1
    base_text_publisher1 = models.CharField(max_length=255, null=True, blank=True)  # 底本出版社名1
    base_text_first_published_year1 = models.CharField(max_length=255, null=True, blank=True)  # 底本初版発行年1
    base_text_name2 = models.CharField(max_length=255, null=True, blank=True)  # 底本名2
    base_text_publisher2 = models.CharField(max_length=255, null=True, blank=True)  # 底本出版社名2
    base_text_first_published_year2 = models.CharField(max_length=255, null=True, blank=True)  # 底本初版発行年2
    original_base_text_name1 = models.CharField(max_length=255, null=True, blank=True)  # 底本の親本名1
    original_base_text_publisher1 = models.CharField(max_length=255, null=True, blank=True)  # 底本の親本出版社名1
    original_base_text_first_published_year1 = models.CharField(max_length=255, null=True, blank=True)  # 底本の親本初版発行年1
    original_base_text_name2 = models.CharField(max_length=255, null=True, blank=True)  # 底本の親本名2
    original_base_text_publisher2 = models.CharField(max_length=255, null=True, blank=True)  # 底本の親本出版社名2
    original_base_text_first_published_year2 = models.CharField(max_length=255, null=True, blank=True)  # 底本の親本初版発行年2
    creation_date = models.DateField(null=True, blank=True)  # ファイル作成日
    modified_date = models.DateField(null=True, blank=True)  # ファイル修正日
    notes = models.TextField(null=True, blank=True)  # 作成ファイルに関する由来の注釈

