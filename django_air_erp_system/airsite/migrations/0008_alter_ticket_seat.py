# Generated by Django 4.1.3 on 2022-12-08 15:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('airsite', '0007_ticket_option_2_alter_option_name_alter_seat_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='seat',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='ticket', to='airsite.seat'),
        ),
    ]
