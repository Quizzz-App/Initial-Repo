# Generated by Django 5.1.2 on 2024-11-10 09:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authenticationSystem', '0004_alter_notifications_notificationtype'),
    ]

    operations = [
        migrations.AddField(
            model_name='customusermodel',
            name='profile_img',
            field=models.FileField(blank=True, default='', null=True, upload_to='profile_images/'),
        ),
    ]
