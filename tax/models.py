from django.db import models

# Create your models here.
from django.db import models

class TaxSlab(models.Model):
    regime = models.CharField(max_length=10)  # old/new
    min_income = models.IntegerField()
    max_income = models.IntegerField()
    rate = models.FloatField()





class PolicyPDF(models.Model):
    title = models.CharField(max_length=200)
    year = models.IntegerField()
    description = models.TextField(blank=True)

    document = models.FileField(
        upload_to="tax_docs/",
        null=True,
        blank=True
    )

    def __str__(self):
        return self.title