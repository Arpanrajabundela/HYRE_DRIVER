from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import User
from drivers.models import DriverProfile
from owners.models import OwnerProfile


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):

    if created:

        if instance.role == "driver":

            DriverProfile.objects.create(
                user=instance
            )

        elif instance.role == "owner":

            OwnerProfile.objects.create(
                user=instance
            )