from django.urls import path
from . import views

urlpatterns = [

    # Driver list
    path(
        "",
        views.driver_list,
        name="driver_list"
    ),

    # Driver public profile
    path(
        "profile/<int:driver_id>/",
        views.driver_profile,
        name="driver_profile"
    ),

    # Driver dashboard
    path(
        "dashboard/",
        views.driver_dashboard,
        name="driver_dashboard"
    ),

    # Driver edit profile
    path(
        "complete-profile/",
        views.complete_profile,
        name="driver_complete_profile"
    ),
]