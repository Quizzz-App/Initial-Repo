# Generated by Django 5.0.6 on 2024-08-01 22:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('paymentSystem', '0004_recieptmodel_recieptcode'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recieptmodel',
            name='recieptCode',
            field=models.CharField(max_length=50),
        ),
    ]
