# Generated by Django 5.0.6 on 2024-07-30 23:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authenticationSystem', '0011_reviewmodel_review_type_alter_reviewmodel_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reviewmodel',
            name='review_type',
            field=models.CharField(max_length=20),
        ),
    ]
