from django import forms
from .models import *

class AnnouncementForms(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea)
    class Meta: 
        model = Announcement
        fields = ['title' , 'content']
