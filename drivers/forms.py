from django import forms

from .models import DriverProfile


class DriverProfileForm(forms.ModelForm):

    class Meta:

        model = DriverProfile

        exclude = (
            "user",
            "created_at",
            "updated_at",
            "is_verified",
            "is_profile_completed",
        )

        widgets = {

            "date_of_birth": forms.DateInput(
                attrs={
                    "type": "date",
                    "class": "form-control",
                }
            ),

            "bio": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "placeholder": "Tell us about yourself, your driving experience, and the type of work you are looking for...",
                }
            ),

            "address": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": "Enter your complete address",
                }
            ),

            "license_number": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter Driving Licence Number",
                }
            ),

            "experience": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Years of Experience",
                    "min": "0",
                }
            ),

            "city": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter your city",
                }
            ),

            "state": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter your state",
                }
            ),

            "expected_salary": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Expected Monthly Salary",
                    "min": "0",
                }
            ),

        }


    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)


        # Required fields

        required_fields = [
            "license_number",
            "license_type",
            "experience",
            "preferred_vehicle",
            "city",
            "state",
        ]

        for field in required_fields:
            self.fields[field].required = True


        # Better labels

        self.fields["profile_picture"].label = "Profile Picture 📷"

        self.fields["date_of_birth"].label = "Date of Birth 🎂"

        self.fields["gender"].label = "Gender 👤"

        self.fields["license_number"].label = "Driving Licence Number 🪪"

        self.fields["license_type"].label = "Licence Type 🚘"

        self.fields["experience"].label = "Driving Experience 🛣️"

        self.fields["preferred_vehicle"].label = "Preferred Vehicle 🚚"

        self.fields["city"].label = "City 📍"

        self.fields["state"].label = "State 📌"

        self.fields["address"].label = "Address 🏠"

        self.fields["expected_salary"].label = "Expected Monthly Salary 💰"

        self.fields["available"].label = "Available for Work 🟢"

        self.fields["phone_visible"].label = "Show Phone Number 📞"

        self.fields["bio"].label = "About You ✨"


        # Add Bootstrap styling

        for name, field in self.fields.items():

            if name in [
                "available",
                "phone_visible",
            ]:
                continue

            field.widget.attrs.setdefault(
                "class",
                "form-control"
            )