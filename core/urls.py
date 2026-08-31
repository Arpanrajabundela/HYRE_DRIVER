from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("pricing/", views.pricing, name="pricing"),
    path("contact/", views.contact, name="contact"),
    path("about/", views.about, name="about"),
    path(
    "terms-and-conditions/",
    views.terms_conditions,
    name="terms_conditions"
    ),
]