# Generated by Django 4.1 on 2024-07-21 05:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0008_remove_author_birth_date_remove_author_death_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='work',
            name='first_published',
            field=models.CharField(blank=True, max_length=3000, null=True),
        ),
    ]
