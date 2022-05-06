from django.db import models
from authentication.models import User
from config.models import BaseModel

# Create your models here.
class Announcement(BaseModel):
    title = models.CharField(max_length=225)
    content = models.CharField(max_length=2000)
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Announcement"

    def __str__(self):
        return self.title
        