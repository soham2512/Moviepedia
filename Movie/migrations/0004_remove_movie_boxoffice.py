# Generated by Django 3.2 on 2022-04-03 20:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Movie', '0003_auto_20220403_1559'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='movie',
            name='BoxOffice',
        ),
    ]