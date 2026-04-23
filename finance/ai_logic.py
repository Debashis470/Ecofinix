def predict_loan(income, existing_emi, loan_amount, credit_score, employment):
    ratio = existing_emi / income

    score = 0

    if credit_score > 750:
        score += 40
    elif credit_score > 650:
        score += 25

    if ratio < 0.4:
        score += 30

    if loan_amount < income * 20:
        score += 20

    if employment == "salaried":
        score += 10

    if score >= 70:
        return "Eligible", score, "Low risk applicant"
    elif score >= 50:
        return "Borderline", score, "Moderate risk"
    else:
        return "Not Eligible", score, "High risk"