# Generated by Django 5.0.7 on 2024-07-25 02:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0019_alter_basetextinfo_base_text_publish_year_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='author',
            name='wikipedia_link',
            field=models.URLField(blank=True, null=True),
        ),
    ]
