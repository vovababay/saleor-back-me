# Generated by Django 3.1.2 on 2021-07-29 13:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('discount', '0023_auto_20210729_1327'),
    ]

    operations = [
        migrations.AddField(
            model_name='sale',
            name='periodically_change',
            field=models.BooleanField(default=False, verbose_name='Переодически изменять стоимость'),
        ),
    ]
