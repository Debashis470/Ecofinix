from django.shortcuts import render
from .forms import TaxInputForm
from .services import compute_tax
from .models import PolicyPDF
from .forms import RegimeCompareForm
from .forms import RegimeCompareForm
from .forms import PolicyUploadForm


def tax_home(request):
    return render(request, "tax/tax_home.html")


def tax_calculator(request):
    result = None

    if request.method == "POST":
        print("POST received")   # DEBUG

        form = TaxInputForm(request.POST)

        if form.is_valid():
            print("Form valid")  # DEBUG

            income = form.cleaned_data["annual_income"]
            deductions = form.cleaned_data.get("investment_deductions") or 0
            deductions += form.cleaned_data.get("hra") or 0
            regime = form.cleaned_data["regime"]

            result = compute_tax(income, deductions, regime)
            print("Result:", result)  # DEBUG

        else:
            print("Form errors:", form.errors)  # DEBUG

    else:
        form = TaxInputForm()

    return render(request, "tax/tax_form.html", {
        "form": form,
        "result": result
    })



def policy_list(request):
    policies = PolicyPDF.objects.all().order_by("-year")
    return render(request, "tax/policy_list.html", {
        "policies": policies
    })




def regime_compare(request):
    result = None

    if request.method == "POST":
        form = RegimeCompareForm(request.POST)

        if form.is_valid():
            income = form.cleaned_data["income"]
            inv = form.cleaned_data.get("investments") or 0
            hra = form.cleaned_data.get("hra") or 0

            old = compute_tax(income, inv + hra, "old")
            new = compute_tax(income, 0, "new")

            if old["total"] < new["total"]:
                better = "Old Regime"
                savings = new["total"] - old["total"]
            else:
                better = "New Regime"
                savings = old["total"] - new["total"]

            result = {
                "old": old,
                "new": new,
                "better": better,
                "savings": savings
            }

    else:
        form = RegimeCompareForm()

    return render(request, "tax/regime_compare.html", {
        "form": form,
        "result": result
    })
def tax_policy_view(request, year):
    try:
        policy = PolicyPDF.objects.get(year=year)
    except PolicyPDF.DoesNotExist:
        policy = None

    return render(request, "tax/policy_detail.html", {
        "policy": policy
    })
def policy_upload(request):
    if request.method == "POST":
        form = PolicyUploadForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return render(request, "tax/upload_success.html")

    else:
        form = PolicyUploadForm()

    return render(request, "tax/policy_upload.html", {"form": form})