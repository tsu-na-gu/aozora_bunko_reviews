from django.db import models


class Author(models.Model):
    person_id = models.IntegerField(primary_key=True)
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100)
    first_name_reading = models.CharField(max_length=100, null=True, blank=True)
    last_name_reading = models.CharField(max_length=100)
    first_name_sorting = models.CharField(max_length=100, null=True, blank=True)
    last_name_sorting = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Work(models.Model):
    title = models.CharField(max_length=256)
    title_reading = models.CharField(max_length=256)
    title_sorting = models.CharField(max_length=256, null=True, blank=True)
    sub_title = models.CharField(max_length=256, null=True, blank=True)
    sub_title_reading = models.CharField(max_length=256, null=True, blank=True)
    original_title = models.CharField(max_length=256, null=True, blank=True)
    classification_number = models.CharField(max_length=50, null=True, blank=True)
    character_usage = models.CharField(max_length=50)
    copyright_flag = models.BooleanField(default=False)
    release_date = models.DateField(null=True, blank=True)
    last_updated = models.DateField(null=True, blank=True)
    book_card_url = models.URLField(max_length=200)
    role_flag = models.CharField(max_length=50, default='著者')  # 役割フラグを追加
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='works')
    translator = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True, blank=True, related_name='translated_works')
    text_file_url = models.URLField(max_length=200, null=True, blank=True)
    html_file_url = models.URLField(max_length=200, null=True, blank=True)

    class Meta:
        unique_together = (('title', 'sub_title'),)

    def __str__(self):
        return self.title




