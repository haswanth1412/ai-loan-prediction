import sqlite3
import pandas as pd

def create_connection(db_name="loan_db.sqlite"):
    conn = sqlite3.connect(db_name)
    return conn

def create_tables(conn):
    query = """
    CREATE TABLE IF NOT EXISTS loan_applications (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        applicant_name TEXT,
        gender TEXT,
        married TEXT,
        dependents TEXT,
        education TEXT,
        self_employed TEXT,
        applicant_income REAL,
        coapplicant_income REAL,
        loan_amount REAL,
        loan_amount_term REAL,
        credit_history REAL,
        property_area TEXT,
        loan_status INTEGER
    );
    """
    conn.execute(query)
    conn.commit()

def insert_application(conn, application_data):
    query = """
    INSERT INTO loan_applications (
        applicant_name, gender, married, dependents, education, self_employed, applicant_income,
        coapplicant_income, loan_amount, loan_amount_term, credit_history, property_area, loan_status
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
    """
    conn.execute(query, application_data)
    conn.commit()

def fetch_all(conn):
    return pd.read_sql_query("SELECT * FROM loan_applications", conn)
