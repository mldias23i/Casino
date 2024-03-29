# Generated by Django 4.2.1 on 2023-10-17 14:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('casino', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Refund',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.CharField(max_length=255)),
                ('clientId', models.CharField(max_length=255)),
                ('roundId', models.UUIDField(unique=True)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('transactionId', models.UUIDField(unique=True)),
                ('refundTransactionId', models.UUIDField(unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Win',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.CharField(max_length=255)),
                ('clientId', models.CharField(max_length=255)),
                ('roundId', models.UUIDField(unique=True)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('transactionId', models.UUIDField(unique=True)),
            ],
        ),
    ]
