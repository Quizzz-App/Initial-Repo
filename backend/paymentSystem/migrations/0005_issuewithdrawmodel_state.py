# Generated by Django 5.1.2 on 2024-11-05 07:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('paymentSystem', '0004_issuewithdrawmodel_refcode_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='issuewithdrawmodel',
            name='state',
            field=models.CharField(default='Pending', max_length=50),
        ),
    ]
