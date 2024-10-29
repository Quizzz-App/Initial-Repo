# Generated by Django 5.0.6 on 2024-09-13 23:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminSystem', '0006_transactionhistory'),
    ]

    operations = [
        migrations.AddField(
            model_name='developer_wallet',
            name='total_amount',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
        migrations.DeleteModel(
            name='TransactionHistory',
        ),
    ]
