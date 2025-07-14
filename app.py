import streamlit as st
from loan_predictor import predict_loan_status
from db_utils import create_connection, create_tables, insert_application

st.title("AI Loan Approval Prediction")

with st.form("loan_form"):
    name = st.text_input("Applicant Name")
    gender = st.selectbox("Gender", ["Male", "Female"])
    married = st.selectbox("Married", ["Yes", "No"])
    dependents = st.selectbox("Dependents", ["0", "1", "2", "3+"])
    education = st.selectbox("Education", ["Graduate", "Not Graduate"])
    self_employed = st.selectbox("Self Employed", ["Yes", "No"])
    applicant_income = st.number_input("Applicant Income", min_value=0)
    coapplicant_income = st.number_input("Coapplicant Income", min_value=0)
    loan_amount = st.number_input("Loan Amount", min_value=0)
    loan_amount_term = st.number_input("Loan Amount Term (days)", min_value=0)
    credit_history = st.selectbox("Credit History", [1.0, 0.0])
    property_area = st.selectbox("Property Area", ["Urban", "Semiurban", "Rural"])

    submitted = st.form_submit_button("Predict Loan Status")

if submitted:
    input_data = {
        "Gender": gender,
        "Married": married,
        "Dependents": dependents,
        "Education": education,
        "Self_Employed": self_employed,
        "ApplicantIncome": applicant_income,
        "CoapplicantIncome": coapplicant_income,
        "LoanAmount": loan_amount,
        "Loan_Amount_Term": loan_amount_term,
        "Credit_History": credit_history,
        "Property_Area": property_area
    }

    result = predict_loan_status(input_data)
    if result["approved"]:
        st.success(f"Loan Approved with probability {result['approval_probability']:.2f}")
    else:
        st.error(f"Loan Denied with probability {1 - result['approval_probability']:.2f}")
    conn = create_connection()
    create_tables(conn)
    application_record = (
        name, gender, married, dependents, education, self_employed, applicant_income,
        coapplicant_income, loan_amount, loan_amount_term, credit_history, property_area,
        int(result["approved"])
    )
    insert_application(conn, application_record)
