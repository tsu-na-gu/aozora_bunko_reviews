# Generated by Django 5.0.7 on 2024-07-24 21:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0015_ndc_classification_parent'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ndc_classification',
            name='parent',
        ),
    ]
