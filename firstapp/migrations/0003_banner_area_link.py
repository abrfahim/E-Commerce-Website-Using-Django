# Generated by Django 5.0 on 2024-01-02 12:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('firstapp', '0002_banner_area'),
    ]

    operations = [
        migrations.AddField(
            model_name='banner_area',
            name='Link',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
