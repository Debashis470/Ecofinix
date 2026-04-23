from decimal import Decimal, ROUND_HALF_UP
from django.shortcuts import render
from django.forms import formset_factory
from .forms import GoalForm


def savings_dashboard(request):

    results = []
    total_monthly = Decimal("0")
    total_weekly = Decimal("0")
    total_savings = Decimal("0")

    step = 1
    num_goals = 0

    if request.method == "POST":

        # STEP 1 SUBMIT
        if "start_planning" in request.POST:
            total_savings = Decimal(request.POST.get("total_savings") or "0")
            num_goals = int(request.POST.get("num_goals") or 1)

            GoalFormSet = formset_factory(GoalForm, extra=num_goals)
            formset = GoalFormSet()

            step = 2

        # STEP 2 SUBMIT
        elif "analyze_goals" in request.POST:

            total_savings = Decimal(request.POST.get("total_savings") or "0")
            num_goals = int(request.POST.get("num_goals") or 1)

            GoalFormSet = formset_factory(GoalForm, extra=num_goals)
            formset = GoalFormSet(request.POST)

            step = 2

            if formset.is_valid():
                for form in formset:
                    data = form.cleaned_data

                    if not data.get("goal_name"):
                        continue

                    goal_name = data["goal_name"]
                    goal_amount = Decimal(data["goal_amount"])
                    current_savings = Decimal(data.get("current_savings") or 0)
                    target_duration = int(data["target_duration"])
                    duration_unit = data["duration_unit"]

                    months = target_duration * 12 if duration_unit == "years" else target_duration
                    months = max(months, 1)

                    remaining_amount = max(goal_amount - current_savings, Decimal("0"))
                    monthly_saving = remaining_amount / Decimal(months)
                    weekly_saving = remaining_amount / (Decimal(months) * Decimal("4.345"))

                    total_monthly += monthly_saving
                    total_weekly += weekly_saving

                    results.append({
                        "goal_name": goal_name,
                        "goal_amount": goal_amount,
                        "current_savings": current_savings,
                        "remaining_amount": remaining_amount.quantize(Decimal("1."), rounding=ROUND_HALF_UP),
                        "monthly_saving": monthly_saving.quantize(Decimal("1."), rounding=ROUND_HALF_UP),
                        "weekly_saving": weekly_saving.quantize(Decimal("1."), rounding=ROUND_HALF_UP),
                    })

        else:
            formset = None

    else:
        formset = None

    can_achieve = total_savings >= sum(
        goal["remaining_amount"] for goal in results
    ) if results else False

    context = {
        "step": step,
        "formset": formset,
        "results": results,
        "total_savings": total_savings,
        "total_monthly": total_monthly.quantize(Decimal("1."), rounding=ROUND_HALF_UP),
        "total_weekly": total_weekly.quantize(Decimal("1."), rounding=ROUND_HALF_UP),
        "num_goals": num_goals,
        "can_achieve": can_achieve,
    }

    return render(request, "savings/multi_goal_form.html", context)
