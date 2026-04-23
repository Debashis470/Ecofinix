import joblib
import pandas as pd
import os

# -----------------------------
# Load Model Safely
# -----------------------------
BASE_DIR = os.path.dirname(__file__)
MODEL_PATH = os.path.join(BASE_DIR, "loan_model-Copy1.pkl")

model = joblib.load(MODEL_PATH)

# -----------------------------
# Feature Order (MUST match training)
# -----------------------------
FEATURES = [
    'number_of_dependents',
    'annual_income',
    'credit_score',
    'loan_amount',
    'term',
    'income_per_dep',
    'loan_income_ratio',
    'gender_Male',
    'marital_status_Yes',
    'education_Not Graduate',
    'property_area_Semiurban',
    'property_area_Urban'
]

# -----------------------------
# Prediction Function
# -----------------------------
def predict_loan(data_dict):

    df = pd.DataFrame([data_dict])
    df = df.reindex(columns=FEATURES, fill_value=0)

    pred = model.predict(df)[0]

    # works for Pipeline or model
    if hasattr(model, "predict_proba"):
        prob = model.predict_proba(df)[0][1]
    else:
        prob = 0.5

    return int(pred), float(prob)


# -----------------------------
# Advisor Logic
# -----------------------------
def build_advisor_output(pred, prob, data):

    percent = round(prob * 100)

    # softer approval rule (industry style)
    approved_flag = prob >= 0.45

    # ---------- Risk Level ----------
    if percent >= 70:
        risk = "Low"
    elif percent >= 50:
        risk = "Medium"
    else:
        risk = "High"

    reasons = []
    suggestions = []

    # ---------- Top Feature Checks ----------
    if data["credit_score"] < 720:
        reasons.append("Credit score below model safe zone")
        suggestions.append("Increase credit score above 720")

    if data["loan_income_ratio"] > 0.30:
        reasons.append("Loan too large relative to income")
        suggestions.append("Reduce loan amount or increase income")

    if data["income_per_dep"] < 250000:
        reasons.append("Income per dependent is low")
        suggestions.append("Increase household income")

    # ---------- Fallback ----------
    if percent < 50 and not reasons:
        reasons.append("Model detected hidden risk patterns")
        suggestions.append("Improve credit profile and reduce liabilities")

    # ---------- Never Empty Lists ----------
    if not reasons:
        reasons.append("No major risk factors detected")

    if not suggestions:
        suggestions.append("Profile looks strong")

    # ---------- Target Improvements ----------
    min_credit = max(720, int(data["credit_score"]))
    min_income = max(int(data["annual_income"]), int(data["loan_amount"] / 0.30))

    return {
        "approved": approved_flag,
        "approval_percent": percent,
        "risk_level": risk,
        "reasons": reasons,
        "suggestions": suggestions,
        "min_credit_for_better_chance": min_credit,
        "min_income_for_better_chance": min_income
    }
def build_improvement_plan(data, advisor_result):
  
    plan = []

    # credit gap
    credit_now = data["credit_score"]
    credit_target = advisor_result["min_credit_for_better_chance"]
    credit_gap = max(0, credit_target - credit_now)

    if credit_gap > 0:
        plan.append(f"Increase credit score by ~{credit_gap} points")

    # income gap
    income_now = data["annual_income"]
    income_target = advisor_result["min_income_for_better_chance"]
    income_gap = max(0, income_target - income_now)

    if income_gap > 0:
        plan.append(f"Increase annual income by ~₹{income_gap:,}")

    # ratio health
    ratio = data["loan_income_ratio"]

    if ratio > 0.35:
        plan.append("Reduce loan amount or extend term")

    if data["number_of_dependents"] > 3:
        plan.append("Lower dependent financial burden if possible")

    if not plan:
        plan.append("Your profile is already strong — maintain stability")

    return plan