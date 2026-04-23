from django import forms

class InvestmentProfileForm(forms.Form):

    RISK_CHOICES = [
        ('Low', 'Low'),
        ('Moderate', 'Moderate'),
        ('High', 'High'),
    ]

    age = forms.IntegerField(min_value=18)
    monthly_income = forms.DecimalField(max_digits=10, decimal_places=2)
    monthly_expenses = forms.DecimalField(max_digits=10, decimal_places=2)
    risk_appetite = forms.ChoiceField(choices=RISK_CHOICES)
    investment_duration = forms.IntegerField(min_value=1, help_text="Enter in years")


