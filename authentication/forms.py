from cProfile import label
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction

from .models import *


class DateInput(forms.DateInput):
    input_type = 'date'
 

class AdminSignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ["last_name", "first_name", "email", "username"]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = "admin"
        if commit:
            user.save()
        return user


class EmployerSignUpForm(UserCreationForm):
    company_name = forms.CharField(max_length=255)
    company_address = forms.CharField(max_length=255)
    business_nature = forms.CharField(max_length=255)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ["last_name", "first_name", "email", "username"]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = "employer"
        if commit:
            user.save()
        return user


class ApplicantSignUpForm(UserCreationForm):
    choices = (
        ("Yes", "Yes"),
        ("No", "No"),
    )
    address = forms.CharField(max_length=255)
    working_exp = forms.ChoiceField(choices = choices, label="Do you have working experience?")
    prev_employer = forms.CharField(max_length=255, label="Previous Employer (if you have working experience)")
    birthdate = forms.CharField(max_length=255)
    age = forms.CharField(max_length=255)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ["last_name", "first_name", "email", "username", "address", "working_exp", "prev_employer", "birthdate", "age"]

        widgets = {
            "birthdate" : DateInput()
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_student = True
        user.save()
        applicant = Applicant.objects.create(user=user)
        applicant.address.add(*self.cleaned_data.get('address'))
        applicant.working_exp.add(*self.cleaned_data.get('working_exp'))
        applicant.prev_employer.add(*self.cleaned_data.get('prev_employer'))
        applicant.birthdate.add(*self.cleaned_data.get('birthdate'))
        applicant.age.add(*self.cleaned_data.get('age'))
        return user

    

class UpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["last_name", "first_name", "email", "username"]
