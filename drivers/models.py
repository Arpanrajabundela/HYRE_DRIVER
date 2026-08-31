from django.db import models
from django.conf import settings


class DriverProfile(models.Model):

    LICENSE_CHOICES = [
        ("LMV", "LMV"),
        ("HMV", "HMV"),
        ("TRANSPORT", "Transport"),
    ]

    VEHICLE_CHOICES = [
    ("TRUCK", "Truck"),
    ("BUS", "Bus"),
    ("TAXI", "Taxi"),
    ("TEMPO", "Tempo"),
    ("TRAILER", "Trailer"),
    ("DUMPER", "Dumper"),
    ("OTHER", "Other"),
]

    GENDER_CHOICES = [
        ("Male", "Male"),
        ("Female", "Female"),
        ("Other", "Other"),
    ]


    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="driver_profile"
    )


    profile_picture = models.ImageField(
        upload_to="driver_profiles/",
        blank=True,
        null=True
    )


    date_of_birth = models.DateField(
        blank=True,
        null=True
    )


    gender = models.CharField(
        max_length=10,
        choices=GENDER_CHOICES,
        blank=True
    )


    license_number = models.CharField(
        max_length=50,
        blank=True
    )


    license_type = models.CharField(
        max_length=20,
        choices=LICENSE_CHOICES,
        blank=True
    )


    experience = models.PositiveIntegerField(
        default=0
    )


    preferred_vehicle = models.CharField(
        max_length=20,
        choices=VEHICLE_CHOICES,
        blank=True
    )


    city = models.CharField(
        max_length=100,
        blank=True
    )


    state = models.CharField(
        max_length=100,
        blank=True
    )


    address = models.TextField(
        blank=True
    )


    expected_salary = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True
    )


    available = models.BooleanField(
        default=True
    )


    phone_visible = models.BooleanField(
        default=True
    )


    bio = models.TextField(
        blank=True
    )


    is_verified = models.BooleanField(
        default=False
    )


    is_profile_completed = models.BooleanField(
        default=False
    )


    created_at = models.DateTimeField(
        auto_now_add=True
    )


    updated_at = models.DateTimeField(
        auto_now=True
    )


    class Meta:
        ordering = ["-created_at"]

        indexes = [
            models.Index(fields=["city"]),
            models.Index(fields=["available"]),
        ]

        verbose_name = "Driver Profile"
        verbose_name_plural = "Driver Profiles"


    def save(self, *args, **kwargs):

        required_fields = [
            self.license_number,
            self.license_type,
            self.city,
            self.experience,
        ]

        self.is_profile_completed = all(required_fields)

        super().save(*args, **kwargs)


    def __str__(self):
        return f"{self.user.full_name} - Driver Profile"