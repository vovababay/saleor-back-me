# Generated by Django 3.1.2 on 2021-07-26 10:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0089_auto_20200902_1249'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='language_code',
            field=models.CharField(default='ru', max_length=35),
        ),
    ]
