
from django import forms
from .models import PolicyPDF

class TaxInputForm(forms.Form):

    annual_income = forms.DecimalField(
        label="Your Total Yearly Income (₹)",
        help_text="Enter your total income before tax for the full year",
        min_value=0,
        widget=forms.NumberInput(attrs={"placeholder": "Example: 850000"})
    )

    regime = forms.ChoiceField(
        label="Choose Tax System",
        choices=[
            ("old", "Old Tax Regime (with deductions)"),
            ("new", "New Tax Regime (lower rates, fewer deductions)")
        ]
    )

    investment_deductions = forms.DecimalField(
        label="Investment Deduction (₹)",
        required=False,
        help_text="Total amount invested in eligible schemes like PF, LIC, mutual funds, health insurance etc.",
        min_value=0,
        widget=forms.NumberInput(attrs={"placeholder": "Example: 150000"})
    )

    hra = forms.DecimalField(
        label="House Rent Allowance (HRA Exemption) (₹)",
        required=False,
        help_text="Only if you receive HRA from employer",
        min_value=0,
        widget=forms.NumberInput(attrs={"placeholder": "Example: 120000"})
    )

from django import forms

class RegimeCompareForm(forms.Form):
    income = forms.DecimalField(
        label="Income",
        min_value=0,
        widget=forms.NumberInput(attrs={
            "class": "form-control",
            "placeholder": "Enter yearly income"
        })
    )

    investments = forms.DecimalField(
        label="Investments",
        min_value=0,
        required=False,
        widget=forms.NumberInput(attrs={
            "class": "form-control",
            "placeholder": "Enter tax-saving investments"
        })
    )

    hra = forms.DecimalField(
        label="HRA",
        min_value=0,
        required=False,
        widget=forms.NumberInput(attrs={
            "class": "form-control",
            "placeholder": "Enter HRA exemption"
        })
    )



class PolicyUploadForm(forms.ModelForm):
    class Meta:
        model = PolicyPDF
        fields = ["title", "year", "description", "document"]