
# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class MonthlySavings(models.Model):
    MONTHS = [
        ("Jan","Jan"), ("Feb","Feb"), ("Mar","Mar"),
        ("Apr","Apr"), ("May","May"), ("Jun","Jun"),
        ("Jul","Jul"), ("Aug","Aug"), ("Sep","Sep"),
        ("Oct","Oct"), ("Nov","Nov"), ("Dec","Dec"),
    ]

    month = models.CharField(max_length=3, choices=MONTHS)
    income = models.FloatField()
    expenses = models.FloatField()

    def saving(self):
        return self.income - self.expenses


class UserActivity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    action = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} — {self.action}"

class EMIRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.CharField(max_length=100)
    loan_amount = models.FloatField()
    rate = models.FloatField()
    months = models.IntegerField()
    emi = models.FloatField()
    created = models.DateTimeField(auto_now_add=True)