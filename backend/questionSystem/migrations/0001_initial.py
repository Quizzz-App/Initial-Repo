# Generated by Django 5.0.6 on 2024-08-25 05:14

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='QuestionLevel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='QuestionsCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='QuestionsModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uID', models.UUIDField(default=uuid.uuid4, unique=True)),
                ('question', models.CharField(max_length=99999999999999999999999999999999999999, unique=True)),
                ('correct_answer', models.CharField(max_length=999999999999999999999)),
                ('incorrect_answers', models.CharField(max_length=999999999999999999999999999999)),
                ('aurthor', models.CharField(max_length=50)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='questionSystem.questionscategory')),
                ('level', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='questionSystem.questionlevel')),
            ],
        ),
    ]
