# Generated by Django 4.1.3 on 2022-12-14 23:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('airsite', '0012_checkin'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='seat',
            name='price',
        ),
    ]