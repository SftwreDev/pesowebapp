import django_filters

from .models import *

class JobPostFilter(django_filters.FilterSet):
    
    class Meta:
        model = JobPost
        fields = {
            "title" : ['icontains']
        }