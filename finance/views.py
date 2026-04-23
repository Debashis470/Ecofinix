from unittest import result
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from .forms import LoanPredictForm
from .ml_predict import predict_loan, build_advisor_output
from .forms import SavingsForm
from .models import EMIRecord, MonthlySavings
from .forms import MonthlySavingsForm
from .activity import UserActivity
from django.db.models import Sum





def signup_view(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        User.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        return redirect('login')

    return render(request, 'auth/signup.html')

def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('dashboard')
        if user is None:
            return render(request, 'auth/login.html', {
                "error": "Invalid username or password"
            })

    return render(request, 'auth/login.html')
    

def logout_view(request):
    logout(request)
    return redirect('login')
@login_required
def dashboard_view(request):
    if not request.user.is_authenticated:
        return redirect('login')

    return render(request, 'dashboard/dashboard.html')
import math

def emi_view(request):
    emi = interest = total = None

    if request.method == "POST":
        P = float(request.POST["amount"])
        annual_rate = float(request.POST["rate"])
        years = int(request.POST["years"])

        r = annual_rate / 12 / 100
        n = years * 12

        emi = P * r * (1+r)**n / ((1+r)**n - 1)
        total = emi * n
        interest = total - P

        emi = round(emi, 2)
        total = round(total, 2)
        interest = round(interest, 2)
        log_activity(request.user, f"EMI calculated for ₹{P}")
    return render(request, "finance/emi.html", {
        "emi": emi,
        "interest": interest,
        "total": total
    })



@login_required
def loan_predict_view(request):

    result = None
    form = LoanPredictForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        cd = form.cleaned_data

        income_per_dep = cd["annual_income"] / max(cd["number_of_dependents"], 1)
        loan_income_ratio = cd["loan_amount"] / max(cd["annual_income"], 1)

        data = {
            "number_of_dependents": cd["number_of_dependents"],
            "annual_income": cd["annual_income"],
            "credit_score": cd["credit_score"],
            "loan_amount": cd["loan_amount"],
            "term": cd["term"],
            "income_per_dep": income_per_dep,
            "loan_income_ratio": loan_income_ratio,

            "gender_Male": 1 if cd["gender"] == "Male" else 0,
            "marital_status_Yes": 1 if cd["marital_status"] == "Yes" else 0,
            "education_Not Graduate": 1 if cd["education"] == "Not Graduate" else 0,
            "property_area_Semiurban": 1 if cd["property_area"] == "Semiurban" else 0,
            "property_area_Urban": 1 if cd["property_area"] == "Urban" else 0,
        }

        pred, prob = predict_loan(data)

        result = build_advisor_output(pred, prob, data)

        print("DEBUG:", result)   # keep for now
        log_activity(request.user, "Used Loan Eligibility Predictor")

    return render(request, "finance/loan_dashboard.html", {
        "form": form,
        "result": result
    })
from .ml_predict import build_improvement_plan

@login_required
def credit_planner_view(request):
  
    result = None
    plan = None

    if request.method == "POST":
        form = LoanPredictForm(request.POST)

        if form.is_valid():
            cd = form.cleaned_data

            income_per_dep = cd["annual_income"] / max(cd["number_of_dependents"], 1)
            loan_income_ratio = cd["loan_amount"] / max(cd["annual_income"], 1)

            data = {
                "number_of_dependents": cd["number_of_dependents"],
                "annual_income": cd["annual_income"],
                "credit_score": cd["credit_score"],
                "loan_amount": cd["loan_amount"],
                "term": cd["term"],
                "income_per_dep": income_per_dep,
                "loan_income_ratio": loan_income_ratio,
                "gender_Male": cd["gender"] == "Male",
                "marital_status_Yes": cd["marital_status"] == "Yes",
                "education_Not Graduate": cd["education"] == "Not Graduate",
                "property_area_Semiurban": cd["property_area"] == "Semiurban",
                "property_area_Urban": cd["property_area"] == "Urban",
            }

            pred, prob = predict_loan(data)
            result = build_advisor_output(pred, prob, data)

            plan = result["suggestions"]   # reuse suggestions as roadmap

    else:
        form = LoanPredictForm()
    log_activity(request.user, "Accessed Credit Planner")

    return render(request, "finance/credit_planner.html", {
        "form": form,
        "result": result,
        "plan": plan
    })



@login_required
def savings_view(request):

    if "savings_data" not in request.session:
        request.session["savings_data"] = []

    result = None

    if request.method == "POST":
        month = request.POST["month"]
        income = float(request.POST["income"])
        expenses = float(request.POST["expenses"])

        savings = income - expenses

        entry = {
            "month": month,
            "income": income,
            "expenses": expenses,
            "savings": savings
        }

        data = request.session.get("savings_data", [])

        # ✅ update if month already exists
        data = [x for x in data if x["month"] != month]
        data.append(entry)

        request.session["savings_data"] = data
        request.session.modified = True   # ⭐ IMPORTANT

        result = {
            "income": income,
            "expenses": expenses,
            "monthly_savings": savings,
            "yearly_savings": sum(x["savings"] for x in data)
        }

        log_activity(request.user, f"Savings updated for {month}")

    data = request.session.get("savings_data", [])

    months = [x["month"] for x in data]
    incomes = [x["income"] for x in data]
    expenses = [x["expenses"] for x in data]
    savings = [x["savings"] for x in data]

    return render(request, "finance/savings_dashboard.html", {
        "result": result,
        "months": months,
        "incomes": incomes,
        "expenses": expenses,
        "savings": savings,
    })
@login_required
def dashboard_view(request):
    emis = EMIRecord.objects.filter(user=request.user)

    total_emi = emis.aggregate(total=Sum("emi"))["total"] or 0
    emi_count = emis.count()

    activities = UserActivity.objects.filter(
        user=request.user
    ).order_by("-created_at")[:5]

    return render(request, "dashboard/dashboard.html", {
        
        "total_emi": round(total_emi, 2),
        "emi_count": emi_count, 
        "activities": activities
        
    })
from .models import UserActivity

def log_activity(user, text):
    if user.is_authenticated:
        UserActivity.objects.create(
            user=user,
            action=text
        )
from .models import EMIRecord

import math

def calculate_emi(P, annual_rate, months):
    r = annual_rate / 12 / 100

    if r == 0:
        return P / months

    emi = P * r * (1+r)**months / ((1+r)**months - 1)
    return emi
from .models import EMIRecord

@login_required
def emi_view2(request):

    result = None

    if request.method == "POST":

        item_name = request.POST["item"]
        price = float(request.POST["price"])
        down_payment = float(request.POST["down"])
        rate = float(request.POST["rate"])
        tenure_value = int(request.POST["tenure"])
        tenure_unit = request.POST["unit"]

        months = tenure_value * 12 if tenure_unit == "years" else tenure_value
        loan_amount = price - down_payment

        emi = calculate_emi(loan_amount, rate, months)
        total_payment = emi * months
        interest = total_payment - loan_amount

        # ✅ save EMI record
        EMIRecord.objects.create(
            user=request.user,
            item=item_name,
            loan_amount=loan_amount,
            rate=rate,
            months=months,
            emi=round(emi, 2)
        )

        result = {
            "item": item_name,
            "price": price,
            "down": down_payment,
            "loan": loan_amount,
            "months": months,
            "rate": rate,
            "emi": round(emi,2),
            "total": round(total_payment,2),
            "interest": round(interest,2)
        }

        log_activity(request.user, f"Calculated EMI for {item_name}")

    return render(request, "finance/emi_dashboard.html", {
        "result": result
    })
import json

@login_required
def emi_list_view(request):

    emis = EMIRecord.objects.filter(user=request.user)

    labels = json.dumps([e.item for e in emis])
    values = json.dumps([float(e.emi) for e in emis])

    return render(request,"finance/emi_dashboard.html", {
        "emis": emis,
        "labels": labels,
        "values": values
    })