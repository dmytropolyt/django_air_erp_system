# Generated by Django 4.1.3 on 2022-12-09 21:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('airsite', '0009_ticket_is_registered'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ticket',
            options={'permissions': [('change_ticket_is_registered', 'Can change is_registered field in ticket')]},
        ),
    ]
