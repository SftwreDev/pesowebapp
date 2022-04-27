from django.db import models

# Create your models here.

class BaseModel(models.Model):
    status = (
        ("Active", "Active"),
        ("Inactive", "Inactive"),
    )
    created_at = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=255, choices=status, name="status")