# Generated by Django 3.1.2 on 2021-07-29 10:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('discount', '0021_auto_20200902_1249'),
    ]

    operations = [
        migrations.AddField(
            model_name='sale',
            name='every_day',
            field=models.BooleanField(default=False, verbose_name='Каждый день изменять стоимость'),
        ),
    ]
