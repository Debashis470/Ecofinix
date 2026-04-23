# investment/views.py
from django.shortcuts import render
from .forms import InvestmentProfileForm

def investment_dashboard(request):
    result = None
    if request.method == "POST":
        form = InvestmentProfileForm(request.POST)
        if form.is_valid():
            age = form.cleaned_data["age"]
            income = form.cleaned_data["monthly_income"]
            expenses = form.cleaned_data["monthly_expenses"]
            risk_appetite = form.cleaned_data["risk_appetite"]
            duration = form.cleaned_data["investment_duration"]

            # -----------------------------
            # AI RISK SCORING LOGIC
            # -----------------------------
            risk_score = 0
            if age < 30: risk_score += 2
            elif age < 45: risk_score += 1

            savings_capacity = income - expenses
            if savings_capacity > 50000: risk_score += 2
            elif savings_capacity > 20000: risk_score += 1

            if risk_appetite == "High": risk_score += 3
            elif risk_appetite == "Moderate": risk_score += 2
            else: risk_score += 1

            if duration >= 10: risk_score += 2
            elif duration >= 5: risk_score += 1

            # Risk Level Classification
            if risk_score <= 3:
                risk_level = "Low"
                stocks, gold, fixed_income = 30, 40, 30
                stock_strategy = "Focus on large-cap and dividend stocks for stability."
                gold_strategy = "Higher gold allocation for capital protection."
            elif risk_score <= 6:
                risk_level = "Moderate"
                stocks, gold, fixed_income = 60, 25, 15
                stock_strategy = "Balanced portfolio with large-cap and index funds."
                gold_strategy = "Moderate gold allocation for diversification."
            else:
                risk_level = "High"
                stocks, gold, fixed_income = 75, 15, 10
                stock_strategy = "Growth-oriented portfolio including mid and small-cap stocks."
                gold_strategy = "Lower gold allocation; focus on high-growth equities."

            result = {
                "risk_score": risk_score,
                "risk_level": risk_level,
                "stocks": stocks,
                "gold": gold,
                "fixed_income": fixed_income,
                "stock_strategy": stock_strategy,
                "gold_strategy": gold_strategy,
            }
    else:
        form = InvestmentProfileForm()

    return render(request, "investment/investment_dashboard.html", {
        "form": form,
        "result": result,
    })
from django.shortcuts import render
from .models import MonthlySavings
import json

def dashboard(request):
    records = MonthlySavings.objects.filter(user=request.user).order_by('month')

    months = [record.month.strftime("%b %Y") for record in records]
    savings = [record.savings for record in records]

    context = {
        "months": json.dumps(months),
        "savings": json.dumps(savings)
    }

    return render(request, "dashboard.html", context)


