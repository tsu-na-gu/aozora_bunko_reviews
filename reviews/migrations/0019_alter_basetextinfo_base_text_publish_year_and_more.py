# Generated by Django 5.0.7 on 2024-07-24 22:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0018_basetextinfo_alter_work_unique_together_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='basetextinfo',
            name='base_text_publish_year',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='basetextinfo',
            name='parent_text_publish_year',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]