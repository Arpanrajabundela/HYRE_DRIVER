from django.urls import path
from . import views


urlpatterns = [

    # =====================================================
    # VEHICLE OWNER LANDING PAGE
    # =====================================================

    path(
        "",
        views.vehicle_owner,
        name="vehicle_owner"
    ),


    # =====================================================
    # OWNER DASHBOARD
    # =====================================================

    path(
        "dashboard/",
        views.owner_dashboard,
        name="owner_dashboard"
    ),


    # =====================================================
    # EDIT OWNER PROFILE
    # =====================================================

    path(
        "edit-profile/",
        views.edit_owner_profile,
        name="edit_owner_profile"
    ),


    # =====================================================
    # POST DRIVER REQUIREMENT
    # =====================================================

    path(
        "post-requirement/",
        views.post_requirement,
        name="post_requirement"
    ),


    # =====================================================
    # DRIVER JOBS
    # =====================================================

    # All available jobs
    path(
        "driver-jobs/",
        views.driver_jobs,
        name="driver_jobs"
    ),


    # Job details
    path(
        "driver-jobs/<int:requirement_id>/",
        views.job_detail,
        name="job_detail"
    ),


    # Apply for a job
    path(
        "driver-jobs/<int:requirement_id>/apply/",
        views.apply_for_job,
        name="apply_for_job"
    ),


    # =====================================================
    # DRIVER DASHBOARD
    # =====================================================

    path(
        "driver-dashboard/",
        views.driver_dashboard,
        name="driver_dashboard"
    ),

    path(
    "requirement/<int:requirement_id>/applications/",
    views.view_applications,
    name="view_applications"
    ),

    # Accept application
path(
    "application/<int:application_id>/accept/",
    views.accept_application,
    name="accept_application"
),

# Reject application
path(
    "application/<int:application_id>/reject/",
    views.reject_application,
    name="reject_application"
),

]