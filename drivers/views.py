from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from owners.models import DriverApplication
from .forms import DriverProfileForm
from .models import DriverProfile


def driver_list(request):

    drivers = DriverProfile.objects.all()

    # Get search values from URL
    state = request.GET.get("state", "").strip()
    city = request.GET.get("city", "").strip()
    vehicle_type = request.GET.get("vehicle_type", "").strip()
    available = request.GET.get("available", "").strip()


    # Filter by state
    if state:

        drivers = drivers.filter(
            state__icontains=state
        )


    # Filter by city
    if city:

        drivers = drivers.filter(
            city__icontains=city
        )


    # Filter by vehicle type
    if vehicle_type:

        drivers = drivers.filter(
            preferred_vehicle=vehicle_type
        )


    # Filter available drivers
    if available == "1":

        drivers = drivers.filter(
            available=True
        )


    return render(
        request,
        "drivers/driver_list.html",
        {
            "drivers": drivers,

            # Send search values back to template
            "search_state": state,
            "search_city": city,
            "search_vehicle": vehicle_type,
            "search_available": available,
        }
    )

def driver_profile(request, driver_id):

    driver = get_object_or_404(
        DriverProfile,
        id=driver_id
    )

    return render(
        request,
        "drivers/driver_profile.html",
        {
            "driver": driver
        }
    )

@login_required
def driver_dashboard(request):

    profile, created = DriverProfile.objects.get_or_create(
        user=request.user
    )

    # Profile completion
    completion_fields = [
        profile.profile_picture,
        profile.date_of_birth,
        profile.gender,
        profile.license_number,
        profile.license_type,
        profile.experience,
        profile.preferred_vehicle,
        profile.city,
        profile.state,
        profile.address,
        profile.expected_salary,
        profile.bio,
    ]

    completed_fields = sum(
        bool(field)
        for field in completion_fields
    )

    total_fields = len(completion_fields)

    if total_fields:
        profile_completion = int(
            (completed_fields / total_fields) * 100
        )
    else:
        profile_completion = 0

    # Driver's job applications
    from owners.models import DriverApplication

    applications = DriverApplication.objects.filter(
        driver=profile
    ).select_related(
        "requirement",
        "requirement__owner"
    )

    return render(
        request,
        "drivers/dashboard.html",
        {
            "profile": profile,
            "profile_completion": profile_completion,
            "applications": applications,
        }
    )
@login_required
def complete_profile(request):

    profile, created = DriverProfile.objects.get_or_create(
        user=request.user
    )

    if request.method == "POST":

        form = DriverProfileForm(
            request.POST,
            request.FILES,
            instance=profile
        )

        if form.is_valid():

            profile = form.save(commit=False)

            profile.user = request.user

            profile.save()

            messages.success(
                request,
                "Profile updated successfully."
            )

            return redirect("driver_dashboard")

    else:

        form = DriverProfileForm(
            instance=profile
        )

    return render(
        request,
        "drivers/complete_profile.html",
        {
            "form": form
        }
    )