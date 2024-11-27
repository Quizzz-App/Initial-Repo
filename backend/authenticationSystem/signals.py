import os
from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import CustomUserModel
from django.conf import settings

@receiver(pre_save, sender= CustomUserModel)
def delete_old_profile_image(sender, instance, **kwargs):
    if instance.pk:
        old_instance= CustomUserModel.objects.get(pk= instance.pk)
        if old_instance.profile_img and old_instance.profile_img != instance.profile_img:
            old_image_path= old_instance.profile_img.path
            if os.path.isfile(old_image_path):
                os.remove(old_image_path)