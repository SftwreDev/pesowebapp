from django import  forms
from django.forms import ClearableFileInput
from .models import *

class ApplyJobForm(forms.ModelForm):
    class Meta:
        model = ApplicationForm
        fields = ['resumes' , 'additional_info']


class ApplicantRequirementsForm(forms.ModelForm):
    class Meta:
        model = ApplicantRequirement
        fields = ['file']
        widgets = {
            'file': ClearableFileInput(attrs={'multiple': True})
        }