from django import forms

class GoalForm(forms.Form):
    goal_name = forms.CharField(label="Goal Name", max_length=100)
    goal_amount = forms.DecimalField(label="Goal Amount (₹)", min_value=0)
    current_savings = forms.DecimalField(label="Current Savings (₹)", min_value=0, required=False, initial=0)
    target_duration = forms.IntegerField(label="Target Duration", min_value=1)
    duration_unit = forms.ChoiceField(label="Duration Unit", choices=[('months','Months'),('years','Years')])

    def clean_current_savings(self):
        data = self.cleaned_data.get("current_savings")
        if data in [None, ""]:
            return 0
        return data

class SavingsInputForm(forms.Form):
    total_savings = forms.FloatField(
        label="Your Current Total Savings (₹)",
        widget=forms.NumberInput(attrs={"placeholder": "Eg: 120000"})
    )
