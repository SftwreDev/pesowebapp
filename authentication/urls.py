from django.urls import path, include


from .views import *

urlpatterns = [
    path('accounts/', include('django.contrib.auth.urls')),
    path("authentication/register/admin", AdminSignUpView.as_view(), name="admin-register"),
    path("authentication/register/employer", EmployerSignUpView.as_view(), name="employer-register"),
    path("authentication/register/applicant", ApplicantSignUpView.as_view(), name="applicant-register")
]