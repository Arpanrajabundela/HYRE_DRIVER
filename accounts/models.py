from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone

from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):

    DRIVER = "driver"
    OWNER = "owner"
    ADMIN = "admin"

    ROLE_CHOICES = [
        (DRIVER, "Driver"),
        (OWNER, "Vehicle Owner"),
        (ADMIN, "Admin"),
    ]

    full_name = models.CharField(max_length=150)

    email = models.EmailField(
        unique=True
    )

    phone_number = models.CharField(
        max_length=15,
        blank=True
    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default=DRIVER
    )

    profile_picture = models.ImageField(
        upload_to="profile_pictures/",
        blank=True,
        null=True
    )

    is_verified = models.BooleanField(
        default=False
    )

    is_active = models.BooleanField(
        default=True
    )

    is_staff = models.BooleanField(
        default=False
    )

    date_joined = models.DateTimeField(
        default=timezone.now
    )


    objects = UserManager()


    USERNAME_FIELD = "email"

    REQUIRED_FIELDS = [
        "full_name"
    ]


    def __str__(self):
        return self.email


    # Required for Django permissions
    def has_perm(self, perm, obj=None):
        return self.is_staff


    def has_module_perms(self, app_label):
        return self.is_staff