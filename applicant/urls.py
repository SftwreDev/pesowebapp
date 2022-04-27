from django.urls import path

from .views import *

urlpatterns = [
    path("applied-job-status/<int:pk>", proceed_next_step, name="proceed_next_step")
]