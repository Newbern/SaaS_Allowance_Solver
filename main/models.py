from datetime import timezone

from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from datetime import datetime
from decimal import Decimal


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
    spending = models.JSONField(default=dict, blank=True)

    def add_expense(self, expense, limit):
        data = {expense: {"limit": limit, "set": limit, "item": {}}}
        self.spending.update(data)

    def add_spending(self, expense, description, amount):
        date = str(datetime.today().date())
        time = str(datetime.today().time())
        self.spending[expense]['item'].update({description: {"amount": amount, "date": date, "time": time}})
        super().save()

    def __str__(self):
        return f"{self.allowance} | {[expense for expense in self.spending]}"

