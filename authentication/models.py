from lib2to3.pytree import Base
from this import d
from django.db import models
from django.contrib.auth.models import AbstractUser
from config.models import BaseModel

# Create your models here.


class User(AbstractUser):
    role = (
        ("superadmin", "superadmin"),
        ("admin", "admin"),
        ("employer", "employer"),
        ("applicant", "applicant"),
    )
    role = models.CharField(max_length=255, choices=role)
    is_verified = models.BooleanField(default=False)


class Employer(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    company_name = models.CharField(max_length=255, name="Company Name")
    company_address = models.CharField(max_length=255, name="Company Address")
    business_nature = models.CharField(
        max_length=255, name="Nature of Business", help_text="Ex. FastFood, IT, BPO")

    def __str__(self):
        return self.company_name


class Applicant(BaseModel):
    choices = (
        ("Yes", "Yes"),
        ("No", "No"),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    address = models.CharField(max_length=255, name="Address")
    working_exp = models.CharField(max_length=255, choices=choices, name="Have working experience?")
    prev_employer = models.CharField(max_length=255, blank=True, null=True, name="Previous employer/s (*if you have working experience)")
    birthdate = models.DateField(auto_now_add=False)
    age = models.IntegerField()

    def __str__(self):
        return f"{self.last_name}, {self.first_name}"