# Generated by Django 3.2.17 on 2023-06-22 12:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20230621_1603'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notificationstudent',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
