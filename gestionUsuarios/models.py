from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, blank=True)
    full_name = models.CharField(max_length=255, blank=True)
    address = models.TextField(blank=True)
