# Generated by Django 5.0.6 on 2024-07-14 17:31

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questionSystem', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='questionlevel',
            old_name='level',
            new_name='name',
        ),
        migrations.RenameField(
            model_name='questionscategory',
            old_name='category',
            new_name='name',
        ),
        migrations.AlterField(
            model_name='questionsmodel',
            name='uID',
            field=models.UUIDField(default=uuid.uuid4, unique=True),
        ),
    ]
