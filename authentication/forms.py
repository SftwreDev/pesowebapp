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
        fields = ["last_name", "first_name", "email"]

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
        fields = ["profile_picture", "last_name", "first_name", "email",
                  "company_name", "company_address", "business_nature"]

    # @transaction.atomic
    # def save(self):
    #     cleaned_data = super().clean()
    #     user = super().save(commit=False)
    #     user.role = "employer"
    #     user.save()
    #     employer = Employer.objects.create(user=user, company_name=cleaned_data('company_name', None), company_address=cleaned_data(
    #         'company_address', None), business_nature=cleaned_data('business_nature', None))
    #     # employer.company_name.add(*self.cleaned_data('company_name'))
    #     # employer.company_address.add(*self.cleaned_data('company_address'))
    #     # employer.business_nature.add(*self.cleaned_data('business_nature'))
    #     return user


class ApplicantSignUpForm(UserCreationForm):
    choices = (
        ("Yes", "Yes"),
        ("No", "No"),
    )
    address = forms.CharField(max_length=255)
    working_exp = forms.ChoiceField(
        choices=choices, label="Do you have working experience?")
    prev_employer = forms.CharField(
        max_length=255, label="Previous Employer (if you have working experience)", initial="N/A")
    birthdate = forms.CharField(max_length=255, widget=DateInput())
    age = forms.CharField(max_length=255)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ["profile_picture", "last_name", "first_name", "email",
                 "address", "working_exp", "prev_employer", "birthdate", "age"]

        widgets = {
            "birthdate": DateInput()
        }

    # def save(self, commit=True):
    #     user = super().save(commit=False)
    #     user.is_student = True
    #     user.save()
    #     applicant = Applicant.objects.create(user=user)
    #     applicant.address.add(*self.cleaned_data.get('address'))
    #     applicant.working_exp.add(*self.cleaned_data.get('working_exp'))
    #     applicant.prev_employer.add(*self.cleaned_data.get('prev_employer'))
    #     applicant.birthdate.add(*self.cleaned_data.get('birthdate'))
    #     applicant.age.add(*self.cleaned_data.get('age'))
    #     return user


class UpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["last_name", "first_name", "email"]

class LoginForm(forms.Form):
    email = forms.CharField(max_length=63)
    password = forms.CharField(max_length=63, widget=forms.PasswordInput)