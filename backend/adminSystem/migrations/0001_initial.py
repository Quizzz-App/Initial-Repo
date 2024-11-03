# Generated by Django 5.1.2 on 2024-11-03 15:24

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('authenticationSystem', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
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
            name='WalletModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('wallet_name', models.CharField(default='', max_length=20, unique=True)),
                ('project_wallet', models.PositiveIntegerField(default=0)),
                ('users_wallet', models.PositiveBigIntegerField(default=0)),
                ('team_wallet', models.PositiveIntegerField(default=0)),
                ('date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='AdminDeveloperUserModel',
            fields=[
                ('customusermodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('approved_status', models.BooleanField(default=False)),
                ('status', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='adminSystem.admindeveloperstatusmodel')),
            ],
            options={
                'abstract': False,
            },
            bases=('authenticationSystem.customusermodel',),
        ),
        migrations.CreateModel(
            name='developer_wallet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('balance', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('name', models.CharField(max_length=20, null=True)),
                ('month', models.IntegerField(default=11)),
                ('year', models.IntegerField(default=2024)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
