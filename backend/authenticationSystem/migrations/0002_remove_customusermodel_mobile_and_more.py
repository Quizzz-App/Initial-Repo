# Generated by Django 5.0.6 on 2024-06-25 18:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authenticationSystem', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customusermodel',
            name='mobile',
        ),
        migrations.AddField(
            model_name='customusermodel',
            name='points_earned',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='customusermodel',
            name='referral_code',
            field=models.CharField(blank=True, max_length=240),
        ),
        migrations.AddField(
            model_name='customusermodel',
            name='referral_code_expired',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='customusermodel',
            name='referrals',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='customusermodel',
            name='referred_by',
            field=models.CharField(blank=True, max_length=240),
        ),
    ]
