# Generated by Django 5.0 on 2023-12-18 12:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('curriculum', '0003_lesson_assessment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lesson',
            name='video',
            field=models.URLField(default='', max_length=300, verbose_name='Videos'),
        ),
    ]
