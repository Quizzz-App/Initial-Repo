# Generated by Django 5.1.2 on 2024-11-05 06:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('paymentSystem', '0003_issuewithdrawmodel_acn'),
    ]

    operations = [
        migrations.AddField(
            model_name='issuewithdrawmodel',
            name='refCode',
            field=models.CharField(default='', max_length=50),
        ),
        migrations.AlterField(
            model_name='issuewithdrawmodel',
            name='timestamp',
            field=models.DateField(auto_now_add=True),
        ),
    ]
