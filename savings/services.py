from decimal import Decimal, ROUND_HALF_UP

def calculate_goal_savings(goal_name, goal_amount, target_value, current_savings, unit="months"):
    goal_amount = Decimal(goal_amount)
    current_savings = Decimal(current_savings)

    remaining_amount = goal_amount - current_savings
    if remaining_amount <= 0:
        return {
            "goal_name": goal_name,
            "goal_amount": goal_amount,
            "current_savings": current_savings,
            "target_months": 0,
            "monthly_saving": 0,
            "weekly_saving": 0,
            "remaining_amount": 0
        }

    target_months = target_value * 12 if unit=="years" else target_value
    monthly_saving = remaining_amount / Decimal(target_months)
    total_weeks = target_months * Decimal("4.345")
    weekly_saving = remaining_amount / total_weeks

    return {
        "goal_name": goal_name,
        "goal_amount": goal_amount,
        "current_savings": current_savings,
        "target_months": target_months,
        "monthly_saving": monthly_saving.quantize(Decimal("1."), rounding=ROUND_HALF_UP),
        "weekly_saving": weekly_saving.quantize(Decimal("1."), rounding=ROUND_HALF_UP),
        "remaining_amount": remaining_amount.quantize(Decimal("1."), rounding=ROUND_HALF_UP)
    }