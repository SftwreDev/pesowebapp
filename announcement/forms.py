from django import forms
from .models import *

class AnnouncementForms(forms.ModelForm):
    class Meta: 
        model = Announcement
        fields = '__all__'
