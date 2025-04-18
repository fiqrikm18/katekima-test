# Generated by Django 5.1.3 on 2025-03-21 07:20

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transaction', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='transaction_type',
            field=models.CharField(choices=[('sell', 'Sell'), ('purchase', 'Purchase')], default='purchase'),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='code',
            field=models.CharField(max_length=10, unique=True),
        ),
        migrations.AlterField(
            model_name='transactiondetail',
            name='header_code',
            field=models.ForeignKey(db_column='header_code', on_delete=django.db.models.deletion.CASCADE, to='transaction.transaction', to_field='code'),
        ),
    ]
