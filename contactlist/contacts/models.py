from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class Contact(models.Model):
    full_name = models.CharField(max_length=500)
    relationship = models.CharField(max_length=50)
    email = models.EmailField(max_length=25)
    phone_number = models.CharField(max_length=10)
    address = models.CharField(max_length=100)

    def __str__(self) :
        return self.full_name
    
