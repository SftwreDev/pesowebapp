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
    username = None
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    role = models.CharField(max_length=255, choices=role)
    is_verified = models.BooleanField(default=False)
    profile_picture = models.ImageField(upload_to="profile_picture/")

    


class Employer(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name="user_employer")
    company_name = models.CharField(max_length=255)
    company_address = models.CharField(max_length=255)
    business_nature = models.CharField(
        max_length=255, help_text="Ex. FastFood, IT, BPO")
    accepted = models.BooleanField(default=False)

    def __str__(self):
        return self.company_name
        
class Applicant(BaseModel):
    choices = (
        ("Yes", "Yes"),
        ("No", "No"),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name="user_applicant")
    address = models.CharField(max_length=255)
    working_exp = models.CharField(max_length=255, choices=choices)
    prev_employer = models.CharField(max_length=255, blank=True, null=True)
    birthdate = models.DateField(auto_now_add=False)
    age = models.IntegerField()
    contact = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.user.last_name}, {self.user.first_name}"

     