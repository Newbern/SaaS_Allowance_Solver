from datetime import timezone

from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from datetime import datetime


# Create your models here.
class Allowance(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(default=datetime.now)

    # Getting Choices to be Chosen
    CHOICES = [("Weekly", "Weekly"), ("Biweekly", "Biweekly"), ("Monthly", "Monthly")]
    schedules = models.CharField(max_length=10, choices=CHOICES, default="Biweekly", blank=True)

    # Getting Allowance
    default_allowance = models.DecimalField(max_digits=10, decimal_places=2)
    set_allowance = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    # Saving Data
    def save(self, *args, **kwargs):
        # If The Set Allowance is None then Change Value to Default Allowance
        if self.set_allowance is None:
            self.set_allowance = self.default_allowance
        # Saving
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user} | {self.date} | {self.default_allowance}"


class Expense(models.Model):
    allowance = models.ForeignKey(Allowance, on_delete=models.CASCADE)
    expense = models.CharField(max_length=100)
    limit = models.DecimalField(max_digits=10, decimal_places=2)
    set = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    spending = ArrayField(models.DecimalField(max_digits=10, decimal_places=2), default=list, blank=True)

    # Saving Data
    def save(self, *args, **kwargs):
        # If The Set  is None then Change Value to limit
        if self.set is None:
            self.set = self.limit
        # Saving
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.allowance} | {self.expense} | {self.limit}"
