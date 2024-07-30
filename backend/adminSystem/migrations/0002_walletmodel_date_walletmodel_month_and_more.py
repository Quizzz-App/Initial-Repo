# Generated by Django 5.0.6 on 2024-07-28 15:52

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminSystem', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='walletmodel',
            name='date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='walletmodel',
            name='month',
            field=models.CharField(default='', max_length=20),
        ),
        migrations.AlterField(
            model_name='walletmodel',
            name='project_wallet',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='walletmodel',
            name='team_wallet',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='walletmodel',
            name='users_wallet',
            field=models.PositiveBigIntegerField(default=0),
        ),
    ]
