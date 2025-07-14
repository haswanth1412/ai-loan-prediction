import joblib
import numpy as np
import pandas as pd

model = joblib.load('model.pkl')
preprocessor = joblib.load('preprocessor.pkl')

def predict_loan_status(input_data: dict) -> dict:
    """
    input_data keys must match dataset columns except target and id:
    ['Gender', 'Married', 'Dependents', 'Education', 'Self_Employed', 'ApplicantIncome',
    'CoapplicantIncome', 'LoanAmount', 'Loan_Amount_Term', 'Credit_History', 'Property_Area']
    """
    df = pd.DataFrame([input_data])
    X_processed = preprocessor.transform(df)
    proba = model.predict_proba(X_processed)[0][1]
    pred = model.predict(X_processed)[0]
    return {"approved": bool(pred), "approval_probability": proba}
