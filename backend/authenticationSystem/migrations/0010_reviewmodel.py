# Generated by Django 5.0.6 on 2024-07-30 23:00

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authenticationSystem', '0009_remove_customusermodel_dev_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReviewModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, unique=True)),
                ('message', models.CharField(max_length=999999999999999999999999999999999999999999999999999999999999999999999999999999999999999)),
                ('user', models.CharField(default='', max_length=100)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
