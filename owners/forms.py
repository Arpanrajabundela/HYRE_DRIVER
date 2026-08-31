from django import forms

from .models import OwnerProfile, DriverRequirement


class OwnerProfileForm(forms.ModelForm):

    class Meta:

        model = OwnerProfile

        exclude = (
            "user",
            "created_at",
            "updated_at",
            "is_verified",
            "is_profile_completed",
        )

        widgets = {

            "about": forms.Textarea(
                attrs={
                    "rows": 5,
                    "placeholder": "Tell us about your transport business...",
                }
            ),

            "address": forms.Textarea(
                attrs={
                    "rows": 3,
                    "placeholder": "Enter your complete address...",
                }
            ),

            "company_name": forms.TextInput(
                attrs={
                    "placeholder": "Enter company or business name",
                }
            ),

            "city": forms.TextInput(
                attrs={
                    "placeholder": "Enter your city",
                }
            ),

            "state": forms.TextInput(
                attrs={
                    "placeholder": "Enter your state",
                }
            ),

            "number_of_vehicles": forms.NumberInput(
                attrs={
                    "placeholder": "Enter number of vehicles",
                    "min": 1,
                }
            ),

            "profile_picture": forms.ClearableFileInput(
                attrs={
                    "accept": "image/*",
                }
            ),
        }


    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        # --------------------------------
        # FIELD STYLING
        # --------------------------------

        for name, field in self.fields.items():

            if name == "phone_visible":

                field.widget.attrs.update({
                    "class": "form-check-input"
                })

            elif isinstance(field.widget, forms.Select):

                field.widget.attrs.update({
                    "class": "form-select"
                })

            elif isinstance(field.widget, forms.FileInput):

                field.widget.attrs.update({
                    "class": "form-control"
                })

            else:

                field.widget.attrs.update({
                    "class": "form-control rounded-3 shadow-sm"
                })


        # --------------------------------
        # BETTER LABELS
        # --------------------------------

        self.fields["profile_picture"].label = "Profile Picture 📷"

        self.fields["owner_type"].label = "Owner Type 🏢"

        self.fields["company_name"].label = "Company / Business Name 🏭"

        self.fields["city"].label = "City 📍"

        self.fields["state"].label = "State 📌"

        self.fields["address"].label = "Complete Address 🏠"

        self.fields["number_of_vehicles"].label = "Number of Vehicles 🚚"

        self.fields["about"].label = "About Your Business ✨"

        self.fields["phone_visible"].label = "Show Phone Number to Drivers 📞"


        # --------------------------------
        # HELP TEXT
        # --------------------------------

        self.fields["company_name"].help_text = (
            "Enter your company or transport business name."
        )

        self.fields["number_of_vehicles"].help_text = (
            "How many vehicles do you currently manage?"
        )

        self.fields["about"].help_text = (
            "Briefly describe your transport business."
        )

        self.fields["phone_visible"].help_text = (
            "Allow drivers to see your phone number."
        )


# =========================================================
# DRIVER REQUIREMENT FORM
# =========================================================


class DriverRequirementForm(forms.ModelForm):

    class Meta:

        model = DriverRequirement

        exclude = (
            "owner",
            "status",
            "created_at",
            "updated_at",
        )

        widgets = {

            "title": forms.TextInput(
                attrs={
                    "class": "form-control rounded-3",
                    "placeholder": "Example: Heavy Truck Driver Required",
                }
            ),

            "vehicle_type": forms.Select(
                attrs={
                    "class": "form-select rounded-3",
                }
            ),

            "number_of_drivers": forms.NumberInput(
                attrs={
                    "class": "form-control rounded-3",
                    "min": 1,
                    "placeholder": "Number of drivers needed",
                }
            ),

            "city": forms.TextInput(
                attrs={
                    "class": "form-control rounded-3",
                    "placeholder": "Job location city",
                }
            ),

            "state": forms.TextInput(
                attrs={
                    "class": "form-control rounded-3",
                    "placeholder": "Job location state",
                }
            ),

            "experience_required": forms.NumberInput(
                attrs={
                    "class": "form-control rounded-3",
                    "min": 0,
                    "placeholder": "Years of experience",
                }
            ),

            "license_type": forms.Select(
                attrs={
                    "class": "form-select rounded-3",
                }
            ),

            "salary": forms.NumberInput(
                attrs={
                    "class": "form-control rounded-3",
                    "min": 0,
                    "step": "0.01",
                    "placeholder": "Monthly salary",
                }
            ),

            "description": forms.Textarea(
                attrs={
                    "class": "form-control rounded-3",
                    "rows": 6,
                    "placeholder": (
                        "Describe the job, responsibilities, "
                        "route, working hours, requirements, etc."
                    ),
                }
            ),
        }


    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        # --------------------------------
        # LABELS
        # --------------------------------

        self.fields["title"].label = "Requirement Title 📋"

        self.fields["vehicle_type"].label = "Vehicle Type 🚚"

        self.fields["number_of_drivers"].label = "Drivers Needed 👨‍🔧"

        self.fields["city"].label = "Job City 📍"

        self.fields["state"].label = "Job State 📌"

        self.fields["experience_required"].label = (
            "Experience Required (Years) 💼"
        )

        self.fields["license_type"].label = "Required License 🪪"

        self.fields["salary"].label = "Monthly Salary ₹"

        self.fields["description"].label = "Job Description 📝"


        # --------------------------------
        # HELP TEXT
        # --------------------------------

        self.fields["title"].help_text = (
            "Give your driver requirement a clear title."
        )

        self.fields["number_of_drivers"].help_text = (
            "How many drivers do you need?"
        )

        self.fields["experience_required"].help_text = (
            "Minimum driving experience required."
        )

        self.fields["salary"].help_text = (
            "Enter the expected monthly salary."
        )

        self.fields["description"].help_text = (
            "Add important details about the job."
        )