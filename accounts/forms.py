from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from .models import User


class RegisterForm(UserCreationForm):

    ROLE_CHOICES = [
        ("driver", "Driver"),
        ("owner", "Vehicle Owner"),
    ]


    role = forms.ChoiceField(
        choices=ROLE_CHOICES,
        widget=forms.RadioSelect,
        initial="driver"
    )


    class Meta:

        model = User

        fields = (
            "full_name",
            "email",
            "phone_number",
            "role",
            "password1",
            "password2",
        )


    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)


        self.fields["full_name"].widget.attrs.update(
            {
                "class": "form-control",
                "placeholder": "Enter your full name"
            }
        )


        self.fields["email"].widget.attrs.update(
            {
                "class": "form-control",
                "placeholder": "Enter your email"
            }
        )


        self.fields["phone_number"].widget.attrs.update(
            {
                "class": "form-control",
                "placeholder": "Enter your phone number"
            }
        )


        self.fields["password1"].widget.attrs.update(
            {
                "class": "form-control",
                "placeholder": "Create a password"
            }
        )


        self.fields["password2"].widget.attrs.update(
            {
                "class": "form-control",
                "placeholder": "Confirm your password"
            }
        )


    def save(self, commit=True):

        user = super().save(commit=False)


        user.email = User.objects.normalize_email(
            self.cleaned_data["email"]
        )

        user.full_name = self.cleaned_data["full_name"]

        user.phone_number = self.cleaned_data["phone_number"]

        user.role = self.cleaned_data["role"]


        if commit:
            user.save()


        return user



class LoginForm(AuthenticationForm):

    username = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
                "placeholder": "Enter your email",
            }
        )
    )


    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Enter your password",
            }
        )
    )