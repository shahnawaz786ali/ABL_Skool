# Generated by Django 3.2.20 on 2023-11-01 15:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_alter_user_profile_school_logo'),
    ]

    operations = [
        migrations.CreateModel(
            name='DemoBooking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('parent_name', models.CharField(max_length=100)),
                ('parent_mobile', models.CharField(max_length=15)),
                ('parent_email', models.EmailField(max_length=254)),
                ('student_name', models.CharField(max_length=100)),
                ('course', models.CharField(max_length=100)),
                ('slot_date', models.DateField()),
                ('slot_time', models.TimeField()),
            ],
        ),
    ]
