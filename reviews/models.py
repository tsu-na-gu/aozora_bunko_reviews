from django.db import models
from django.contrib import auth
from tailwind.validate import ValidationError




class Author(models.Model):
    person_id = models.IntegerField(primary_key=True)
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100)
    first_name_reading = models.CharField(max_length=100, null=True, blank=True)
    last_name_reading = models.CharField(max_length=100)
    first_name_sorting = models.CharField(max_length=100, null=True, blank=True)
    last_name_sorting = models.CharField(max_length=100)
    full_name = models.CharField(max_length=100, null=True, blank=True)
    full_name_reading = models.CharField(max_length=100, null=True, blank=True)
    wikipedia_link = models.URLField(max_length=200, null=True, blank=True)

    def save(self, *args, **kwargs):
        self.full_name = f'{self.last_name}{self.first_name or ""}'
        self.full_name_reading = f'{self.last_name_reading}{self.first_name_reading or ""}'
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.full_name}'

    
class NDC_Classification(models.Model):
    ndc_code = models.CharField(max_length=10, unique=True)
    genre = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self):
        return self.ndc_code


class BaseTextInfo(models.Model):
    base_text_name = models.CharField(max_length=500)
    base_text_publisher = models.CharField(max_length=256, null=True, blank=True)
    base_text_publish_year = models.CharField(max_length=100, null=True, blank=True)
    parent_text_name = models.CharField(max_length=500, null=True, blank=True)
    parent_text_publisher = models.CharField(max_length=256, null=True, blank=True)
    parent_text_publish_year = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.base_text_name

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
    authors = models.ManyToManyField(Author,related_name='works', blank=True)
    translator = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True, blank=True,
                                   related_name='translated_works')
    editor = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True, blank=True, related_name='edited_works')
    other_role = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True, blank=True,
                                   related_name='other_role_works')
    text_file_url = models.URLField(max_length=200, null=True, blank=True)
    html_file_url = models.URLField(max_length=200, null=True, blank=True)
    genre_info1 = models.ForeignKey(NDC_Classification, null=True, blank=True, on_delete=models.SET_NULL,
                                    related_name='primary_works')
    genre_info2 = models.ForeignKey(NDC_Classification, null=True, blank=True, on_delete=models.SET_NULL,
                                    related_name='secondary_works')
    base_text_info = models.ForeignKey(BaseTextInfo, null=True, blank=True, on_delete=models.SET_NULL, related_name='base_text_info')

    class Meta:
        unique_together = (('title', 'sub_title', 'original_title', 'book_card_url'),)
    def __str__(self):
        return self.title


class FirstPublication(models.Model):
    work = models.OneToOneField(Work, related_name='first_publication', on_delete=models.CASCADE)
    publication_info = models.TextField()

    def __str__(self):
        return self.publication_info[:15]


def validate_rating(value):
    if value < 1 or value > 5:
        raise ValidationError("It must be between 1 and 5.")


class Review(models.Model):
    title = models.CharField(max_length=255)
    rating = models.IntegerField(validators=[validate_rating])
    content = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    date_edited = models.DateTimeField(null=True, blank=True)
    is_spoiler = models.BooleanField(default=False)
    creator = models.ForeignKey(
        auth.get_user_model(),  on_delete=models.CASCADE, related_name="review_user"
    )
    book = models.ForeignKey(
        Work, on_delete=models.CASCADE, related_name="review_book"
    )



