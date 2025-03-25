from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Account(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    access_token = models.CharField(max_length=255, blank=True, null=True)
    item_id = models.CharField(max_length=255, blank=True, null=True)
    institution_name = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.user}: {self.institution_name}"