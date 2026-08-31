from django.db import models
from django.conf import settings


class OwnerProfile(models.Model):

    OWNER_TYPE_CHOICES = [
        ("INDIVIDUAL", "Individual"),
        ("COMPANY", "Company"),
        ("TRANSPORT_AGENCY", "Transport Agency"),
    ]


    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="owner_profile"
    )


    profile_picture = models.ImageField(
        upload_to="owner_profiles/",
        blank=True,
        null=True
    )


    owner_type = models.CharField(
        max_length=30,
        choices=OWNER_TYPE_CHOICES,
        default="INDIVIDUAL"
    )


    company_name = models.CharField(
        max_length=150,
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


    number_of_vehicles = models.PositiveIntegerField(
        default=1
    )


    phone_visible = models.BooleanField(
        default=True
    )


    about = models.TextField(
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
        ]

        verbose_name = "Owner Profile"
        verbose_name_plural = "Owner Profiles"


    def save(self, *args, **kwargs):

        required_fields = [
            self.city,
            self.state,
            self.address,
            self.number_of_vehicles,
            self.about,
        ]

        self.is_profile_completed = all(
            str(field).strip()
            for field in required_fields
        )

        super().save(*args, **kwargs)


    def __str__(self):

        return f"{self.user.full_name} - Owner Profile"


# =========================================================
# DRIVER REQUIREMENT
# =========================================================


class DriverRequirement(models.Model):

    VEHICLE_CHOICES = [
        ("TRUCK", "Truck"),
        ("BUS", "Bus"),
        ("TAXI", "Taxi"),
        ("TEMPO", "Tempo"),
        ("TRAILER", "Trailer"),
        ("DUMPER", "Dumper"),
        ("OTHER", "Other"),
    ]


    LICENSE_CHOICES = [
        ("LMV", "LMV"),
        ("HMV", "HMV"),
        ("TRANSPORT", "Transport"),
    ]


    STATUS_CHOICES = [
        ("ACTIVE", "Active"),
        ("CLOSED", "Closed"),
    ]


    # Owner who created the requirement

    owner = models.ForeignKey(
        OwnerProfile,
        on_delete=models.CASCADE,
        related_name="requirements"
    )


    # Requirement title

    title = models.CharField(
        max_length=200
    )


    # Vehicle required

    vehicle_type = models.CharField(
        max_length=20,
        choices=VEHICLE_CHOICES
    )


    # Number of drivers required

    number_of_drivers = models.PositiveIntegerField(
        default=1
    )


    # Job location

    city = models.CharField(
        max_length=100
    )


    state = models.CharField(
        max_length=100
    )


    # Experience required

    experience_required = models.PositiveIntegerField(
        default=0
    )


    # Licence required

    license_type = models.CharField(
        max_length=20,
        choices=LICENSE_CHOICES
    )


    # Salary

    salary = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True
    )


    # Job description

    description = models.TextField()


    # Requirement status

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default="ACTIVE"
    )


    # Timestamps

    created_at = models.DateTimeField(
        auto_now_add=True
    )


    updated_at = models.DateTimeField(
        auto_now=True
    )


    class Meta:

        ordering = ["-created_at"]

        indexes = [

            models.Index(
                fields=["city"]
            ),

            models.Index(
                fields=["state"]
            ),

            models.Index(
                fields=["vehicle_type"]
            ),

            models.Index(
                fields=["status"]
            ),

        ]

        verbose_name = "Driver Requirement"
        verbose_name_plural = "Driver Requirements"


    def __str__(self):

        return self.title
# =========================================================
# DRIVER APPLICATION
# =========================================================


class DriverApplication(models.Model):

    STATUS_CHOICES = [
        ("PENDING", "Pending"),
        ("ACCEPTED", "Accepted"),
        ("REJECTED", "Rejected"),
    ]


    # Driver who is applying

    driver = models.ForeignKey(
        "drivers.DriverProfile",
        on_delete=models.CASCADE,
        related_name="applications"
    )


    # Requirement the driver is applying for

    requirement = models.ForeignKey(
        DriverRequirement,
        on_delete=models.CASCADE,
        related_name="applications"
    )


    # Application status

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default="PENDING"
    )


    # Message written by driver

    message = models.TextField(
        blank=True
    )


    # Response written by owner

    owner_response = models.TextField(
        blank=True
    )


    # Timestamps

    created_at = models.DateTimeField(
        auto_now_add=True
    )


    updated_at = models.DateTimeField(
        auto_now=True
    )


    class Meta:

        ordering = ["-created_at"]

        constraints = [

            models.UniqueConstraint(
                fields=[
                    "driver",
                    "requirement"
                ],
                name="unique_driver_requirement_application"
            )

        ]

        indexes = [

            models.Index(
                fields=["status"]
            ),

            models.Index(
                fields=["driver"]
            ),

            models.Index(
                fields=["requirement"]
            ),

        ]

        verbose_name = "Driver Application"

        verbose_name_plural = "Driver Applications"


    def __str__(self):

        return (
            f"{self.driver.user.full_name} "
            f"- {self.requirement.title}"
        )