# Generated by Django 4.2.16 on 2024-10-31 23:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questionSystem', '0003_quizpreparation'),
    ]

    operations = [
        migrations.AddField(
            model_name='quizpreparation',
            name='created_on',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
