# Generated by Django 4.2.1 on 2023-10-17 15:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('casino', '0002_refund_win'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bet',
            name='token',
        ),
        migrations.RemoveField(
            model_name='refund',
            name='token',
        ),
        migrations.RemoveField(
            model_name='win',
            name='token',
        ),
    ]
