# Generated by Django 5.1.2 on 2024-11-10 09:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authenticationSystem', '0005_customusermodel_profile_img'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customusermodel',
            name='profile_img',
            field=models.ImageField(blank=True, default='', null=True, upload_to='profile_images/'),
        ),
    ]
