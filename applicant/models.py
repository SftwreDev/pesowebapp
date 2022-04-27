from django.db import models
from authentication.models import User
from jobpost.models import *
from config.models import BaseModel
# Create your models here.

class ApplicationForm(BaseModel):
    status = (
        ("Approved", "Approved"),
        ("Disapproved", "Disapproved"),
        ("Pending", "Pending"),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="job_applicant")
    jobs = models.ForeignKey(JobPost, on_delete=models.CASCADE)
    resumes = models.FileField(upload_to="resumes/")
    additional_info = models.TextField(max_length=500)
    already_applied = models.BooleanField(default=True)
    approved = models.CharField(max_length=255, choices=status, default="Pending")

class ApplicantRequirement(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    jobs = models.ForeignKey(JobPost, on_delete=models.CASCADE)
    requirements_type = models.CharField(max_length=255)
    file = models.FileField(upload_to="requirements/")