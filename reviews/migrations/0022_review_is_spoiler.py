# Generated by Django 5.0.7 on 2024-07-26 07:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0021_review'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='is_spoiler',
            field=models.BooleanField(default=False),
        ),
    ]
