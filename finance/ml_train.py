import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import joblib

df = pd.read_csv("loan_data.csv")

# feature engineering
df["total_income"] = df["ApplicantIncome"] + df["CoapplicantIncome"]
df["loan_income_ratio"] = df["LoanAmount"] / df["total_income"]

# encode categorical
le_dict = {}

for col in df.select_dtypes(include="object"):
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col].astype(str))
    le_dict[col] = le

X = df.drop("Loan_Status", axis=1)
y = df["Loan_Status"]

model = RandomForestClassifier(n_estimators=200)
model.fit(X, y)

joblib.dump(
    {
        "model": model,
        "features": X.columns.tolist()
    },
    "finance/loan_model-Copy1.pkl"
)

print("Model bundle saved ✅")
print("Features:", X.columns.tolist())
print("Model saved with features ✅")
print("Features:", X.columns.tolist())