# Generated by Django 5.0.6 on 2024-07-30 20:48

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminSystem', '0004_rename_month_walletmodel_wallet_name'),
        ('authenticationSystem', '0009_remove_customusermodel_dev_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='AdminDeveloperStatusModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='AdminDeveloperUserModel',
            fields=[
                ('customusermodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('status', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='adminSystem.admindeveloperstatusmodel')),
            ],
            options={
                'abstract': False,
            },
            bases=('authenticationSystem.customusermodel',),
        ),
    ]
