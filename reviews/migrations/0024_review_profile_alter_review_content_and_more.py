# Generated by Django 5.0.7 on 2024-07-27 05:49

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
        ('reviews', '0023_review_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='profile',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='account.profile'),
        ),
        migrations.AlterField(
            model_name='review',
            name='content',
            field=models.TextField(default=''),
        ),
        migrations.AlterField(
            model_name='review',
            name='title',
            field=models.CharField(default='', max_length=255),
        ),
    ]