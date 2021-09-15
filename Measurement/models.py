from django.db import models
from django.db.models.base import Model
from django.db.models.fields import AutoField
from django.core.validators import FileExtensionValidator

# Create your models here.
class Measurement(models.Model):
    location = models.CharField(max_length=200)
    destination = models.CharField(max_length=200)
    distance = models.DecimalField(max_digits=10, decimal_places=2)
    created = models.DateTimeField(auto_now_add=True)
    video = models.FileField(upload_to='videos_uploaded',null=True,validators=[FileExtensionValidator(allowed_extensions=['MOV','avi','mp4','webm','mkv'])])


    def __str__(self):
        return f"Distance From {self.location} to {self.destination} is {self.distance} KM"
