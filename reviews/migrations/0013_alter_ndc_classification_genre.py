# Generated by Django 5.0.7 on 2024-07-24 02:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0012_remove_ndc_classification_parent_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ndc_classification',
            name='genre',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]