from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout

from .forms import RegisterForm, LoginForm
from drivers.models import DriverProfile
from owners.models import OwnerProfile



def register(request):

    if request.method == "POST":

        form = RegisterForm(request.POST)

        if form.is_valid():

            user = form.save()


            # DRIVER
            if user.role == "driver":

                DriverProfile.objects.get_or_create(
                    user=user
                )


            # OWNER
            elif user.role == "owner":

                OwnerProfile.objects.get_or_create(
                    user=user
                )


            messages.success(
                request,
                "Account created successfully."
            )


            return redirect("login")


        else:

            print(form.errors)


    else:

        form = RegisterForm()


    return render(
        request,
        "accounts/register.html",
        {
            "form": form
        }
    )

def login_view(request):

    if request.method == "POST":

        form = LoginForm(
            request,
            data=request.POST
        )

        if form.is_valid():

            user = form.get_user()

            login(
                request,
                user
            )

            messages.success(
                request,
                f"Welcome {user.full_name}!"
            )

            # Redirect according to user role

            if user.role == "driver":
                return redirect("driver_dashboard")

            elif user.role == "owner":
                return redirect("owner_dashboard")

            return redirect("home")

        else:

            print(form.errors)

    else:

        form = LoginForm()

    return render(
        request,
        "accounts/login.html",
        {
            "form": form
        }
    )


def logout_view(request):

    logout(request)


    messages.success(
        request,
        "You have been logged out successfully."
    )


    return redirect("/")