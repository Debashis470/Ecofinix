
# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class MonthlySavings(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    month = models.DateField()
    income = models.FloatField()
    savings = models.FloatField()

    def __str__(self):
        return f"{self.user.username} - {self.month}"
