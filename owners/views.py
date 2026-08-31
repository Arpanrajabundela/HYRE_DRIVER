from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from .forms import OwnerProfileForm, DriverRequirementForm
from .models import DriverRequirement, DriverApplication


# =========================================================
# VEHICLE OWNER LANDING PAGE
# =========================================================

def vehicle_owner(request):

    return render(
        request,
        "owners/vehicle_owner.html"
    )


# =========================================================
# OWNER DASHBOARD
# =========================================================

@login_required
def owner_dashboard(request):

    # Only allow owners

    if request.user.role != "owner":

        return redirect("/")

    # Get owner's profile

    profile = request.user.owner_profile

    # Owner's requirements

    requirements = DriverRequirement.objects.filter(
        owner=profile
    )

    context = {
        "profile": profile,
        "requirements": requirements,
    }

    return render(
        request,
        "owners/dashboard.html",
        context
    )


# =========================================================
# EDIT OWNER PROFILE
# =========================================================

@login_required
def edit_owner_profile(request):

    profile = request.user.owner_profile

    if request.method == "POST":

        form = OwnerProfileForm(
            request.POST,
            request.FILES,
            instance=profile
        )

        if form.is_valid():

            profile = form.save(
                commit=False
            )

            profile.is_profile_completed = True

            profile.save()

            return redirect(
                "owner_dashboard"
            )

    else:

        form = OwnerProfileForm(
            instance=profile
        )

    return render(
        request,
        "owners/edit_profile.html",
        {
            "form": form
        }
    )


# =========================================================
# POST DRIVER REQUIREMENT
# =========================================================

@login_required
def post_requirement(request):

    # Only owners can post requirements

    if request.user.role != "owner":

        return redirect("/")

    # Get owner's profile

    owner_profile = request.user.owner_profile

    if request.method == "POST":

        form = DriverRequirementForm(
            request.POST
        )

        if form.is_valid():

            requirement = form.save(
                commit=False
            )

            # Connect requirement to owner

            requirement.owner = owner_profile

            # New requirement is active

            requirement.status = "ACTIVE"

            requirement.save()

            return redirect(
                "owner_dashboard"
            )

    else:

        form = DriverRequirementForm()

    return render(
        request,
        "owners/post_requirement.html",
        {
            "form": form
        }
    )


# =========================================================
# REQUIREMENT DETAIL
# =========================================================

@login_required
def requirement_detail(request, requirement_id):

    requirement = get_object_or_404(
        DriverRequirement,
        id=requirement_id
    )

    return render(
        request,
        "owners/requirement_detail.html",
        {
            "requirement": requirement
        }
    )


# =========================================================
# DRIVER APPLY FOR REQUIREMENT
# =========================================================

@login_required
def apply_for_requirement(request, requirement_id):

    # Only drivers can apply

    if request.user.role != "driver":

        return redirect("/")

    # Get driver profile

    driver_profile = request.user.driver_profile

    # Get requirement

    requirement = get_object_or_404(
        DriverRequirement,
        id=requirement_id
    )

    # Requirement must be active

    if requirement.status != "ACTIVE":

        return redirect(
            "requirement_detail",
            requirement_id=requirement.id
        )

    # Check if driver already applied

    already_applied = DriverApplication.objects.filter(
        driver=driver_profile,
        requirement=requirement
    ).exists()

    if already_applied:

        return redirect(
            "requirement_detail",
            requirement_id=requirement.id
        )

    # Create application

    DriverApplication.objects.create(
        driver=driver_profile,
        requirement=requirement,
        status="PENDING"
    )

    return redirect(
        "requirement_detail",
        requirement_id=requirement.id
    )


# =========================================================
# ALL DRIVER JOBS
# =========================================================

@login_required
def driver_jobs(request):

    # Only drivers can access all jobs

    if request.user.role != "driver":

        return redirect("/")

    requirements = DriverRequirement.objects.filter(
        status="ACTIVE"
    )

    return render(
        request,
        "owners/driver_jobs.html",
        {
            "requirements": requirements
        }
    )


# =========================================================
# JOB DETAIL FOR DRIVER
# =========================================================

@login_required
def job_detail(request, requirement_id):

    # Only drivers can view driver job details

    if request.user.role != "driver":

        return redirect("/")

    requirement = get_object_or_404(
        DriverRequirement,
        id=requirement_id,
        status="ACTIVE"
    )

    return render(
        request,
        "owners/job_detail.html",
        {
            "requirement": requirement
        }
    )


# =========================================================
# APPLY FOR JOB
# =========================================================

@login_required
def apply_for_job(request, requirement_id):

    # Only drivers can apply

    if request.user.role != "driver":

        return redirect("/")

    # Get driver profile

    driver_profile = request.user.driver_profile

    # Get active requirement

    requirement = get_object_or_404(
        DriverRequirement,
        id=requirement_id,
        status="ACTIVE"
    )

    # Create application if it does not already exist

    application, created = DriverApplication.objects.get_or_create(
        driver=driver_profile,
        requirement=requirement,
        defaults={
            "status": "PENDING"
        }
    )

    return render(
        request,
        "owners/application_submitted.html",
        {
            "application": application,
            "requirement": requirement,
            "created": created,
        }
    )


# =========================================================
# DRIVER DASHBOARD
# =========================================================

@login_required
def driver_dashboard(request):

    # Only drivers can access this dashboard

    if request.user.role != "driver":

        return redirect("/")

    # Get driver's profile

    driver_profile = request.user.driver_profile

    # Get all applications submitted by this driver

    applications = DriverApplication.objects.filter(
        driver=driver_profile
    ).select_related(
        "requirement",
        "requirement__owner"
    )

    context = {
        "driver_profile": driver_profile,
        "applications": applications,
    }

    return render(
        request,
        "drivers/dashboard.html",
        context
    )

@login_required
def view_applications(request, requirement_id):

    if request.user.role != "owner":
        return redirect("/")

    owner_profile = request.user.owner_profile

    requirement = get_object_or_404(
        DriverRequirement,
        id=requirement_id,
        owner=owner_profile
    )

    applications = DriverApplication.objects.filter(
        requirement=requirement
    ).select_related(
        "driver",
        "driver__user"
    )

    return render(
        request,
        "owners/view_applications.html",
        {
            "requirement": requirement,
            "applications": applications,
        }
    )

# =========================================================
# ACCEPT DRIVER APPLICATION
# =========================================================

@login_required
def accept_application(request, application_id):

    # Only owners can accept applications
    if request.user.role != "owner":
        return redirect("/")

    # Get owner's profile
    owner_profile = request.user.owner_profile

    # Get application belonging to this owner
    application = get_object_or_404(
        DriverApplication,
        id=application_id,
        requirement__owner=owner_profile
    )

    # Get the requirement
    requirement = application.requirement

    # Job must still be active
    if requirement.status != "ACTIVE":
        return redirect(
            "view_applications",
            requirement_id=requirement.id
        )

    # Application must still be pending
    if application.status != "PENDING":
        return redirect(
            "view_applications",
            requirement_id=requirement.id
        )

    # Count already accepted drivers
    accepted_count = DriverApplication.objects.filter(
        requirement=requirement,
        status="ACCEPTED"
    ).count()

    # Check whether all driver positions are already filled
    if accepted_count >= requirement.number_of_drivers:

        # Close the requirement
        requirement.status = "CLOSED"
        requirement.save()

        return redirect(
            "view_applications",
            requirement_id=requirement.id
        )

    # Accept this driver
    application.status = "ACCEPTED"

    application.owner_response = (
        "Your application has been accepted. "
        "The vehicle owner will contact you soon."
    )

    application.save()

    # Count accepted drivers again
    accepted_count = DriverApplication.objects.filter(
        requirement=requirement,
        status="ACCEPTED"
    ).count()

    # Close job when all required drivers are accepted
    if accepted_count >= requirement.number_of_drivers:

        requirement.status = "CLOSED"
        requirement.save()

    return redirect(
        "view_applications",
        requirement_id=requirement.id
    )

# =========================================================
# REJECT DRIVER APPLICATION
# =========================================================

@login_required
def reject_application(request, application_id):

    # Only owners can reject applications
    if request.user.role != "owner":
        return redirect("/")

    owner_profile = request.user.owner_profile

    application = get_object_or_404(
        DriverApplication,
        id=application_id,
        requirement__owner=owner_profile
    )

    application.status = "REJECTED"
    application.owner_response = (
        "Thank you for applying. "
        "Unfortunately, your application was not selected."
    )
    application.save()

    return redirect(
        "view_applications",
        requirement_id=application.requirement.id
    )