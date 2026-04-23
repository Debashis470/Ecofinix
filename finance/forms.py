from django import forms
from .models import MonthlySavings
from django.forms import ModelForm

class LoanPredictForm(forms.Form):

    number_of_dependents = forms.IntegerField()
    annual_income = forms.FloatField()
    credit_score = forms.IntegerField()
    loan_amount = forms.FloatField()

    term = forms.IntegerField(label="Loan Term (Months)")

    gender = forms.ChoiceField(
        choices=[("Male","Male"),("Female","Female")]
    )

    marital_status = forms.ChoiceField(
        choices=[("Yes","Yes"),("No","No")]
    )

    education = forms.ChoiceField(
        choices=[("Graduate","Graduate"),("Not Graduate","Not Graduate")]
    )

    property_area = forms.ChoiceField(
        choices=[
            ("Rural","Rural"),
            ("Semiurban","Semiurban"),
            ("Urban","Urban")
        ]
    )
class SavingsForm(forms.Form):
    month = forms.CharField()
    income = forms.FloatField()
    expenses = forms.FloatField()

class MonthlySavingsForm(ModelForm):
    class Meta:
        model = MonthlySavings
        fields = ["month", "income", "expenses"]