# Generated by Django 5.0.6 on 2024-06-27 11:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authenticationSystem', '0005_customusermodel_indirectreferrals'),
    ]

    operations = [
        migrations.AddField(
            model_name='tokensmodel',
            name='refCode',
            field=models.CharField(default='', max_length=240),
        ),
    ]
