# Generated by Django 4.2.1 on 2023-10-17 15:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('casino', '0003_remove_bet_token_remove_refund_token_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='bet',
            name='clientId',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='bet',
            name='currency',
            field=models.CharField(max_length=10),
        ),
    ]
