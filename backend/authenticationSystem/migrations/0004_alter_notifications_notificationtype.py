# Generated by Django 5.1.2 on 2024-11-05 16:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authenticationSystem', '0003_notifications_notificationtype'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notifications',
            name='notificationType',
            field=models.CharField(max_length=100),
        ),
    ]
