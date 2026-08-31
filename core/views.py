from django.shortcuts import render

from owners.models import DriverRequirement


def home(request):

    requirements = DriverRequirement.objects.filter(
        status="ACTIVE"
    )[:6]

    return render(
        request,
        "core/home.html",
        {
            "requirements": requirements,
        }
    )

def pricing(request):
    return render(request, "pricing/pricing.html")

def contact(request):
    return render(request, "contact/contact.html")

def about(request):
    return render(request, "about/about.html")

def terms_conditions(request):

    return render(
        request,
        "terms_conditions.html"
    )