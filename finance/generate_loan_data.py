import pandas as pd
import numpy as np

np.random.seed(42)

rows = 1200

data = {
    "Gender": np.random.choice(["Male", "Female"], rows),
    "Married": np.random.choice(["Yes", "No"], rows),
    "Education": np.random.choice(["Graduate", "Not Graduate"], rows),
    "Self_Employed": np.random.choice(["Yes", "No"], rows),
    "ApplicantIncome": np.random.randint(15000, 150000, rows),
    "CoapplicantIncome": np.random.randint(0, 80000, rows),
    "LoanAmount": np.random.randint(50, 600, rows),
    "Loan_Amount_Term": np.random.choice([180, 240, 300, 360], rows),
    "Credit_History": np.random.choice([0, 1], rows, p=[0.25, 0.75]),
    "Property_Area": np.random.choice(["Urban", "Semiurban", "Rural"], rows),
}

df = pd.DataFrame(data)

# Simple approval logic (for realistic pattern)
df["Loan_Status"] = (
    (df["Credit_History"] == 1) &
    (df["ApplicantIncome"] + df["CoapplicantIncome"] > 40000)
).astype(int)

df.to_csv("loan_data.csv", index=False)

print("✅ loan_data.csv created with", len(df), "rows")