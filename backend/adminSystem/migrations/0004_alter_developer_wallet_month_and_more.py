# Generated by Django 5.1.2 on 2025-01-13 00:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminSystem', '0003_alter_developer_wallet_month'),
    ]

    operations = [
        migrations.AlterField(
            model_name='developer_wallet',
            name='month',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='developer_wallet',
            name='year',
            field=models.IntegerField(default=2025),
        ),
    ]
