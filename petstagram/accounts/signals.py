from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

from petstagram.accounts.models import Profile

UserModel = get_user_model()


@receiver(post_save, sender=UserModel)
def create_user(sender, instance, created, **kwargs):
    if created:
        profile = Profile(user=instance)
        profile.save()
